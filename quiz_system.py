"""
=============================================================================
             SMART QUIZ & PERFORMANCE ANALYZER SYSTEM
=============================================================================
Author: Python Instructor
Description: A beginner-friendly, modular, console-based quiz application
             featuring input validation, negative marking, weak area detection,
             performance tier classification, and multi-attempt tracking.
=============================================================================
"""

# ---------------------------------------------------------------------------
# 1. QUESTION BANK
# ---------------------------------------------------------------------------
# Each question is represented as a dictionary containing:
# - 'question': The question text
# - 'options': A dictionary of possible options (A, B, C, D)
# - 'answer': The correct option key ('A', 'B', 'C', or 'D')
# - 'topic': The subject matter topic (used for weak area analysis)
# - 'explanation': Helpful feedback explaining the correct answer
# ---------------------------------------------------------------------------
QUIZ_QUESTIONS = [
    {
        "question": "What is the output of bool('False') in Python?",
        "options": {
            "A": "False",
            "B": "True",
            "C": "None",
            "D": "ValueError"
        },
        "answer": "B",
        "topic": "Data Types & Booleans",
        "explanation": "Any non-empty string in Python evaluates to True in a boolean context."
    },
    {
        "question": "Which of the following data structures is immutable?",
        "options": {
            "A": "List",
            "B": "Dictionary",
            "C": "Tuple",
            "D": "Set"
        },
        "answer": "C",
        "topic": "Data Structures",
        "explanation": "Tuples cannot be modified after creation, making them immutable."
    },
    {
        "question": "What keyword is used to handle exceptions in Python?",
        "options": {
            "A": "catch",
            "B": "except",
            "C": "rescue",
            "D": "try_catch"
        },
        "answer": "B",
        "topic": "Exception Handling",
        "explanation": "Python uses 'try' and 'except' blocks to gracefully handle runtime exceptions."
    },
    {
        "question": "Which statement terminates the current loop immediately?",
        "options": {
            "A": "pass",
            "B": "continue",
            "C": "break",
            "D": "return"
        },
        "answer": "C",
        "topic": "Control Flow & Loops",
        "explanation": "'break' exits the enclosing loop entirely, skipping any remaining iterations."
    },
    {
        "question": "What is the default return value of a Python function that lacks a return statement?",
        "options": {
            "A": "0",
            "B": "False",
            "C": "Empty string ('')",
            "D": "None"
        },
        "answer": "D",
        "topic": "Functions & Scope",
        "explanation": "Functions without an explicit return statement implicitly return None."
    },
    {
        "question": "What does the expression 3 * [1, 2] evaluate to?",
        "options": {
            "A": "[3, 6]",
            "B": "[[1, 2], [1, 2], [1, 2]]",
            "C": "[1, 2, 1, 2, 1, 2]",
            "D": "TypeError"
        },
        "answer": "C",
        "topic": "Lists & Operations",
        "explanation": "Multiplying a list by an integer duplicates its elements into a single list."
    }
]


# ---------------------------------------------------------------------------
# 2. HELPER UTILITY FUNCTIONS
# ---------------------------------------------------------------------------

def display_banner(title):
    """Prints a styled decorative header banner."""
    separator = "=" * 60
    print(f"\n{separator}")
    print(f" {title.center(58)} ")
    print(f"{separator}")


def get_validated_choice(prompt, valid_options):
    """
    Prompts the user repeatedly until a valid choice is provided.
    - Trims whitespace
    - Converts input to uppercase (case-insensitive)
    - Validates against allowed options
    """
    valid_set = {opt.upper() for opt in valid_options}
    
    while True:
        user_input = input(prompt).strip().upper()
        if user_input in valid_set:
            return user_input
        print(f"  [!] Invalid input '{user_input}'. Please choose from: {', '.join(sorted(valid_set))}")


def classify_performance(percentage):
    """
    Categorizes the user's score based on their percentage:
    - Beginner: < 50%
    - Intermediate: 50% to 79%
    - Advanced: >= 80%
    """
    if percentage >= 80.0:
        return "Advanced", "Outstanding mastery! You have a solid grasp of core concepts."
    elif percentage >= 50.0:
        return "Intermediate", "Good effort! Review the identified weak spots to reach advanced level."
    else:
        return "Beginner", "Needs improvement. Focus on fundamental concepts and try again."


# ---------------------------------------------------------------------------
# 3. CORE QUIZ ENGINE
# ---------------------------------------------------------------------------

def run_quiz(questions, quiz_history):
    """
    Executes a complete quiz session:
    1. Iterates through each question.
    2. Enforces input validation (A, B, C, D).
    3. Applies negative marking (+1.0 for correct, -0.25 for incorrect).
    4. Identifies weak areas / missed topics with feedback.
    5. Calculates score and performance tier.
    6. Appends attempt metadata to session history.
    """
    display_banner(f"STARTING QUIZ (Attempt #{len(quiz_history) + 1})")
    print("Guidelines:")
    print("  - Each correct answer awards:  +1.00 mark")
    print("  - Each incorrect answer deducts: -0.25 mark")
    print("  - Valid options for each question: A, B, C, or D\n")

    score = 0.0
    correct_count = 0
    incorrect_count = 0
    weak_topics = {}  # topic -> list of explanation strings for questions missed

    total_questions = len(questions)

    for index, q in enumerate(questions, start=1):
        print(f"------------------------------------------------------------")
        print(f"Question {index} of {total_questions} | Topic: [{q['topic']}]")
        print(f"{q['question']}")
        for opt_key in sorted(q["options"].keys()):
            print(f"   {opt_key}) {q['options'][opt_key]}")

        # Input validation: Accepts only A, B, C, or D (case-insensitive)
        user_choice = get_validated_choice("Your answer (A/B/C/D): ", ["A", "B", "C", "D"])

        # Check answer & apply negative marking
        if user_choice == q["answer"]:
            score += 1.0
            correct_count += 1
            print("   -> Correct! (+1.00 mark)\n")
        else:
            score -= 0.25
            incorrect_count += 1
            print(f"   -> Incorrect! (-0.25 mark) | Correct answer was: {q['answer']}")
            print(f"      Note: {q['explanation']}\n")
            
            # Record missed topic for personalized feedback
            topic = q["topic"]
            if topic not in weak_topics:
                weak_topics[topic] = []
            weak_topics[topic].append(q["explanation"])

    # Prevent negative overall percentages
    effective_score = max(0.0, score)
    max_score = float(total_questions)
    percentage = round((effective_score / max_score) * 100, 2)
    level, recommendation = classify_performance(percentage)

    # Compile attempt record
    attempt_record = {
        "attempt_number": len(quiz_history) + 1,
        "raw_score": round(score, 2),
        "effective_score": round(effective_score, 2),
        "max_score": max_score,
        "percentage": percentage,
        "level": level,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "weak_topics": weak_topics
    }
    quiz_history.append(attempt_record)

    # Display instant post-quiz summary
    display_banner("QUIZ SUMMARY & RESULTS")
    print(f"  Attempt Number    : #{attempt_record['attempt_number']}")
    print(f"  Correct Answers   : {correct_count} / {total_questions}")
    print(f"  Incorrect Answers : {incorrect_count} / {total_questions}")
    print(f"  Final Score       : {score:.2f} / {max_score:.2f} (with -0.25 negative marking)")
    print(f"  Percentage        : {percentage:.2f}%")
    print(f"  Performance Tier  : [{level}]")
    print(f"  Recommendation    : {recommendation}")

    # Personalized Feedback & Weak Area Detection
    print("\n--- Personalized Topic Feedback ---")
    if not weak_topics:
        print("  Terrific! You answered every question correctly across all topics!")
    else:
        print("  Mistakes detected in the following topic(s):")
        for topic, explanations in weak_topics.items():
            print(f"\n  * Topic: {topic}")
            for exp in explanations:
                print(f"    - Tip: {exp}")
    print("------------------------------------------------------------\n")


# ---------------------------------------------------------------------------
# 4. VIEW LAST SCORE
# ---------------------------------------------------------------------------

def view_last_score(quiz_history):
    """Displays the metrics and result of the most recently taken quiz."""
    display_banner("LAST QUIZ SCORE")
    
    if not quiz_history:
        print("  No quiz attempts found in this session yet.")
        print("  Please select Option 1 from the main menu to take a quiz first!\n")
        return

    last_attempt = quiz_history[-1]
    print(f"  Attempt Number    : #{last_attempt['attempt_number']}")
    print(f"  Correct Answers   : {last_attempt['correct_count']} questions")
    print(f"  Incorrect Answers : {last_attempt['incorrect_count']} questions")
    print(f"  Raw Score         : {last_attempt['raw_score']:.2f} / {last_attempt['max_score']:.2f}")
    print(f"  Percentage        : {last_attempt['percentage']:.2f}%")
    print(f"  Performance Tier  : {last_attempt['level']}")
    
    if last_attempt["weak_topics"]:
        weak_list = ", ".join(last_attempt["weak_topics"].keys())
        print(f"  Topics to Review  : {weak_list}")
    else:
        print("  Topics to Review  : None (Perfect Score!)")
    print()


# ---------------------------------------------------------------------------
# 5. PERFORMANCE ANALYSIS & PROGRESS TRACKING
# ---------------------------------------------------------------------------

def performance_analysis(quiz_history):
    """
    Provides comprehensive multi-attempt analysis:
    - Tabular summary of all attempts
    - Score trajectory and statistical summary
    - Aggregated weak topic frequency across all attempts
    """
    display_banner("PERFORMANCE ANALYSIS & HISTORY")

    if not quiz_history:
        print("  No quiz data available for analysis.")
        print("  Take at least one quiz to view performance metrics.\n")
        return

    # 1. Multi-Attempt History Table
    print("Attempt History Overview:")
    header = f"{'Attempt':<10} | {'Score':<10} | {'Percentage':<12} | {'Level':<14} | {'Accuracy':<10}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    scores = []
    percentages = []
    all_weak_topics_count = {}

    for record in quiz_history:
        att = f"#{record['attempt_number']}"
        scr = f"{record['raw_score']:.2f}/{record['max_score']:.0f}"
        pct = f"{record['percentage']:.2f}%"
        lvl = record["level"]
        acc = f"{record['correct_count']}/{record['correct_count'] + record['incorrect_count']}"
        print(f"{att:<10} | {scr:<10} | {pct:<12} | {lvl:<14} | {acc:<10}")

        scores.append(record["raw_score"])
        percentages.append(record["percentage"])

        # Aggregate weak topics count
        for topic in record["weak_topics"]:
            all_weak_topics_count[topic] = all_weak_topics_count.get(topic, 0) + 1

    print("-" * len(header))

    # 2. Statistical Progress
    total_attempts = len(quiz_history)
    avg_percentage = sum(percentages) / total_attempts
    highest_score = max(scores)
    latest_percentage = percentages[-1]

    print("\nSession Progress Metrics:")
    print(f"  * Total Attempts Completed : {total_attempts}")
    print(f"  * Average Percentage       : {avg_percentage:.2f}%")
    print(f"  * Highest Raw Score        : {highest_score:.2f}")

    if total_attempts > 1:
        first_pct = percentages[0]
        diff = latest_percentage - first_pct
        trend = "improved" if diff > 0 else ("declined" if diff < 0 else "remained consistent")
        print(f"  * Trajectory               : Your score has {trend} by {abs(diff):.2f}% from Attempt #1 to #{total_attempts}.")
    else:
        print("  * Trajectory               : Complete more attempts to unlock improvement trends!")

    # 3. Aggregated Weak Area Report
    print("\nCumulative Weak Area Diagnosis:")
    if not all_weak_topics_count:
        print("  Flawless record! No weak areas detected across any attempts.")
    else:
        print("  Topics requiring extra practice (ranked by error frequency):")
        # Sort topics descending by frequency of mistakes
        sorted_weak = sorted(all_weak_topics_count.items(), key=lambda item: item[1], reverse=True)
        for topic, count in sorted_weak:
            plural = "attempt" if count == 1 else "attempts"
            print(f"    - {topic}: missed in {count} {plural}")
    print()


# ---------------------------------------------------------------------------
# 6. MAIN MENU & CONTROLLER
# ---------------------------------------------------------------------------

def display_menu():
    """Renders the main system menu."""
    print("============================================================")
    print("        SMART QUIZ & PERFORMANCE ANALYZER SYSTEM           ")
    print("============================================================")
    print("  1. Start Quiz")
    print("  2. View Last Score")
    print("  3. Performance Analysis")
    print("  4. Exit")
    print("============================================================")


def main():
    """
    Main controller loop running the menu-driven system.
    Persists attempt history across the runtime session.
    """
    # In-memory history list tracking all quiz attempts during the session
    quiz_history = []

    print("\nWelcome to the Smart Quiz & Performance Analyzer System!")
    print("Designed to evaluate, diagnose, and elevate your Python skills.\n")

    while True:
        display_menu()
        choice = get_validated_choice("Enter your choice (1-4): ", ["1", "2", "3", "4"])

        if choice == "1":
            run_quiz(QUIZ_QUESTIONS, quiz_history)
        elif choice == "2":
            view_last_score(quiz_history)
        elif choice == "3":
            performance_analysis(quiz_history)
        elif choice == "4":
            display_banner("THANK YOU FOR LEARNING!")
            print("  You have exited the Smart Quiz System.")
            print("  Keep practicing and refining your Python mastery!\n")
            break


# ---------------------------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
