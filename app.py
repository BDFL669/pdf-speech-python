from flask import Flask, render_template, send_file, send_from_directory
import os
import time
import PyPDF2
from PyPDF2 import PdfReader
from gtts import gTTS
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import psutil
import re as re
from pymongo import MongoClient
import gridfs

URL = 'mongodb+srv://lowa:pdftoaudio@cluster0.ln44kqj.mongodb.net/test'

def mongo_connect():
    try:
        conn = MongoClient(URL, port=5000)
        print("MongoDB Connected!", conn)
        return conn.AudioFiles
    except Exception as err:
        print(f"Error in MongoDB connection: {err}")

client = MongoClient()
db = client.AudioFIles
fs = gridfs.GridFS(db)

mongo_connect()


def upload_file(file_loc, filename, fs):
    with open(file_loc, 'rb') as file_data:
        data = file_data.read()

        #insert audio file in db
        

def delete_file():
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = ''

class UploadFileForm(FlaskForm):
    files = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload PDF")
download = False
filename_reg = ''
file_tag = ''
@app.route('/', methods=['GET',"POST"])
#@app.route('/home', methods=['GET',"POST"])
def home():
    try:
        form = UploadFileForm()
        if form.validate_on_submit():
        #global file
            file = form.files.data # First grab the file
            filename_re = re.sub(r"\s", "_", file.filename)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(filename_re))) # Then save the file
        
        # if file is not empty
            if file is not None:
            #print(file.filename)
                global filename_reg
                filename_reg = re.sub(r"\s", "_", file.filename)
                reader = PdfReader(filename_reg)
                number_of_pages = len(reader.pages)
                global filenoun
                filenoun = file.filename
                page = reader.pages[0]
                text = page.extract_text()
            #print(text)
                os.remove(file.filename)
                global audio_file 
                
                audio_file = f'{filename_reg}.mp3'
                tts = gTTS(text=text, lang='en', tld='co.uk')
                
                directory = ''
                global file_tag
                file_tag = f'{filename_reg}.mp3'
                #upload_file(file_tag, file_tag, fs)
                with open(file_tag, "wb") as f:
                   tts.write_to_fp(f)
                with open(file_tag, "rb") as f:
                    fs.put(f, filename=file_tag)
                    print("Upload Complete")
                #file_tag.close()
                try:
                    #pass
                    #global download
                    #download = True
                    return send_from_directory(directory, f'{filename_reg}.mp3', as_attachment=True)
                finally:
                    pass
                   # if download:
                      #  time.sleep(30)
                      #  os.remove(file_tag)
                    
            
            #return send_file(f"Users/admi/uploading-pdf/Flask-File-Uploads/{file.filename}.mp3")
    finally:
        pass
        
    return render_template('index.html', form=form) 


if __name__ == '__main__':
    app.run(debug=True)
