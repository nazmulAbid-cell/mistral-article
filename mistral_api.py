from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import PyPDF2
from docx import Document
from preprocess.pre_processing import preprocess_text

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/generate_response', methods=['GET'])
def receive_json():
    try:
        article_text = request.form['user_input']
    except KeyError:
        return jsonify("Error: Please enter article text"), 400

    # article_text = "Behind the Desk: Why Your Employee Could Be Your Risky Bet! Did you ever heard about Insider Risk? in today's digital world, companies are aware and ready for variety range of cybersecurity risks, like Malware attack, Distributed denial of service (DDoS), zero day vulnerabilities or any kind of cybersecurity attacks. although if you noticed these are list of well-recognized external threats. but most of companies are forgetting to add the insider risk in the list of Cybersecurity risks, it's important to not overlook risk posed by insiders within the organization. Insider risks, combines both intentional and unintentional actions done by empoyee, contractor or other party, that’s effect organization people, data or resources negatively. So typically, Insider Risk: a risk raised by employee, contractor, or other party to negatively affect organization people, data or resources, either by intentional or unintentional actions. Why its matter? You may ask why insider risk is matter, lets me give a short store about insider risk at Airline Company, Pegasus Airline left 23 million files containing personal data exposed online after an employee improperly configured a database. The incident was reported in June 2022 after the Turkish airline discovered the error. But I’m sure that you now that the store did not end here, as a consequence of this accident, company lost millions of dollars, brand awareness, customer lose trust in the brand, paid a fine for non-compliance with IT requirements, stalled data, etc. What are the different types of insider threats? The different type of insider threats is primarily based on individuals' roles and responsibilities. current employees, former employee, covert agents (moles). Every type of the above has a distinct motivation for attacking, such stealing sensitive data or valuable data for financial gain, sabotaging, or damaging as a form of revenge or personal gain, steal trade secret to limit a company competitive advantage, etc. Recognizing these people is must for organizations to implement strong security measures, monitor activities, and mitigate the risks created by insider threats. Note that not all insider threats are malicious, it could be an accident, but this accident may case a significant risk. What are the warning signs that could indicate an insider threat? Why is access control important for insider threat? To effectively control insider risks, Access control is crucial part. with some principle like, Role-based access control, that insure everyone have just permission aligned with their department and work responsibilities. least-privilege access, employees are restricted from accessing the network to only what they need to carry out for their responsibilities. zero trust security, verifies identities even within the network, to limit user and devices access. Therefore, reducing potential damage from insider threats. With time the effect of insiders’ threats are increasing from the side of cost and also the consequences of this event, as evidence se the fowling chart. total average cost of insider threats incidents, What are the consequences of barely manage insider risks? The consequences of a race but the most popular are financial loses, loss of intellectual property, reputational losses, operational destruction. In conclusion, organizations must remain alert in determining and mitigating insider risks, as these threats can arise from trusted individuals and have dangerous consequences. Effective management and security measures are must to deal with these threats successfully"

    preprocessed_text = preprocess_text(article_text)
    print('Preprocessed text: ' + preprocessed_text)

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    data= {"model": "mistral", "prompt": f"You will be provided with article text delimited by triple quotes create a presentation content with the following format: 1- Create a title for this article, based on the content of the text. 2- Summarize the following text and create bullet points (these points can be either pointers or numbering or a paragraph depending on the content). 3- Create a tagline for the text. 4- Determine the article type (tech, health, business, marketing, etc.). 5- Calculate the number of slides. 6- Output a JSON object that contains the following keys: Title, slide_1 Content, slide_2 Content, slide_n Content, tagline, article_type, slide_number and the value of each key will be with in string. If the text does not contain an article to make a presentation from, then simply write No content provided. Use the following format: Title: ‹title to be generated› slide_1 Content: <summary> slide_2 Content: <slide 2 Content bullet points> slide_n Content: <slide_n Content bullet points> tagline: <tagline> article_type: <article-type> Slides_Number: <Slides_Number> Output JSON: <JSON with summary Title, slide_1 Content, slide_2 Content, slide_n Content, tagline, article_type, slide_number> Please note that slide_1 Content, slide_2 Content, slide_n Content is in sequence of numbers, so based on the content provided, assume what is the best number of slides and fill every slide with different content. Slides should be like this: slide1, slide2, slide3, slide4, slide5, etc. And you could assume that slide_1 Content: is the title, slide_2 Content: is bullet points with the title of the bullet point, slide_3 Content: numbering points with the title of the numbering, slide_n Content: this point can be either pointers or numbering or a paragraph depending on the content. The slide before the last slide should be: Conclusion, and the last slide should be:form the aritical text'''article_text= {preprocessed_text}'''","stream": False}

    response = requests.post('http://localhost:11434/api/generate', headers=headers, data=json.dumps(data))

    json_response = response.json()
    print(json_response['response'])

    return jsonify(json_response['response'])


@app.route('/generate_response_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        article_text = extract_text(filename)
        preprocessed_text = preprocess_text(article_text)
        print('Preprocessed text: ' + preprocessed_text)

        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        data= {"model": "mistral", "prompt": f"You will be provided with article text delimited by triple quotes create a presentation content with the following format: 1- Create a title for this article, based on the content of the text. 2- Summarize the following text and create bullet points (these points can be either pointers or numbering or a paragraph depending on the content). 3- Create a tagline for the text. 4- Determine the article type (tech, health, business, marketing, etc.). 5- Calculate the number of slides. 6- Output a JSON object that contains the following keys: Title, slide_1 Content, slide_2 Content, slide_n Content, tagline, article_type, slide_number and the value of each key will be with in string. If the text does not contain an article to make a presentation from, then simply write No content provided. Use the following format: Title: ‹title to be generated› slide_1 Content: <summary> slide_2 Content: <slide 2 Content bullet points> slide_n Content: <slide_n Content bullet points> tagline: <tagline> article_type: <article-type> Slides_Number: <Slides_Number> Output JSON: <JSON with summary Title, slide_1 Content, slide_2 Content, slide_n Content, tagline, article_type, slide_number> Please note that slide_1 Content, slide_2 Content, slide_n Content is in sequence of numbers, so based on the content provided, assume what is the best number of slides and fill every slide with different content. Slides should be like this: slide1, slide2, slide3, slide4, slide5, etc. And you could assume that slide_1 Content: is the title, slide_2 Content: is bullet points with the title of the bullet point, slide_3 Content: numbering points with the title of the numbering, slide_n Content: this point can be either pointers or numbering or a paragraph depending on the content. The slide before the last slide should be: Conclusion, and the last slide should be:form the aritical text'''article_text= {preprocessed_text}'''","stream": False}

        response = requests.post('http://localhost:11434/api/generate', headers=headers, data=json.dumps(data))

        json_response = response.json()
        print(json_response['response'])

        
        os.remove(filename)
        return jsonify(json_response['response'])

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
    app.run(debug=True,port=5015)







