import sys
import traceback
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    # Allow the app to run without crashing if matplotlib is not installed
    MATPLOTLIB_AVAILABLE = False

def calculate_grade(percentage, pass_fail):
    if pass_fail == "Fail": return "F"
    if percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B"
    elif percentage >= 60: return "C"
    elif percentage >= 50: return "D"
    else: return "F"

def analyze_performance():
    try:
        name = name_entry.get()
        roll = roll_entry.get()
        
        if not name or not roll:
            messagebox.showerror("Input Error", "Please enter Name and Roll Number.")
            return
        subjects = {
            'English': float(eng_entry.get()),
            'Science': float(sci_entry.get()),
            'Maths': float(math_entry.get()),
            'Physics': float(physics_entry.get()),
            'CS': float(cs_entry.get())
        }
        
        for mark in subjects.values():
            if mark < 0 or mark > 100:
                messagebox.showerror("Input Error", "Marks must be between 0 and 100.")
                return
        total_marks = sum(subjects.values())
        percentage = round((total_marks / 500) * 100, 2)
        pass_fail = "Pass" if all(mark >= 40 for mark in subjects.values()) else "Fail"
        grade = calculate_grade(percentage, pass_fail)
        
        strongest = max(subjects.items(), key=lambda item: item[1])[0]
        weakest = min(subjects.items(), key=lambda item: item[1])[0]

        if pass_fail == "Pass":
            rec = f"Excellent! Keep dominating in {strongest}.\nFocus a bit more on {weakest}."
        else:
            rec = f"Focus heavily on {weakest} to pass.\nKeep up the effort in {strongest}."
        lbl_result_name.config(text=f"Student: {name} ({roll})")
        lbl_result_total.config(text=f"Total: {total_marks} / 500")
        lbl_result_perc.config(text=f"Percentage: {percentage}%")
        lbl_result_grade.config(text=f"Grade: {grade}")
        lbl_result_status.config(text=f"Status: {pass_fail}", fg="green" if pass_fail=="Pass" else "red")
        lbl_result_ai.config(text=f"Strongest: {strongest} | Weakest: {weakest}\n{rec}")
        draw_chart(list(subjects.keys()), list(subjects.values()))

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all subjects.")

def draw_chart(subjects, scores):
    for widget in chart_frame.winfo_children():
        widget.destroy()

    if not MATPLOTLIB_AVAILABLE:
        tk.Label(
            chart_frame,
            text="Chart unavailable: install matplotlib in the selected interpreter.",
            font=("Helvetica", 10),
            bg="white",
            fg="red"
        ).pack(pady=20)
        return

    
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    
    ax.bar(subjects, scores, color="#46e583")
    ax.set_ylim(0, 100)
    ax.set_ylabel('Marks')
    ax.set_title('Subject Performance')
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
def create_root_window():
    try:
        return tk.Tk()
    except Exception:
        error_details = traceback.format_exc()
        print("Failed to initialize the GUI window:\n")
        print(error_details)
        input("Press Enter to close...")
        sys.exit(1)


root = create_root_window()
root.title("Smart Student Result Analyser")
root.geometry("950x650")
root.configure(bg="#f9f7f1")

TITLE_FONT = ("Helvetica", 16, "bold")
LABEL_FONT = ("Helvetica", 11)
left_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
left_frame.place(x=20, y=20, width=350, height=600)

right_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
right_frame.place(x=390, y=20, width=540, height=600)
tk.Label(left_frame, text="Enter Student Details", font=TITLE_FONT, bg="white").pack(pady=(0, 15))
def create_input(parent, text):
    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="x", pady=5)
    tk.Label(frame, text=text, font=LABEL_FONT, bg="white", width=12, anchor="w").pack(side="left")
    entry = tk.Entry(frame, font=LABEL_FONT)
    entry.pack(side="right", expand=True, fill="x")
    return entry

name_entry = create_input(left_frame, "Name:")
roll_entry = create_input(left_frame, "Roll No:")

tk.Label(left_frame, text="Marks (out of 100)", font=("Helvetica", 12, "bold"), bg="white").pack(pady=(15, 5))

math_entry = create_input(left_frame, "Math:")
sci_entry = create_input(left_frame, "Science:")
eng_entry = create_input(left_frame, "English:")
physics_entry = create_input(left_frame, "Physics:")
cs_entry = create_input(left_frame, "Comp Sci:")

btn_analyze = tk.Button(left_frame, text="Analyze Performance", font=("Helvetica", 12, "bold"), 
                        bg="#eda200", fg="white", command=analyze_performance)
btn_analyze.pack(pady=20, fill="x")
tk.Label(right_frame, text="Performance Dashboard", font=TITLE_FONT, bg="white").pack(pady=(0, 10))

lbl_result_name = tk.Label(right_frame, text="Student: --", font=("Helvetica", 12, "bold"), bg="white", wraplength=400, justify="left")
lbl_result_name.pack(pady=5)

info_frame = tk.Frame(right_frame, bg="white")
info_frame.pack(pady=10, padx=10, fill="x")

lbl_result_total = tk.Label(info_frame, text="Total: --", font=LABEL_FONT, bg="white", width=20, wraplength=180, justify="left")
lbl_result_total.grid(row=0, column=0, padx=5, pady=5, sticky="w")
lbl_result_perc = tk.Label(info_frame, text="Percentage: --", font=LABEL_FONT, bg="white", width=20, wraplength=180, justify="left")
lbl_result_perc.grid(row=0, column=1, padx=5, pady=5, sticky="w")
lbl_result_grade = tk.Label(info_frame, text="Grade: --", font=LABEL_FONT, bg="white", width=20, wraplength=180, justify="left")
lbl_result_grade.grid(row=1, column=0, padx=5, pady=5, sticky="w")
lbl_result_status = tk.Label(info_frame, text="Status: --", font=LABEL_FONT, bg="white", width=20, wraplength=180, justify="left")
lbl_result_status.grid(row=1, column=1, padx=5, pady=5, sticky="w")

lbl_result_ai = tk.Label(right_frame, text="Insights will appear here.", font=("Helvetica", 10, "italic"), bg="#e0e7ff", pady=10, wraplength=400, justify="left")
lbl_result_ai.pack(fill="x", pady=10, padx=5)
chart_frame = tk.Frame(right_frame, bg="white")
chart_frame.pack(fill="both", expand=True, pady=10)

if __name__ == "__main__":
    try:
        root.mainloop()
    except Exception:
        error_details = traceback.format_exc()
        print("Application crashed with an unexpected error:\n")
        print(error_details)
        input("Press Enter to close...")
