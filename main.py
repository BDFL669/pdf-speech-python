from flask import Flask, render_template, send_file, send_from_directory
import os
import PyPDF2
from PyPDF2 import PdfReader
from gtts import gTTS
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = ''

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
file_download = 'no'
@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        
        # if file is not empty
        if file is not None:
            #print(file.filename)
            reader = PdfReader(file.filename)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            text = page.extract_text()
            #print(text)
            tts = gTTS(text=text, lang='en', tld='co.uk')
            tts.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{file.filename}.mp3"))) # Then save the file
            file_download = 'yes'
            directory = ''
            return send_from_directory(directory, f'{file.filename}.mp3', as_attachment=True)
            #return send_file(f"Users/admi/uploading-pdf/Flask-File-Uploads/{file.filename}.mp3")
    return render_template('index.html', form=form)
def download_mp3():
    if file_download == 'yes':
        print(file_download) 

if __name__ == '__main__':
    app.run(debug=True)