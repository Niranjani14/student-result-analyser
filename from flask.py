from flask import Flask, render_template, request
import json

app = Flask(__name__)

def calculate_grade(percentage, pass_fail):
    if pass_fail == "Fail":
        return "F"
    if percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B"
    elif percentage >= 60: return "C"
    elif percentage >= 50: return "D"
    else: return "F"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        
        # Parse subject marks
        subjects = {
            'Math': float(request.form.get('math')),
            'Science': float(request.form.get('science')),
            'English': float(request.form.get('english')),
            'History': float(request.form.get('history')),
            'CS': float(request.form.get('cs'))
        }
        
        # Calculations
        total_marks = sum(subjects.values())
        max_marks = len(subjects) * 100
        percentage = round((total_marks / max_marks) * 100, 2)
        
        # Pass/Fail Status (Assuming 40 is passing for each subject)
        pass_fail = "Pass" if all(mark >= 40 for mark in subjects.values()) else "Fail"
        grade = calculate_grade(percentage, pass_fail)
        
        # Smart Analytics
        strongest_subject = max(subjects, key=subjects.get)
        weakest_subject = min(subjects, key=subjects.get)
        
        if pass_fail == "Pass":
            recommendation = f"Excellent work overall! You are dominating in {strongest_subject}. To push your grade higher, dedicate a bit more study time to {weakest_subject}."
        else:
            recommendation = f"Don't get discouraged. Focus heavily on {weakest_subject} to reach a passing grade, and keep up the good effort in {strongest_subject}."

        # Prepare data for dashboard
        student_data = {
            'name': name,
            'roll_no': roll_no,
            'total': total_marks,
            'percentage': percentage,
            'grade': grade,
            'status': pass_fail,
            'strongest': strongest_subject,
            'weakest': weakest_subject,
            'recommendation': recommendation,
            'subject_names': list(subjects.keys()),
            'subject_scores': list(subjects.values())
        }
        
        return render_template('index.html', data=student_data)
        
    return render_template('index.html', data=None)

if __name__ == '__main__':
    app.run(debug=True)