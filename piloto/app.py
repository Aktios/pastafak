import os
from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import uuid
from botocore.client import Config
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import requests

app = Flask(__name__)
app.secret_key = 'clavesecreta'  # Cambia por tu secreta clave

region_name = 'eu-central-1'
s3 = boto3.client('s3', config=Config(signature_version='s3v4'), region_name=region_name)

def generate_key(password: str, salt=None):
    if salt is None:
        salt = os.urandom(16)
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return salt, key

@app.route('/', methods=['GET', 'POST'])
def upload_text_to_s3():
    url = ""  # Se inicializa 'url' como un string vacío.
    if request.method == 'POST':
        text_input = request.form['text_input']
        password = request.form['password']
        bucket_name = os.environ.get('BUCKET_NAME')

        if not text_input:
            return "No text input provided."

        salt, key = generate_key(password)
        cipher_suite = Fernet(key)
        encrypted_text = cipher_suite.encrypt(text_input.encode())

        object_name = str(uuid.uuid4())
        s3.put_object(Body=salt + encrypted_text, Bucket=bucket_name, Key=object_name)

        url = s3.generate_presigned_url('get_object',
                                         Params={'Bucket': bucket_name, 'Key': object_name},
                                         ExpiresIn=900)
        
        return render_template('get.html', url=url)

    return render_template('upload.html')


@app.route('/get', methods=['GET', 'POST'])
def get_secret():
    if request.method == 'POST':
        if 'url_input' in request.form and 'password' in request.form:
            url = request.form['url_input']
            password = request.form['password']

            response = requests.get(url)
            encrypted_content = response.content
            salt = encrypted_content[:16]
            encrypted_text = encrypted_content[16:]
            
            _, key = generate_key(password, salt)
            cipher_suite = Fernet(key)
            
            try:
                plain_text = cipher_suite.decrypt(encrypted_text).decode()
                flash('Este es su secreto descifrado: {}'.format(plain_text))
            except:
                flash('Invalid Token or Password')
                
            return redirect(request.url)

    return render_template('get.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)