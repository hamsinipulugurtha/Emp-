from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling the file upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        file_path = 'uploads/' + filename
        file.save(file_path)
        
        # Run the Python program with the uploaded video file
        subprocess.run(['python', 'process_video.py', file_path])
        
        return 'File uploaded and processed successfully'
    
    return 'Error uploading file'

if __name__ == '__main__':
    app.run()
