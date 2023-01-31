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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = ''

class UploadFileForm(FlaskForm):
    files = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload PDF")
#download = False
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
            filename_re = re.sub(r"[\s]", "_", file.filename)
            #filename_re = re.sub(r"[\(\)]", "", filename_re)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(filename_re))) # Then save the file
        
        # if file is not empty
            if file is not None:
                path = os.getcwd()
                audios = os.listdir(path)

                mp3_files = [audio for audio in audios if audio.endswith('.mp3')]

                if mp3_files:
                    for audio in mp3_files:
                        os.remove(os.path.join(path, audio))
                        print('Deleted', len(mp3_files), 'mp3 file(s).')
                    else:
                        print('No mp3 files found.')
            #print(file.filename)
                global filename_reg
                filename_reg = re.sub(r"[\s]", "_", file.filename)
                filename_reg = re.sub(r"[\(\)]", "", filename_reg)
                reader = PdfReader(filename_reg)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
    
    # Extract the text from the page
                    text = page.extract_text()
            #print(text)
                os.remove(filename_reg)
                global audio_file 
                
                audio_file = f'{filename_reg}.mp3'
                tts = gTTS(text=text, lang='en', tld='co.uk')
                
                directory = ''
                global file_tag
                file_tag = f'{filename_reg}.mp3'
                #upload_file(file_tag, file_tag, fs)
                with open(file_tag, "wb") as f:
                   tts.write_to_fp(f)
                   f.close()                
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
    app.run(host='0.0.0.0', port=5000, debug=True)
