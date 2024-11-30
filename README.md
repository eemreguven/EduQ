
# EduQ - Quiz Generator

EduQ is a web-based application designed to streamline the creation of quizzes. Users can upload files (PDFs, DOCX, or TXT) and configure the number of questions for each difficulty level (Easy, Medium, Difficult) and question type. The application provides an intuitive interface and dynamic validation to ensure accurate configuration.

## Features
- Upload files (PDF, DOCX, TXT) up to **1MB**.
- Dynamically configure quiz questions by difficulty levels: Easy, Medium, and Difficult.
- Real-time validation of input values to ensure consistency.
- Submit button activation only when the total is valid (1-10).
- Responsive and user-friendly design.

## Requirements
The project requires the following Python packages to work:
- `Flask`
- `Flask-WTF`
- `WTForms`
- `python-docx`
- `PyPDF2`
- `lxml`

You can install all dependencies using the provided `requirements.txt` file.

## Installation, Usage, and Commands
```bash

# Install required Python packages
pip install -r requirements.txt

# Run the Flask application
python app.py

# Open your browser and navigate to:
http://127.0.0.1:5000/

# Interact with the application:
# - Upload a file using the "Choose a File" button.
# - Configure quiz questions by setting the number of Easy, Medium, and Difficult questions for each question type.
# - Ensure your inputs are valid (total between 1-10) to activate the Submit button.

# Stop the Flask application
# Press Ctrl+C in the terminal to stop the server.
