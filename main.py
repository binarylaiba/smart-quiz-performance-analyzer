"""
Convenience entry point for the Smart Quiz & Performance Analyzer System.

Usage:
  py main.py         -> Launches the modern Tkinter GUI
  py main.py --cli   -> Launches the interactive Console/Terminal mode
  py main.py --gui   -> Explicitly launches the Tkinter GUI
"""
import sys

def main():
    if "--cli" in sys.argv:
        from quiz_system import main as run_cli
        run_cli()
    else:
        try:
            from quiz_gui import launch_gui
            launch_gui()
        except Exception as err:
            print(f"[!] Could not launch Tkinter GUI ({err}). Falling back to console mode...")
            from quiz_system import main as run_cli
            run_cli()

if __name__ == "__main__":
    main()
