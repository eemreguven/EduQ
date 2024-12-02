import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB limit
app.config['CHARACTER_LIMIT'] = 10000

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def count_characters(file_path, file_type):
    char_count = 0
    if file_type == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            char_count = len(f.read())
    elif file_type == 'pdf':
        reader = PdfReader(file_path)
        char_count = sum(len(page.extract_text()) for page in reader.pages)
    elif file_type in {'doc', 'docx'}:
        doc = Document(file_path)
        char_count = sum(len(paragraph.text) for paragraph in doc.paragraphs)
    return char_count

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            file_type = filename.rsplit('.', 1)[1].lower()
            char_count = count_characters(file_path, file_type)
            
            if char_count > app.config['CHARACTER_LIMIT']:
                flash(f'The file contains {char_count} characters, which exceeds the limit.')
            else:
                flash(f'File uploaded successfully.')
                return redirect(url_for('questions'))
            
            return redirect(url_for('index'))
        else:
            flash('Invalid file type. Only PDF, TXT, DOC, or DOCX allowed.')
            return redirect(request.url)

    return render_template('upload.html')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    question_types = [
        "True/False",
        "Multiple Choice",
        "Fill-in-the-Blank",
        "Scenario-Based",
        "Comparison",
        "Cause and Effect",
        "Argument-Based",
        "Creative Suggestion",
        "Open-Ended Problem Solving"
    ]
    
    if request.method == 'POST':
        # Get form data
        question_count = int(request.form.get('question_count'))
        easy_count = int(request.form.get('easy', 0))
        medium_count = int(request.form.get('medium', 0))
        difficult_count = int(request.form.get('difficult', 0))

        # Backend validation
        errors = []
        if not (0 <= easy_count <= 10):
            errors.append('Easy count must be between 0 and 10.')
        if not (0 <= medium_count <= 10):
            errors.append('Medium count must be between 0 and 10.')
        if not (0 <= difficult_count <= 10):
            errors.append('Difficult count must be between 0 and 10.')
        if (easy_count + medium_count + difficult_count) != question_count:
            errors.append('The sum of easy, medium, and difficult counts must equal the total number of questions.')

        # Display errors or proceed
        if errors:
            for error in errors:
                flash(error)
        else:
            flash('Questions successfully configured.')
            return redirect(url_for('index'))

    return render_template('questions.html', question_types=question_types)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='127.0.0.1', port=5000, debug=True)  # Explicitly setting the host and port
