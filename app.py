import os
from flask import Flask, render_template, request, redirect, url_for
import boto3
import uuid
from botocore.client import Config
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

app = Flask(__name__)

def encrypt_text(text, password):
    data = text.encode('utf-8')
    key = password.rjust(32, '0').encode()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct_bytes

def create_presigned_post(s3, bucket_name, object_name, expiration=3600):
    response = s3.generate_presigned_post(Bucket=bucket_name, 
                                          Key=object_name,
                                          Fields={"Content-Type": "application/octet-stream"},
                                          Conditions=[
                                              {"Content-Type": "application/octet-stream"}
                                          ],
                                          ExpiresIn=expiration)
    return response
  
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_text_to_s3():
    region_name = 'eu-central-1'
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'), region_name=region_name)
    bucket_name = 'stacksets-test'

    text_input = request.form['text_input']
    password = request.form['password']
    object_name = str(uuid.uuid4())
    encrypted_text = encrypt_text(text_input, password)

    presigned_post = create_presigned_post(s3, bucket_name, object_name, 900)

    files = {"file": (object_name, encrypted_text)}

    response = requests.post(presigned_post['url'], data=presigned_post['fields'], files=files)

    object_url = f"{presigned_post['url']}/{object_name}"
  
    return object_url, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)