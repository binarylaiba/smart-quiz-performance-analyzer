"""
=============================================================================
         SMART QUIZ & PERFORMANCE ANALYZER SYSTEM (TKINTER GUI)
=============================================================================
Author: Python Instructor
Description: A modern, beautiful, beginner-friendly Tkinter GUI version of
             the Smart Quiz & Performance Analyzer System.
             Includes interactive quiz taking, negative marking (+1 / -0.25),
             topic-based weak area detection, performance tier classification,
             and multi-attempt session analytics.
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Import shared questions and helper functions from quiz_system
from quiz_system import QUIZ_QUESTIONS, classify_performance


class SmartQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Quiz & Performance Analyzer")
        self.root.geometry("880x680")
        self.root.minsize(800, 600)

        # Session attempt history list
        self.quiz_history = []

        # Active quiz state variables
        self.current_question_index = 0
        self.current_score = 0.0
        self.correct_count = 0
        self.incorrect_count = 0
        self.current_weak_topics = {}
        self.selected_option_var = tk.StringVar(value="")

        # Setup modern dark theme colors
        self.colors = {
            "bg": "#0f172a",          # Slate 900
            "card": "#1e293b",        # Slate 800
            "card_border": "#334155", # Slate 700
            "primary": "#6366f1",     # Indigo 500
            "primary_hover": "#4f46e5",
            "success": "#10b981",     # Emerald 500
            "danger": "#ef4444",      # Rose 500
            "warning": "#f59e0b",     # Amber 500
            "text": "#f8fafc",        # Slate 50
            "text_muted": "#94a3b8",  # Slate 400
            "badge_bg": "#312e81",
            "option_bg": "#243048",
            "option_select": "#3730a3"
        }

        self.root.configure(bg=self.colors["bg"])
        self._configure_styles()

        # Master container for switching views
        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Show Dashboard initially
        self.show_home_screen()

    # -----------------------------------------------------------------------
    # UI Styling
    # -----------------------------------------------------------------------
    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure Treeview table for analytics
        style.configure(
            "Treeview",
            background=self.colors["card"],
            foreground=self.colors["text"],
            rowheight=32,
            fieldbackground=self.colors["card"],
            borderwidth=0,
            font=("Helvetica", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="#ffffff",
            font=("Helvetica", 10, "bold"),
            relief="flat"
        )
        style.map("Treeview", background=[("selected", self.colors["primary"])])

    def _clear_container(self):
        """Destroys all child widgets inside the main container."""
        for widget in self.container.winfo_children():
            widget.destroy()

    # -----------------------------------------------------------------------
    # 1. HOME SCREEN / MAIN MENU
    # -----------------------------------------------------------------------
    def show_home_screen(self):
        self._clear_container()

        # Header card
        header_card = tk.Frame(self.container, bg=self.colors["card"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
        header_card.pack(fill="x", pady=(0, 20), ipady=15)

        title_lbl = tk.Label(
            header_card,
            text="🎓 Smart Quiz & Performance Analyzer",
            font=("Helvetica", 20, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        )
        title_lbl.pack(pady=(10, 4))

        subtitle_lbl = tk.Label(
            header_card,
            text="Interactive Knowledge Assessment with Real-time Diagnostics & Analytics",
            font=("Helvetica", 11),
            fg=self.colors["text_muted"],
            bg=self.colors["card"]
        )
        subtitle_lbl.pack()

        # Navigation Action Grid / Menu Buttons
        menu_frame = tk.Frame(self.container, bg=self.colors["bg"])
        menu_frame.pack(fill="both", expand=True, pady=10)

        # Grid of 4 main menu cards
        options = [
            {
                "title": "1. Start Quiz",
                "desc": "Take the 6-question quiz with negative marking (-0.25) and real-time validation.",
                "color": self.colors["primary"],
                "action": self.start_quiz
            },
            {
                "title": "2. View Last Score",
                "desc": "Inspect your most recent quiz score breakdown, accuracy, and tier classification.",
                "color": "#0ea5e9",
                "action": self.show_last_score_screen
            },
            {
                "title": "3. Performance Analysis",
                "desc": "Explore complete multi-attempt progress, trajectory metrics, and cumulative weak topics.",
                "color": "#8b5cf6",
                "action": self.show_analysis_screen
            },
            {
                "title": "4. Exit Application",
                "desc": "Conclude your study session and exit the program safely.",
                "color": self.colors["danger"],
                "action": self.confirm_exit
            }
        ]

        for i, opt in enumerate(options):
            card = tk.Frame(
                menu_frame,
                bg=self.colors["card"],
                bd=1,
                relief="solid",
                highlightthickness=1,
                highlightbackground=self.colors["card_border"]
            )
            card.grid(row=i // 2, column=i % 2, padx=12, pady=12, sticky="nsew")
            menu_frame.grid_columnconfigure(i % 2, weight=1)
            menu_frame.grid_rowconfigure(i // 2, weight=1)

            t_lbl = tk.Label(card, text=opt["title"], font=("Helvetica", 14, "bold"), fg=opt["color"], bg=self.colors["card"])
            t_lbl.pack(anchor="w", padx=20, pady=(18, 6))

            d_lbl = tk.Label(card, text=opt["desc"], font=("Helvetica", 10), fg=self.colors["text_muted"], bg=self.colors["card"], wraplength=340, justify="left")
            d_lbl.pack(anchor="w", padx=20, pady=(0, 16))

            btn = tk.Button(
                card,
                text="Open →",
                font=("Helvetica", 10, "bold"),
                bg=opt["color"],
                fg="#ffffff",
                activebackground=self.colors["primary_hover"],
                activeforeground="#ffffff",
                relief="flat",
                cursor="hand2",
                command=opt["action"],
                padx=16,
                pady=6
            )
            btn.pack(anchor="w", padx=20, pady=(0, 16))

        # Bottom info bar
        status_bar = tk.Label(
            self.container,
            text=f"Total attempts recorded this session: {len(self.quiz_history)}",
            font=("Helvetica", 10, "italic"),
            fg=self.colors["text_muted"],
            bg=self.colors["bg"]
        )
        status_bar.pack(side="bottom", pady=6)

    # -----------------------------------------------------------------------
    # 2. ACTIVE QUIZ RUNNER
    # -----------------------------------------------------------------------
    def start_quiz(self):
        """Resets active quiz state and displays question 1."""
        self.current_question_index = 0
        self.current_score = 0.0
        self.correct_count = 0
        self.incorrect_count = 0
        self.current_weak_topics = {}
        self.show_question_screen()

    def show_question_screen(self):
        self._clear_container()

        q_data = QUIZ_QUESTIONS[self.current_question_index]
        total_q = len(QUIZ_QUESTIONS)
        self.selected_option_var.set("")

        # Top Bar: Progress & Live Marks Info
        top_bar = tk.Frame(self.container, bg=self.colors["bg"])
        top_bar.pack(fill="x", pady=(0, 10))

        q_counter = tk.Label(
            top_bar,
            text=f"Question {self.current_question_index + 1} of {total_q}",
            font=("Helvetica", 13, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        )
        q_counter.pack(side="left")

        topic_badge = tk.Label(
            top_bar,
            text=f"Topic: {q_data['topic']}",
            font=("Helvetica", 10, "bold"),
            fg="#c7d2fe",
            bg=self.colors["badge_bg"],
            padx=10,
            pady=4
        )
        topic_badge.pack(side="right")

        # Question Card
        card = tk.Frame(
            self.container,
            bg=self.colors["card"],
            bd=1,
            relief="solid",
            highlightbackground=self.colors["card_border"]
        )
        card.pack(fill="both", expand=True, pady=10, padx=2)

        rules_lbl = tk.Label(
            card,
            text="Scoring: Correct answer = +1.00 mark | Incorrect answer = -0.25 mark",
            font=("Helvetica", 9, "italic"),
            fg=self.colors["text_muted"],
            bg=self.colors["card"]
        )
        rules_lbl.pack(anchor="w", padx=25, pady=(15, 8))

        q_text = tk.Label(
            card,
            text=q_data["question"],
            font=("Helvetica", 15, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"],
            wraplength=760,
            justify="left"
        )
        q_text.pack(anchor="w", padx=25, pady=(5, 20))

        # Options Radio Group (A, B, C, D)
        options_frame = tk.Frame(card, bg=self.colors["card"])
        options_frame.pack(fill="x", padx=25, pady=5)

        for opt_key in sorted(q_data["options"].keys()):
            opt_text = f"{opt_key})  {q_data['options'][opt_key]}"

            opt_row = tk.Frame(
                options_frame,
                bg=self.colors["option_bg"],
                bd=1,
                relief="solid",
                highlightbackground=self.colors["card_border"]
            )
            opt_row.pack(fill="x", pady=6)

            rb = tk.Radiobutton(
                opt_row,
                text=opt_text,
                variable=self.selected_option_var,
                value=opt_key,
                font=("Helvetica", 12),
                fg=self.colors["text"],
                bg=self.colors["option_bg"],
                activebackground=self.colors["option_select"],
                activeforeground="#ffffff",
                selectcolor=self.colors["card"],
                anchor="w",
                padx=15,
                pady=10,
                cursor="hand2"
            )
            rb.pack(fill="x")

        # Bottom Button Bar
        btn_bar = tk.Frame(self.container, bg=self.colors["bg"])
        btn_bar.pack(fill="x", pady=(15, 0))

        cancel_btn = tk.Button(
            btn_bar,
            text="← Quit to Menu",
            font=("Helvetica", 10),
            bg=self.colors["card"],
            fg=self.colors["text_muted"],
            relief="flat",
            cursor="hand2",
            command=self.show_home_screen,
            padx=14,
            pady=8
        )
        cancel_btn.pack(side="left")

        submit_btn = tk.Button(
            btn_bar,
            text="Submit Answer →",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["primary"],
            fg="#ffffff",
            activebackground=self.colors["primary_hover"],
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.process_answer,
            padx=22,
            pady=8
        )
        submit_btn.pack(side="right")

    def process_answer(self):
        """Validates choice and calculates score with negative marking."""
        chosen = self.selected_option_var.get().strip().upper()

        # Input Validation: Must choose A, B, C, or D
        if chosen not in ["A", "B", "C", "D"]:
            messagebox.showwarning(
                "Selection Required",
                "Please select an option (A, B, C, or D) before submitting!"
            )
            return

        q_data = QUIZ_QUESTIONS[self.current_question_index]
        correct_answer = q_data["answer"]

        # Check correctness & apply negative marking
        if chosen == correct_answer:
            self.current_score += 1.0
            self.correct_count += 1
            feedback_title = "Correct! (+1.00)"
            feedback_msg = f"Well done! '{chosen}' is the correct choice.\n\nExplanation: {q_data['explanation']}"
            is_correct = True
        else:
            self.current_score -= 0.25
            self.incorrect_count += 1
            feedback_title = "Incorrect (-0.25)"
            feedback_msg = (
                f"Your choice: '{chosen}'\n"
                f"Correct choice: '{correct_answer}'\n\n"
                f"Explanation: {q_data['explanation']}"
            )
            is_correct = False

            # Add to weak area detection
            topic = q_data["topic"]
            if topic not in self.current_weak_topics:
                self.current_weak_topics[topic] = []
            self.current_weak_topics[topic].append(q_data["explanation"])

        # Display instantaneous answer feedback dialog
        if is_correct:
            messagebox.showinfo(feedback_title, feedback_msg)
        else:
            messagebox.showwarning(feedback_title, feedback_msg)

        # Advance to next question or complete quiz
        self.current_question_index += 1
        if self.current_question_index < len(QUIZ_QUESTIONS):
            self.show_question_screen()
        else:
            self.finalize_quiz()

    def finalize_quiz(self):
        """Calculates final scores, categorizes tier, and records attempt."""
        total_questions = len(QUIZ_QUESTIONS)
        max_score = float(total_questions)
        effective_score = max(0.0, self.current_score)
        percentage = round((effective_score / max_score) * 100, 2)
        level, recommendation = classify_performance(percentage)

        attempt_record = {
            "attempt_number": len(self.quiz_history) + 1,
            "raw_score": round(self.current_score, 2),
            "effective_score": round(effective_score, 2),
            "max_score": max_score,
            "percentage": percentage,
            "level": level,
            "recommendation": recommendation,
            "correct_count": self.correct_count,
            "incorrect_count": self.incorrect_count,
            "weak_topics": self.current_weak_topics
        }
        self.quiz_history.append(attempt_record)

        # Show detailed result screen
        self.show_results_screen(attempt_record)

    # -----------------------------------------------------------------------
    # 3. QUIZ RESULTS SCREEN
    # -----------------------------------------------------------------------
    def show_results_screen(self, record):
        self._clear_container()

        # Header
        header = tk.Frame(self.container, bg=self.colors["card"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
        header.pack(fill="x", pady=(0, 15), ipady=12)

        tk.Label(
            header,
            text=f"🎉 Quiz Completed (Attempt #{record['attempt_number']})",
            font=("Helvetica", 18, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(pady=(5, 2))

        # Color-coded tier badge
        tier_color = self.colors["success"] if record["level"] == "Advanced" else (
            self.colors["warning"] if record["level"] == "Intermediate" else self.colors["danger"]
        )
        tier_badge = tk.Label(
            header,
            text=f"Performance Tier: {record['level']} ({record['percentage']:.1f}%)",
            font=("Helvetica", 12, "bold"),
            fg="#ffffff",
            bg=tier_color,
            padx=16,
            pady=4
        )
        tier_badge.pack(pady=6)

        # Stat cards in a row
        stats_frame = tk.Frame(self.container, bg=self.colors["bg"])
        stats_frame.pack(fill="x", pady=10)

        stats = [
            ("Raw Score", f"{record['raw_score']:.2f} / {record['max_score']:.0f}", self.colors["primary"]),
            ("Correct Answers", f"{record['correct_count']} / {int(record['max_score'])}", self.colors["success"]),
            ("Incorrect Answers", f"{record['incorrect_count']} / {int(record['max_score'])}", self.colors["danger"]),
            ("Percentage", f"{record['percentage']:.1f}%", "#0ea5e9")
        ]

        for i, (title, val, col) in enumerate(stats):
            c = tk.Frame(stats_frame, bg=self.colors["card"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
            c.grid(row=0, column=i, padx=6, sticky="nsew")
            stats_frame.grid_columnconfigure(i, weight=1)

            tk.Label(c, text=title, font=("Helvetica", 9), fg=self.colors["text_muted"], bg=self.colors["card"]).pack(pady=(12, 2))
            tk.Label(c, text=val, font=("Helvetica", 15, "bold"), fg=col, bg=self.colors["card"]).pack(pady=(0, 12))

        # Teacher Recommendation & Weak Area Box
        feedback_card = tk.Frame(self.container, bg=self.colors["card"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
        feedback_card.pack(fill="both", expand=True, pady=10, padx=2)

        tk.Label(
            feedback_card,
            text="🎯 Instructor Feedback & Weak Area Diagnostics",
            font=("Helvetica", 12, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(anchor="w", padx=20, pady=(15, 6))

        tk.Label(
            feedback_card,
            text=f"Advice: {record['recommendation']}",
            font=("Helvetica", 10, "italic"),
            fg=self.colors["text_muted"],
            bg=self.colors["card"]
        ).pack(anchor="w", padx=20, pady=(0, 10))

        # Scrollable / list of weak areas
        if not record["weak_topics"]:
            perfect_lbl = tk.Label(
                feedback_card,
                text="🌟 Outstanding! You made zero mistakes across all tested topics.",
                font=("Helvetica", 11, "bold"),
                fg=self.colors["success"],
                bg=self.colors["card"]
            )
            perfect_lbl.pack(anchor="w", padx=20, pady=10)
        else:
            tk.Label(
                feedback_card,
                text="Topics requiring reinforcement:",
                font=("Helvetica", 10, "bold"),
                fg=self.colors["warning"],
                bg=self.colors["card"]
            ).pack(anchor="w", padx=20, pady=(5, 4))

            for topic, explanations in record["weak_topics"].items():
                t_frame = tk.Frame(feedback_card, bg=self.colors["card"])
                t_frame.pack(fill="x", padx=25, pady=3)

                tk.Label(
                    t_frame,
                    text=f"• {topic}:",
                    font=("Helvetica", 10, "bold"),
                    fg=self.colors["text"],
                    bg=self.colors["card"]
                ).pack(anchor="w")

                for exp in explanations:
                    tk.Label(
                        t_frame,
                        text=f"   - Recommendation: {exp}",
                        font=("Helvetica", 9),
                        fg=self.colors["text_muted"],
                        bg=self.colors["card"],
                        wraplength=720,
                        justify="left"
                    ).pack(anchor="w")

        # Bottom Actions
        btn_bar = tk.Frame(self.container, bg=self.colors["bg"])
        btn_bar.pack(fill="x", pady=(12, 0))

        tk.Button(
            btn_bar,
            text="⌂ Main Menu",
            font=("Helvetica", 10),
            bg=self.colors["card"],
            fg=self.colors["text_muted"],
            relief="flat",
            cursor="hand2",
            command=self.show_home_screen,
            padx=16,
            pady=8
        ).pack(side="left")

        tk.Button(
            btn_bar,
            text="📊 View Detailed Analysis",
            font=("Helvetica", 10),
            bg="#8b5cf6",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.show_analysis_screen,
            padx=16,
            pady=8
        ).pack(side="left", padx=10)

        tk.Button(
            btn_bar,
            text="🔄 Retake Quiz",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["primary"],
            fg="#ffffff",
            activebackground=self.colors["primary_hover"],
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.start_quiz,
            padx=20,
            pady=8
        ).pack(side="right")

    # -----------------------------------------------------------------------
    # 4. VIEW LAST SCORE SCREEN
    # -----------------------------------------------------------------------
    def show_last_score_screen(self):
        if not self.quiz_history:
            messagebox.showinfo(
                "No Quiz Taken Yet",
                "You haven't completed any quiz attempts during this session!\nPlease start a quiz first."
            )
            return

        self.show_results_screen(self.quiz_history[-1])

    # -----------------------------------------------------------------------
    # 5. PERFORMANCE ANALYSIS & PROGRESS SCREEN
    # -----------------------------------------------------------------------
    def show_analysis_screen(self):
        if not self.quiz_history:
            messagebox.showinfo(
                "No Analytics Available",
                "No quiz data has been recorded yet.\nTake at least one quiz to view performance analytics."
            )
            return

        self._clear_container()

        # Header
        header = tk.Frame(self.container, bg=self.colors["card"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
        header.pack(fill="x", pady=(0, 15), ipady=10)

        tk.Label(
            header,
            text="📈 Performance Analytics & Session History",
            font=("Helvetica", 18, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(pady=(4, 2))

        # Summary Metrics Strip
        total_attempts = len(self.quiz_history)
        avg_pct = sum(r["percentage"] for r in self.quiz_history) / total_attempts
        best_score = max(r["raw_score"] for r in self.quiz_history)
        latest_pct = self.quiz_history[-1]["percentage"]

        strip = tk.Frame(self.container, bg=self.colors["bg"])
        strip.pack(fill="x", pady=(0, 10))

        metric_data = [
            ("Total Attempts", str(total_attempts), self.colors["primary"]),
            ("Average Score", f"{avg_pct:.1f}%", "#0ea5e9"),
            ("Highest Score", f"{best_score:.2f}", self.colors["success"]),
            ("Latest Score", f"{latest_pct:.1f}%", self.colors["warning"])
        ]

        for i, (title, val, col) in enumerate(metric_data):
            c = tk.Frame(strip, bg=self.colors["card"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
            c.grid(row=0, column=i, padx=5, sticky="nsew")
            strip.grid_columnconfigure(i, weight=1)

            tk.Label(c, text=title, font=("Helvetica", 9), fg=self.colors["text_muted"], bg=self.colors["card"]).pack(pady=(8, 2))
            tk.Label(c, text=val, font=("Helvetica", 14, "bold"), fg=col, bg=self.colors["card"]).pack(pady=(0, 8))

        # Treeview Table for Attempt History
        table_card = tk.Frame(self.container, bg=self.colors["card"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
        table_card.pack(fill="x", pady=6)

        tk.Label(
            table_card,
            text="Attempt-by-Attempt Progress Log",
            font=("Helvetica", 11, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(anchor="w", padx=15, pady=(10, 6))

        columns = ("attempt", "score", "percentage", "tier", "accuracy")
        tree = ttk.Treeview(table_card, columns=columns, show="headings", height=min(6, total_attempts))

        tree.heading("attempt", text="Attempt #")
        tree.heading("score", text="Raw Score")
        tree.heading("percentage", text="Percentage")
        tree.heading("tier", text="Tier Level")
        tree.heading("accuracy", text="Accuracy (Correct/Total)")

        tree.column("attempt", width=90, anchor="center")
        tree.column("score", width=120, anchor="center")
        tree.column("percentage", width=120, anchor="center")
        tree.column("tier", width=140, anchor="center")
        tree.column("accuracy", width=160, anchor="center")

        for r in self.quiz_history:
            tree.insert(
                "",
                "end",
                values=(
                    f"#{r['attempt_number']}",
                    f"{r['raw_score']:.2f} / {r['max_score']:.0f}",
                    f"{r['percentage']:.1f}%",
                    r["level"],
                    f"{r['correct_count']} / {r['correct_count'] + r['incorrect_count']}"
                )
            )

        tree.pack(fill="x", padx=15, pady=(0, 15))

        # Aggregated Weak Areas Section
        weak_agg = {}
        for r in self.quiz_history:
            for t in r["weak_topics"]:
                weak_agg[t] = weak_agg.get(t, 0) + 1

        weak_card = tk.Frame(self.container, bg=self.colors["card"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
        weak_card.pack(fill="both", expand=True, pady=6)

        tk.Label(
            weak_card,
            text="Cumulative Weak Area Diagnosis across All Attempts",
            font=("Helvetica", 11, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(anchor="w", padx=15, pady=(10, 6))

        if not weak_agg:
            tk.Label(
                weak_card,
                text="🌟 Perfect record across all attempts! No weak areas identified.",
                font=("Helvetica", 10),
                fg=self.colors["success"],
                bg=self.colors["card"]
            ).pack(anchor="w", padx=15, pady=8)
        else:
            sorted_weak = sorted(weak_agg.items(), key=lambda x: x[1], reverse=True)
            for topic, count in sorted_weak:
                plural = "attempt" if count == 1 else "attempts"
                row = tk.Frame(weak_card, bg=self.colors["card"])
                row.pack(fill="x", padx=15, pady=2)

                tk.Label(
                    row,
                    text=f"• {topic}:",
                    font=("Helvetica", 10, "bold"),
                    fg=self.colors["warning"],
                    bg=self.colors["card"]
                ).pack(side="left")

                tk.Label(
                    row,
                    text=f" missed in {count} {plural}",
                    font=("Helvetica", 10),
                    fg=self.colors["text_muted"],
                    bg=self.colors["card"]
                ).pack(side="left")

        # Bottom back button
        btn_bar = tk.Frame(self.container, bg=self.colors["bg"])
        btn_bar.pack(fill="x", pady=(10, 0))

        tk.Button(
            btn_bar,
            text="← Back to Menu",
            font=("Helvetica", 10, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            relief="flat",
            cursor="hand2",
            command=self.show_home_screen,
            padx=18,
            pady=8
        ).pack(side="left")

    def confirm_exit(self):
        """Displays exit confirmation dialog."""
        if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit the application?"):
            self.root.destroy()


def launch_gui():
    """Entry point function to launch the Tkinter GUI app."""
    root = tk.Tk()
    app = SmartQuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
