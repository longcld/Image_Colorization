import os
from flask import Flask, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
SAVE_FOLDER = './out'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SAVE_FOLDER'] = SAVE_FOLDER

@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)

            # get path of file
            filenameToResponse = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # processm save file
            file.save(filenameToResponse)
            
            outputFileName = './out/' + filename
            command = 'python demo.py --image ' + filenameToResponse + ' --save ./out/' 
            
            print(command)
            os.system(command)
            # response file to client
            return send_file(outputFileName)
        return False