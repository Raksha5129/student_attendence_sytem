from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    date TEXT,
                    status TEXT,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_student.html', title="Add Student")

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    
    if request.method == 'POST':
        today = str(date.today())
        for student in students:
            status = request.form.get(f'status_{student[0]}')
            c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                      (student[0], today, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('mark_attendance.html', students=students, title="Mark Attendance")

@app.route('/view_attendance')
def view_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT students.name, attendance.date, attendance.status 
                 FROM attendance 
                 JOIN students ON students.id = attendance.student_id
                 ORDER BY attendance.date DESC''')
    records = c.fetchall()
    conn.close()
    return render_template('view_attendance.html', records=records, title="View Attendance")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
