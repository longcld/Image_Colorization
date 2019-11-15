import os
from flask import Flask, request, redirect, url_for, send_file, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/out/<path:path>')
def send_js(path):
    return send_from_directory('out', path)

@app.route('/upload', methods=["GET", "POST"])
@cross_origin()
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
            
            name = filename.split('.')[0]
            print(name)
            command = 'python demo.py -i '+ filenameToResponse + ' -s out/'
            os.system(command)

            #print(filenameToResponse)
            # response file to client
            return 'http://localhost:5000/out/' + filename + '_out.png'
        return False