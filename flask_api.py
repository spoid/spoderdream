from __future__ import print_function # In python 2.7
from flask import Flask
import os
from flask import request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
import sys
import caffe

# If your GPU supports CUDA and Caffe was built with CUDA support,
# uncomment the following to run Caffe operations on the GPU.
caffe.set_mode_gpu()
caffe.set_device(0) # select GPU device if multiple devices exist

from deepdreaming import *


UPLOAD_FOLDER = '/home/spoid/deepdream/deepdream/dreams/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPG', 'JPEG'])



def test(path):
    caffe.set_mode_gpu()
    caffe.set_device(0)
    output = output_path()
    
    generate_img(path)
    
    return output

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index')
def index():
    return """
    <html><header></header><body>
    <h1><a href="/upload">Deep Dream Random Generator</a></h1>
    </body></html>
    """
    
    

#<tobi> aus url zeile uebergeben
#@app.route('/a/<tobi>')
#def x2(tobi):
#    return "<html><header></header><body><h1>" + tobi + "</h1></body></html>"
    




#upload shit?

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#random re-run
@app.route('/a/<filename>')
def deepdream(filename):
    output = test(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return """
    <!doctype html>
    <title>All your base are belong to us</title>
    <h1>Here is a random deep dream for """ + filename + """:</h1>
    <img src='""" + url_for('uploaded_file', filename=output.replace("dreams/","")) + """'>
    </br></br>
    <a href="/a/""" + filename + """">Create a new random dream from this image!</a>
    """
    
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #print(file, file=sys.stderr)
            #print(filename, file=sys.stderr)
            
            #print(output, file=sys.stderr)
            
            #return redirect(url_for('uploaded_file',
            #                        filename=output.replace("dreams/","")))
            return redirect("/a/" + filename)
                        
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload a JPG for one random deep dream run!</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    
    


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
from werkzeug import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})



 
    
app.run(debug=True, host='0.0.0.0')

