from flask import Flask, render_template_string, request
import json

app = Flask(__name__)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Student Result Analyser</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-slate-100 min-h-screen font-sans text-slate-800 p-6">

    <div class="max-w-4xl mx-auto">
        <header class="text-center mb-10">
            <h1 class="text-4xl font-bold text-indigo-600 mb-2">Smart Student Result Analyser</h1>
            <p class="text-slate-500">Generate insights and visual analytics from student performance.</p>
        </header>

        {% if not data %}
        <div class="bg-white rounded-xl shadow-lg p-8 max-w-2xl mx-auto">
            <h2 class="text-2xl font-semibold mb-6 border-b pb-2">Enter Student Details</h2>
            <form method="POST" action="/">
                <div class="grid grid-cols-2 gap-4 mb-6">
                    <div>
                        <label class="block text-sm font-medium mb-1">Student Name</label>
                        <input type="text" name="name" required class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Roll Number</label>
                        <input type="text" name="roll_no" required class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                </div>

                <h3 class="font-medium text-lg mb-4">Subject Marks (out of 100)</h3>
                <div class="grid grid-cols-2 gap-4 mb-8">
                    <div>
                        <label class="block text-sm font-medium mb-1">Mathematics</label>
                        <input type="number" name="math" min="0" max="100" required class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Science</label>
                        <input type="number" name="science" min="0" max="100" required class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">English</label>
                        <input type="number" name="english" min="0" max="100" required class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">History</label>
                        <input type="number" name="history" min="0" max="100" required class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Computer Science</label>
                        <input type="number" name="cs" min="0" max="100" required class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none">
                    </div>
                </div>

                <button type="submit" class="w-full bg-indigo-600 text-white font-semibold py-3 rounded-lg hover:bg-indigo-700 transition duration-200">
                    Analyze Performance
                </button>
            </form>
        </div>

        {% else %}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="space-y-6">
                <div class="bg-white rounded-xl shadow-lg p-6 border-t-4 border-indigo-600">
                    <h2 class="text-2xl font-bold">{{ data.name }}</h2>
                    <p class="text-slate-500 mb-4">Roll No: {{ data.roll_no }}</p>
                    <div class="grid grid-cols-2 gap-4 text-center">
                        <div class="bg-slate-50 p-3 rounded-lg">
                            <p class="text-sm text-slate-500">Total Marks</p>
                            <p class="text-xl font-bold text-indigo-600">{{ data.total }} <span class="text-sm">/ 500</span></p>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-lg">
                            <p class="text-sm text-slate-500">Percentage</p>
                            <p class="text-xl font-bold text-indigo-600">{{ data.percentage }}%</p>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-lg">
                            <p class="text-sm text-slate-500">Grade</p>
                            <p class="text-xl font-bold text-indigo-600">{{ data.grade }}</p>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-lg">
                            <p class="text-sm text-slate-500">Status</p>
                            <p class="text-xl font-bold {% if data.status == 'Pass' %} text-green-600 {% else %} text-red-600 {% endif %}">{{ data.status }}</p>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-lg p-6">
                    <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
                        <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                        Smart Analytics
                    </h3>
                    <div class="mb-4">
                        <p><strong>Strongest Subject:</strong> <span class="text-green-600">{{ data.strongest }}</span></p>
                        <p><strong>Weakest Subject:</strong> <span class="text-red-600">{{ data.weakest }}</span></p>
                    </div>
                    <div class="bg-indigo-50 p-4 rounded-lg text-sm text-indigo-900 border border-indigo-100">
                        <strong>Recommendation:</strong> {{ data.recommendation }}
                    </div>
                </div>
                
                <a href="/" class="inline-block bg-slate-200 text-slate-700 font-semibold py-2 px-4 rounded-lg hover:bg-slate-300 transition">Analyze Another Student</a>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6 flex flex-col justify-center items-center">
                <h3 class="text-lg font-semibold mb-4 self-start">Performance Radar</h3>
                <div class="w-full max-w-md">
                    <canvas id="performanceChart"></canvas>
                </div>
            </div>
        </div>

        <script>
            // Injecting Jinja data into JS safely
            const subjectNames = {{ data.subject_names | tojson | safe }};
            const subjectScores = {{ data.subject_scores | tojson | safe }};

            const ctx = document.getElementById('performanceChart').getContext('2d');
            new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: subjectNames,
                    datasets: [{
                        label: 'Subject Marks',
                        data: subjectScores,
                        backgroundColor: 'rgba(79, 70, 229, 0.2)',
                        borderColor: 'rgba(79, 70, 229, 1)',
                        pointBackgroundColor: 'rgba(79, 70, 229, 1)',
                        borderWidth: 2,
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                            grid: { color: 'rgba(0, 0, 0, 0.1)' },
                            pointLabels: {
                                font: { size: 14, family: "'Inter', sans-serif" }
                            },
                            ticks: {
                                beginAtZero: true,
                                max: 100,
                                stepSize: 20
                            }
                        }
                    }
                }
            });
        </script>
        {% endif %}
    </div>

</body>
</html>
"""
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
        
        # Pass the data into our HTML string
        return render_template_string(HTML_TEMPLATE, data=student_data)
        
    # Render empty form if GET request
    return render_template_string(HTML_TEMPLATE, data=None)

if __name__ == '__main__':
    app.run(debug=True)