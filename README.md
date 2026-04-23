# AcadPredict 🎓

AcadPredict is a Flask-based Academic Performance Prediction System designed to help educators and students leverage data-driven insights to predict and optimize academic outcomes. 

## Features

- **User Authentication:** Secure login and registration using `flask-login` and `werkzeug` password hashing.
- **Student Profiling:** Add multiple students with their college year, age, enrollment details, and attendance percentages.
- **Year-wise Subject Specialization:** Dynamic subject lists tailored to each college year based on the **GGSIPU B.Tech syllabus**, covering specialized topics from Year 1 to Year 4.
- **Machine Learning Integration:** Uses `scikit-learn`'s Linear Regression model to predict a student's final score based on their mid-sem performance, practical marks, and attendance.
- **Grades and Diagnostics:** Automatically calculates cumulative grades and indicates failed subjects to identify areas that need improvement.
- **Accordion Dashboard:** A sleek, year-wise grouped dashboard with collapsible sections (accordions) for a cleaner overview of students.
- **Real-time Search & Filter:** Filter the student list instantly across all years; relevant year sections automatically expand when matches are found.
- **Enhanced CSV Export:** Generate year-wise separated performance reports with simplified subject-wise total marks.

## Project Structure

- `app.py`: The main Flask application entry point, routing, and controller logic.
- `database.py`: SQLAlchemy database models defining `User`, `Student`, and `SubjectRecord`.
- `model.py`: Scikit-learn data generation, training, saving `trained_model.pkl` & `scaler.pkl`, and prediction functions.
- `templates/`: HTML structures using Jinja2 for dynamic rendering (Dashboard, Views, Auth pages).
- `static/`: Custom sleek CSS styling matching the project aesthetics.

## Tech Stack

- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn, NumPy
- **Database:** SQLite, Flask-SQLAlchemy
- **Frontend:** HTML5, CSS3, Jinja2

## Getting Started

### Prerequisites

Ensure you have Python 3 installed. Start by installing the necessary dependencies from the `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Running the Application

To initialize the database locally and start the web server, run:

```bash
python3 app.py
```

The application will be hosted locally at `http://127.0.0.1:5000/`.

> **Note:** The application automatically generates an `admin` user with the password `admin123` upon its first run if the account doesn't exist, and subsequently trains/loads the underlying predictive models locally.

## License
MIT License. Feel free to explore and modify!
