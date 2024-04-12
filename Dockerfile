# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Create a user to run our application
RUN useradd --create-home appuser
USER appuser

# Install Flask and Boto3
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run your application when the container launches
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]