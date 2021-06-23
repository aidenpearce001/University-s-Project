from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import steganography 
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route('/')
def upload_file():
   return render_template('uploads.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def process():
   if request.method == 'POST':
      print("receive")
      f = request.files['file']
      print(f.filename)
      if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

      return f.filename
      # data = {
      #       "method" : request.form['method'],
      # }

      # print(request.form)
      # f = request.files['file']
      # if f:
      #       filename = secure_filename(f.filename)
      #       f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

      # if request.form['method'] == 'encode':
      #    with open("secret.txt","w") as f:
      #       f.write(request.form['secret'])
      #    steganography.encode(os.path.join(app.config['UPLOAD_FOLDER'],filename),"secret.txt",os.path.join(app.config['UPLOAD_FOLDER'],"secret.wav"),2)

      #    os.remove("secret.txt")

      #    return jsonify({'encode' : 'encrypted'})

      # elif request.form['method'] == 'decode':
      #    steganography.decode(os.path.join(app.config['UPLOAD_FOLDER'],filename),"output.txt",2,1000)
      #    f = open("output.txt",'r+')
      #    # print(f.read())
      #    secret = f.read().rstrip('\x00')
      #    print({'decode' : 'secret is '+ str(f.read())})
      #    return jsonify({'decode' : 'secret is '+ secret})

      #    os.remove("output.txt")
		

if __name__ == '__main__':
   app.run(port=45000,debug = True)