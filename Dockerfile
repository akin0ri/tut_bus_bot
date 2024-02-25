# select python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /workspace
ENV FLASK_APP=app

# Copy requirements file
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
