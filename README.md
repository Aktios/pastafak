# README

## SecurePaste

SecurePaste is a web application that allows users to upload and retrieve encrypted text from an Amazon S3 bucket. The application uses the Fernet encryption library to encrypt the text before uploading it to S3, and it uses a password-based key derivation function (PBKDF2) to generate a unique encryption key for each user.

## Installation

To get started, follow these steps:

1. Clone the repository:
   
     `git clone https://github.com/Aktios/pastafak.git`

3. Build the Docker image:
   
     `docker build -t my-flask-app:latest .`

4. Replace `bucket-name` with the name of the s3 bucket you want to use.
5. Run the Docker container:
   
     `docker run -d -p 8000:5000 -e BUCKET_NAME=bucket-name --name flask-app-instance my-flask-app:latest`

## Usage

To use SecurePaste, visit the following URL in your web browser:

`http://localhost:8000`

You will be prompted to enter a password. Once you have entered a password, you can upload and retrieve encrypted text.

## Features

* **Encryption:** SecurePaste uses the Fernet encryption library to encrypt the text before uploading it to S3. This ensures that the text is protected from unauthorized access.
* **Password-based key derivation:** SecurePaste uses a password-based key derivation function (PBKDF2) to generate a unique encryption key for each user. This makes it more difficult for attackers to guess the encryption key.
* **Pre-signed URLs:** SecurePaste generates pre-signed URLs that can be used to retrieve the encrypted text from S3. This allows users to share the encrypted text with others without having to give them access to their S3 credentials.

## Security

SecurePaste is a secure application that uses industry-standard encryption algorithms to protect your data. However, it is important to note that no application is completely secure. You should always use a strong password and be careful about who you share your encrypted text with.
