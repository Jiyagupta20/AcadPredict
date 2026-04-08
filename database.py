from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(db.Model):
    __tablename__          = 'students'
    id                     = db.Column(db.Integer, primary_key=True)
    name                   = db.Column(db.String(100), nullable=False)
    enrollment_number      = db.Column(db.String(30), unique=True, nullable=False)
    college_year           = db.Column(db.Integer, nullable=False)
    age                    = db.Column(db.Integer, nullable=False)
    attendance_percentage  = db.Column(db.Float, default=0.0)
    subjects               = db.relationship('SubjectRecord', backref='student',
                                              lazy=True, cascade='all, delete-orphan')


class SubjectRecord(db.Model):
    __tablename__    = 'subject_records'
    id               = db.Column(db.Integer, primary_key=True)
    student_id       = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_name     = db.Column(db.String(100), nullable=False)
    mid_sem1_marks   = db.Column(db.Float, default=0.0)
    mid_sem2_marks   = db.Column(db.Float, default=0.0)
    practical_marks  = db.Column(db.Float, default=0.0)
    total_marks      = db.Column(db.Float, default=0.0)
    is_failed        = db.Column(db.Boolean, default=False)
    predicted_score  = db.Column(db.Float, default=0.0)