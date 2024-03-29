from fastapi import FastAPI, File, UploadFile, Form
import os
import shutil
import boto3

app = FastAPI()

#s3 Configuration
s3 = boto3.resource('s3')
bucket = s3.Bucket('final-web-usth')
location = boto3.client('s3').get_bucket_location(Bucket='final-web-usth')['LocationConstraint']

@app.post('/file')
def _file_upload(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer) # save on server 

    with open(file.filename, "rb") as data:
        bucket.upload_fileobj(data,file.filename) #upload to S3
        os.remove(file.filename)

    return {"filename": "https://s3-%s.amazonaws.com/%s/%s" % (location, 'final-web-usth', file.filename)}

