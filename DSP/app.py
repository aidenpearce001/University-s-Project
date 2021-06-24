from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import steganography 
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route('/')
def upload_file():
   return render_template('uploads.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def process():
   if request.method == 'POST':
      data = {}

      print(request.form)
      print("receive")
      f = request.files['file']
      print(f.filename)
      if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

      lsb = int(request.form['lsb'])
      if request.form['lsb'] == "":
         lsb = 2

      if request.form['method'] == 'encode':
         with open("secret.txt","w") as f:
            f.write(request.form['secret'])
         status, num_lsb, max_bytes_to_hide, file_size, hide_time = steganography.encode(os.path.join(app.config['UPLOAD_FOLDER'],filename),"secret.txt",os.path.join(app.config['UPLOAD_FOLDER'],"secret.wav"),lsb)
         data['status'] = status
         data['number of lsb'] = num_lsb
         data['Total bytes can hide'] = str(max_bytes_to_hide) + " bytes"
         data['Total'] = str(file_size) + " bytes hidden" + hide_time

      elif request.form['method'] == 'decode':
         status, bytes_to_recover, rec_time = steganography.decode(os.path.join(app.config['UPLOAD_FOLDER'],filename),"output.txt",lsb,1000)
         f = open("output.txt",'r+')
         # print(f.read())
         secret = f.read().rstrip('\x00')
         print({'decode' : 'secret is '+ str(f.read())})

         data['status'] = status
         data['recover'] = str(bytes_to_recover) + rec_time 
         data['The Secret is'] = secret

   print(data)
   print(filename)
   return render_template('audio.html',data = data, audiofile= filename)

if __name__ == '__main__':
   app.run(port=45000,debug = True)