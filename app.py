from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, User, Student, SubjectRecord
from model import predict_score, calculate_grade, train_model

app = Flask(__name__)
app.secret_key = 'academic_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view    = 'login'
login_manager.login_message = 'Please log in first.'

SUBJECTS = ['Mathematics', 'Physics', 'Chemistry',
            'Computer Science', 'English', 'Electronics']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ── Index ──────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('login'))

# ── Login ──────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'].strip()).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Welcome back! 👋', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

# ── Register ───────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if request.form['confirm_password'] != password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return render_template('register.html')
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# ── Logout ─────────────────────────────────────────────────────
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

# ── Student Info ───────────────────────────────────────────────
@app.route('/student-info', methods=['GET', 'POST'])
@login_required
def student_info():
    if request.method == 'POST':
        enroll = request.form['enrollment_number'].strip()
        if Student.query.filter_by(enrollment_number=enroll).first():
            flash('Enrollment number already exists!', 'danger')
            return render_template('student_info.html')
        s = Student(
            name                  = request.form['name'].strip(),
            enrollment_number     = enroll,
            college_year          = int(request.form['college_year']),
            age                   = int(request.form['age']),
            attendance_percentage = float(request.form['attendance_percentage'])
        )
        db.session.add(s)
        db.session.commit()
        session['student_id'] = s.id
        flash(f'Student {s.name} added! Now enter marks.', 'success')
        return redirect(url_for('subject_entry'))
    return render_template('student_info.html')

# ── Subject Entry ──────────────────────────────────────────────
@app.route('/subject-entry', methods=['GET', 'POST'])
@login_required
def subject_entry():
    sid = session.get('student_id')
    if not sid:
        flash('Enter student info first.', 'warning')
        return redirect(url_for('student_info'))
    student = Student.query.get_or_404(sid)
    if request.method == 'POST':
        SubjectRecord.query.filter_by(student_id=student.id).delete()
        for subj in SUBJECTS:
            mid1      = float(request.form.get(f'{subj}_mid1', 0))
            mid2      = float(request.form.get(f'{subj}_mid2', 0))
            practical = float(request.form.get(f'{subj}_practical', 0))
            total     = mid1 + mid2 + practical
            db.session.add(SubjectRecord(
                student_id      = student.id,
                subject_name    = subj,
                mid_sem1_marks  = mid1,
                mid_sem2_marks  = mid2,
                practical_marks = practical,
                total_marks     = total,
                is_failed       = total < 44,
                predicted_score = predict_score(mid1, mid2, practical,
                                                student.attendance_percentage)
            ))
        db.session.commit()
        flash('Marks saved! Prediction complete 🎯', 'success')
        return redirect(url_for('results', student_id=student.id))
    return render_template('subject_entry.html', student=student, subjects=SUBJECTS)

# ── Dashboard ──────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.all()
    stats = []
    for s in students:
        recs    = SubjectRecord.query.filter_by(student_id=s.id).all()
        failed  = sum(1 for r in recs if r.is_failed)
        avg     = sum(r.total_marks for r in recs)/len(recs) if recs else 0
        stats.append({'student': s, 'failed_count': failed,
                       'avg_total': round(avg,1),
                       'grade': calculate_grade(avg) if recs else '-'})
    return render_template('dashboard.html', stats=stats)

# ── Detailed Report ──────────────────────────────────────────────
@app.route('/detailed-report')
@login_required
def detailed_report():
    students = Student.query.all()
    report_data = []
    for s in students:
        recs = SubjectRecord.query.filter_by(student_id=s.id).all()
        if not recs:
            continue
        avg_mid1 = sum(r.mid_sem1_marks for r in recs) / len(recs)
        avg_mid2 = sum(r.mid_sem2_marks for r in recs) / len(recs)
        avg_practical = sum(r.practical_marks for r in recs) / len(recs)
        failed = sum(1 for r in recs if r.is_failed)
        overall_pred = predict_score(avg_mid1, avg_mid2, avg_practical, s.attendance_percentage)
        
        report_data.append({
            'student': s,
            'avg_mid1': round(avg_mid1, 1),
            'avg_mid2': round(avg_mid2, 1),
            'avg_practical': round(avg_practical, 1),
            'failed_count': failed,
            'overall_pred': overall_pred
        })
    return render_template('detailed_report.html', report_data=report_data)

# ── Results ────────────────────────────────────────────────────
@app.route('/results/<int:student_id>')
@login_required
def results(student_id):
    student = Student.query.get_or_404(student_id)
    records = SubjectRecord.query.filter_by(student_id=student_id).all()
    data = [{'subject': r.subject_name, 'mid1': r.mid_sem1_marks,
              'mid2': r.mid_sem2_marks, 'practical': r.practical_marks,
              'total': r.total_marks, 'predicted': r.predicted_score,
              'grade': calculate_grade(r.total_marks), 'failed': r.is_failed}
             for r in records]
    overall = sum(d['total'] for d in data)/len(data) if data else 0
    return render_template('results.html', student=student, subject_data=data,
                           failed_subjects=[d['subject'] for d in data if d['failed']],
                           overall_avg=round(overall,1),
                           overall_grade=calculate_grade(overall) if data else '-')

# ── Delete ─────────────────────────────────────────────────────
@app.route('/delete-student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    s = Student.query.get_or_404(student_id)
    db.session.delete(s)
    db.session.commit()
    flash(f'{s.name} deleted.', 'info')
    return redirect(url_for('dashboard'))

# ── Run ────────────────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            a = User(username='admin')
            a.set_password('admin123')
            db.session.add(a)
            db.session.commit()
            print("✅ Admin created — user: admin | pass: admin123")
        train_model()
    app.run(debug=True, port=5000)