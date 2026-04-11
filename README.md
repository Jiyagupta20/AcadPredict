# AcadPredict 🎓

AcadPredict is a Flask-based Academic Performance Prediction System designed to help educators and students leverage data-driven insights to predict and optimize academic outcomes. 

## Features

- **User Authentication:** Secure login and registration using `flask-login` and `werkzeug` password hashing.
- **Student Profiling:** Add multiple students with their college year, age, enrollment details, and attendance percentages.
- **Performance Tracking:** Enter mid-semester and practical marks across a consolidated list of 6 key subjects (Mathematics, Physics, Chemistry, Computer Science, English, Electronics), unified across all academic years for simplicity.
- **Machine Learning Integration:** Uses `scikit-learn`'s Linear Regression model to predict a student's final score based on their mid-sem performance, practical marks, and attendance.
- **Grades and Diagnostics:** Automatically calculates cumulative grades and indicates failed subjects to identify areas that need improvement.
- **Real-time Search:** Filter the student list instantly on the dashboard using the built-in search bar.
- **CSV Data Export:** Generate and download comprehensive performance records for all students with a single click.
- **Comprehensive Dashboard:** A consolidated view representing statistics across all registered students, now with instant filtering.

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
