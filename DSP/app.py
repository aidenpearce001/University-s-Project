from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import wave
import steganography 

app = Flask(__name__)

@app.route('/')
def upload_file():
   return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def process():
   if request.method == 'POST':
      print(request.form)
      # data = request.json
      f = request.files['file']
      f.save(secure_filename(secure_filename(f.filename)))

      # if data['method'] == 'encode':
      #    pass
      # elif data['method'] == 'decode':
      #    pass
      # else:
      #    return 'something not right'

   return request.json
        # if request.form['submit_button'] == 'Do Something':
        #     pass # do something
        # elif request.form['submit_button'] == 'Do Something Else':
        #     pass # do something else
        # else:
        #     pass # unknown
   # if request.method == 'POST':
   #    f = request.files['file']
   #    f.save(secure_filename(f.filename))
   #    steganography.encode("demo.wav","untitled.txt","testing.wav",2)
   #    return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(port=45000,debug = True)