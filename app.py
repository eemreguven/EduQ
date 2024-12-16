import os
from flask import (
    Flask, render_template, request, jsonify, url_for,
    redirect, flash, send_from_directory
)
from progress import progress_data
from methods import (
    clear_folder,
    reset_database,
    validate_questions,
    generate_questions,
    handle_file_upload,
    handle_youtube_upload,
)
from constants import (
    CHROMA_FOLDER_PATH,
    DOWNLOAD_FOLDER_PATH,
    UPLOAD_FOLDER_PATH,
    question_types
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    """
    Render the home page.
    """
    return render_template('index.html')

@app.route('/progress')
def progress():
    """
    Provide real-time progress updates as JSON.
    """
    return jsonify(progress_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Handle file or YouTube URL uploads.

    - GET: Clear upload folder, reset database, and render upload form.
    - POST: Process file uploads or YouTube URLs.
    """
    if request.method == 'GET':
        clear_folder(UPLOAD_FOLDER_PATH)
        reset_database()
        progress_data["status"] = "idle"
        return render_template('upload.html')

    if request.method == 'POST':
        try:
            resource_type = request.form.get('resourceType')

            if resource_type == 'file':
                progress_data["status"] = "Processing file..."
                response = handle_file_upload(request.files.get('file'))
                progress_data["status"] = "File processing completed."
                return response

            elif resource_type == 'youtube':
                progress_data["status"] = "Extracting text from YouTube video..."
                response = handle_youtube_upload(request.form.get('youtubeUrl'))
                progress_data["status"] = "Text extraction from YouTube video completed."
                return response

            return jsonify({'error': 'Invalid resource type. Supported types: file, youtube.'}), 400
        except Exception as e:
            progress_data["status"] = "Error occurred during processing."
            print(f"Error in /upload route: {str(e)}")
            return jsonify({'error': 'An unexpected server error occurred.'}), 500

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    """
    Handle question generation based on user input.

    - GET: Render the question input form.
    - POST: Validate input, generate questions, and return JSON response.
    """
    if request.method == 'GET':
        return render_template('questions.html', question_types=question_types)

    if request.method == 'POST':
        try:
            progress_data["status"] = "Validating input..."
            question_data, errors = validate_questions(request.form)
            if errors:
                progress_data["status"] = "Validation errors."
                return jsonify({"success": False, "errors": errors}), 400

            progress_data["status"] = "Generating questions..."
            filename = generate_questions(question_data)
            progress_data["status"] = "Questions generated successfully."

            return jsonify({
                "success": True,
                "redirect_url": url_for('results', filename=filename)
            })

        except Exception as e:
            progress_data["status"] = "Error during question generation."
            print(f"Error in /questions route: {str(e)}")
            return jsonify({
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }), 500

@app.route('/results', methods=['GET'])
def results():
    """
    Render the results page with a download link for the generated file.
    Redirect to the questions page if no file is found.
    """
    filename = request.args.get('filename')
    if not filename:
        flash("No file found to download.")
        return redirect(url_for('questions'))
    return render_template('results.html', filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    """
    Allow users to download the generated .docx file.
    """
    return send_from_directory(
        DOWNLOAD_FOLDER_PATH,
        filename,
        as_attachment=True
    )

if __name__ == '__main__':
    if os.path.exists(UPLOAD_FOLDER_PATH):
        clear_folder(UPLOAD_FOLDER_PATH)
    else:
        os.makedirs(UPLOAD_FOLDER_PATH, exist_ok=True)

    if os.path.exists(CHROMA_FOLDER_PATH):
        reset_database()
    else:
        os.makedirs(CHROMA_FOLDER_PATH, exist_ok=True)

    app.run(host='127.0.0.1', port=5000, debug=True)
