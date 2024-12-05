import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from utils import (    allowed_file,
    count_characters,
    delete_all_files_in_directory,
    validate_questions,
    query_rag,
    run_script,
    create_directory_if_not_exists
)
from constants import PROMPT_TEMPLATE, ALLOWED_EXTENSIONS, CHROMA_PATH, question_types, prompt_templates

# Flask App Configuration
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'rag-system/data'
app.config['DB_FOLDER'] = 'rag-system/chroma'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['CHARACTER_LIMIT'] = 100000


# Flask Routes
@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file uploads."""
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No file selected.')
            return redirect(request.url)

        if allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            delete_all_files_in_directory(app.config['UPLOAD_FOLDER'])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            file_type = filename.rsplit('.', 1)[1].lower()
            char_count = count_characters(file_path, file_type)

            if char_count > app.config['CHARACTER_LIMIT']:
                flash(f'The file contains {char_count} characters, exceeding the limit.')
            else:
                flash('File uploaded successfully.')
                return redirect(url_for('questions'))

        flash('Invalid file type. Only PDF, TXT, DOC, or DOCX are allowed.')
        return redirect(request.url)

    return render_template('upload.html')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    """Handle question generation form."""
    if request.method == 'POST':
        question_data, errors = validate_questions(request.form, question_types)
        if errors:
            for error in errors:
                flash(error)
            return render_template('questions.html', question_types=question_types)

        try:
            generated_questions = generate_questions(question_data)
            for question_tuple in generated_questions:
                flash(f"{question_tuple[0]}: {question_tuple[1]}")
        except Exception as e:
            flash(f"An error occurred while generating questions: {e}")
            return render_template('questions.html', question_types=question_types)
        return redirect(url_for('results'))

    return render_template('questions.html', question_types=question_types)


@app.route('/results', methods=['GET'])
def results():
    """Render the results page."""
    return render_template('results.html')

# Helper Functions
def generate_questions(question_data):
    """Generate questions using the RAG system."""
    # Update the database
    run_script('populate_database.py', cwd='rag-system')

    generated_questions = []
    for item in question_data:
        question_type = item['question_type']
        for difficulty in ['easy', 'medium', 'difficult']:
            count = item[difficulty]
            if count > 0:
                prompt_template = prompt_templates[question_type][difficulty]
                for _ in range(count):
                    question = query_rag(prompt_template, CHROMA_PATH, PROMPT_TEMPLATE)
                    generated_questions.append(
                        (f"{question_type} {difficulty.capitalize()}", question)
                    )
    return generated_questions

# Run the Application
if __name__ == '__main__':
    create_directory_if_not_exists(app.config['UPLOAD_FOLDER'])
    app.run(host='127.0.0.1', port=5000, debug=True)
