"""
Automated Screenshot Generator for Smart Quiz & Performance Analyzer.
Captures high-resolution images of each main screen for repository documentation.
"""

import os
import time
import struct
import ctypes
from ctypes import wintypes
import tkinter as tk
from PIL import Image

from quiz_gui import SmartQuizApp
from quiz_system import QUIZ_QUESTIONS, classify_performance

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

def capture_window(root, output_path):
    root.update_idletasks()
    root.update()
    time.sleep(0.3)
    root.update()

    hwnd = root.winfo_id()
    hwnd_parent = user32.GetParent(hwnd)
    target_hwnd = hwnd_parent if hwnd_parent else hwnd

    rect = wintypes.RECT()
    user32.GetWindowRect(target_hwnd, ctypes.byref(rect))
    w = rect.right - rect.left
    h = rect.bottom - rect.top

    hdc_window = user32.GetWindowDC(target_hwnd)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_window)
    hbm = gdi32.CreateCompatibleBitmap(hdc_window, w, h)
    gdi32.SelectObject(hdc_mem, hbm)

    res = user32.PrintWindow(target_hwnd, hdc_mem, 2)
    if not res:
        res = user32.PrintWindow(target_hwnd, hdc_mem, 0)

    bmpinfo = bytearray(40)
    struct.pack_into('<IiiHHIIIIII', bmpinfo, 0, 40, w, -h, 1, 32, 0, w * h * 4, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(hdc_mem, hbm, 0, h, buf, bytes(bmpinfo), 0)

    gdi32.DeleteObject(hbm)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(target_hwnd, hdc_window)

    img = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'BGRA', 0, 1).convert('RGB')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Captured: {output_path} ({w}x{h})")

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(out_dir, exist_ok=True)

    root = tk.Tk()
    app = SmartQuizApp(root)
    root.geometry("920x720")
    root.update()

    # 1. Main Dashboard
    app.show_home_screen()
    capture_window(root, os.path.join(out_dir, "01_dashboard.png"))

    # 2. Question Screen (Select option B for demonstration)
    app.start_quiz()
    app.selected_option_var.set("B")
    capture_window(root, os.path.join(out_dir, "02_quiz_question.png"))

    # 3. Populate realistic multi-attempt history
    attempt1 = {
        "attempt_number": 1,
        "raw_score": 3.75,
        "effective_score": 3.75,
        "max_score": 6.0,
        "percentage": 62.5,
        "level": "Intermediate",
        "recommendation": "Good foundation! Review tricky corner cases in control flow and scope.",
        "correct_count": 4,
        "incorrect_count": 1,
        "weak_topics": {
            "Functions & Scope": ["Review local vs global variable shadowing and LEGB scope rules."]
        }
    }

    attempt2 = {
        "attempt_number": 2,
        "raw_score": 5.0,
        "effective_score": 5.0,
        "max_score": 6.0,
        "percentage": 83.33,
        "level": "Advanced",
        "recommendation": "Outstanding mastery! You demonstrate high accuracy and in-depth conceptual grasp.",
        "correct_count": 5,
        "incorrect_count": 0,
        "weak_topics": {
            "Data Structures": ["Review dictionary key immutability requirements."]
        }
    }

    attempt3 = {
        "attempt_number": 3,
        "raw_score": 6.0,
        "effective_score": 6.0,
        "max_score": 6.0,
        "percentage": 100.0,
        "level": "Advanced",
        "recommendation": "Flawless score! Exceptional conceptual clarity across all tested modules.",
        "correct_count": 6,
        "incorrect_count": 0,
        "weak_topics": {}
    }

    app.quiz_history = [attempt1, attempt2]

    # 3. Results Screen
    app.show_results_screen(attempt2)
    capture_window(root, os.path.join(out_dir, "03_quiz_results.png"))

    # 4. Performance Analytics Screen (with all 3 attempts)
    app.quiz_history = [attempt1, attempt2, attempt3]
    app.show_analysis_screen()
    capture_window(root, os.path.join(out_dir, "04_performance_analysis.png"))

    root.destroy()
    print("All screenshots successfully captured in ./screenshots/")

if __name__ == "__main__":
    main()
