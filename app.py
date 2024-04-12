import os
from flask import Flask, render_template, request, redirect, url_for
import boto3
import uuid
from botocore.client import Config

app = Flask(__name__)

# En Config, proporcionar signature_version como 's3v4' para usar 'AWS4-HMAC-SHA256' 
region_name = 'eu-central-1'
s3 = boto3.client('s3', config=Config(signature_version='s3v4'), region_name=region_name)

@app.route('/')
def index():
    return render_template('index.html')



import uuid

@app.route('/', methods=['POST'])
def upload_file_to_s3():
    file = request.files['file']
    text_input = request.form['text_input']

    bucket_name = os.environ.get('BUCKET_NAME')
    
    if text_input:
        # Generate a random file name for text inputs
        object_name = str(uuid.uuid4())
        s3.put_object(Body=text_input, Bucket=bucket_name, Key=object_name)
    elif file:
        # Keep original filename for file uploads
        object_name = file.filename
        s3.upload_fileobj(file, bucket_name, object_name)
    else:
        return "No file or text input provided."
    
    # Generate a presigned URL for the S3 object
    
    url = s3.generate_presigned_url('get_object', 
                                    {'Bucket': bucket_name, 'Key': object_name}, 
                                    ExpiresIn = 900)

    # Build the response
    response = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download File</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="my-4">Download Secret</h1>

        <input id="url" type="text" value='""" + url + """' class="form-control" readonly>

        <button onclick="copyToClipboard()" class="btn btn-primary my-4">Copy to Clipboard</button>
        
        <a href="/" class="btn btn-secondary my-4">Clear</a>

        <script>
        function copyToClipboard() {
            var $temp = document.querySelector("#url");
            $temp.select();
            document.execCommand("copy");
        }
        </script>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
