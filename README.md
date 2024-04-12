# README

## Installation

To get started, follow these steps:

1. Clone the repository:
   
     `bash git clone https://github.com/Aktios/pastafak.git`

3. Build the Docker image:
   
     `bash docker build -t my-flask-app:latest .`

4. Replace `bucket-name` with the name of the s3 bucket you want to use.
5. Run the Docker container:
   
     `bash docker run -d -p 8000:5000 -e BUCKET_NAME=bucket-name --name flask-app-instance my-flask-app:latest`
