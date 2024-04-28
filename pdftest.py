from flask import Flask, request, jsonify
import os
import PyPDF2
from docx import Document

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/text-extractor', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        extracted_text = extract_text(filename)
        os.remove(filename)
        return jsonify({'text': extracted_text})

def extract_text(filename):
    extension = filename.split('.')[-1]

    if extension == 'pdf':
        return extract_text_from_pdf(filename)
    elif extension == 'docx':
        return extract_text_from_docx(filename)
    elif extension == 'txt':
        return extract_text_from_txt(filename)
    else:
        return None

def extract_text_from_pdf(filename):
    with open(filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

def extract_text_from_docx(filename):
    doc = Document(filename)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text
def extract_text_from_txt(filename):
    with open(filename, 'r') as txt_file:
        return txt_file.read()

if __name__ == '__main__':
    app.run(debug=True, port=5015)












