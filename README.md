 DOCKER SETUP
===============
 
Step 1: Prerequisites
--------------

Complete the following prerequisites before you get started with your Flask app.

1.1 — You need an AWS account and must install Docker, the AWS Command Line Interface (CLI) tool and the Lightsail Control (lightsailctl) plugin on your system. Follow the provided links if you don’t have some of those.
Already have an account? Log in to your account

Step 2: Create the Flask application
--------------
Complete the following steps on your local machine that is running Docker. These steps walk you through the process of creating the Flask application files.
### 2.1 — Create a new project directory and switch to that directory.
```commandline
$ mkdir lightsail-containers-flask && cd lightsail-containers-flask
```

### 2.2 — Create a new project directory and switch to that directory with the following code: 

 This minimal Flask application contains a single function hello_world that is triggered when the route “/” is requested. When it runs, this application binds to all IPs on the system (“0.0.0.0”) and listens on port 5000, which is the default Flask port.

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello, World!"

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)

```
### 2.3 — Create a new file, requirements.txt. Edit the file and add the following code. 

Then, save the file.

requirements.txt files are used to specify what Python packages are required by the application. For this minimal Flask application there is only one required package, Flask.
flask===1.1.2
2.4 — Create a new file named Dockerfile. Edit the file and add the following command to it. Save the file.

The Python alpine image ensures the resulting container is as compact and small as possible. The command to run when the container starts is the same as if run from the command line: 
```commandline
python app.py
```

```dockerfile
# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .

# Specify the command to run on container start
CMD [ "python", "./app.py" ]

```

At this point, your directory should contain the following files:

```
$ tree
.
├── app.py
├── Dockerfile
└── requirements.txt
```
0 directories, 3 files

Step 3: Build your container image
--------------
Complete the following steps to build and test the container image locally.
### 3.1 — Build the container using Docker. Execute the following command from the same directory as the Dockerfile:

This command builds a container using the Dockerfile in the current directory and tags the container “flask-container”.
```
$ docker build -t flask-container .
```
### 3.2 —Once the container build is done, test the Flask application locally by running the container.
```
$ docker run -p 5000:5000 flask-container
```
### 3.3 —The Flask app will run in the container and will be exposed to your local system on port 5000. 

Browse to http://localhost:5000 or use curl from the command line and you will see “Hello, World!”.


```
$ curl localhost:5000
```

Hello, World!

Step 4: Create a container service
--------------

Complete the following steps to create the Lightsail container service using the AWS CLI, and then push your local container image to your new container service using the Lightsail control (lightsailctl) plugin.
### 4.1a — Create a Lightsail container service with the create-container-service command.

The power and scale parameters specify the capacity of the container service. For a minimal flask app, little capacity is required.

The output of the create-container-service command indicates the state of the new service is “PENDING”. Refer to the second code block to see this. 
 

### 4.1b — Use the get-container-services command to monitor the state of the container as it is being created. (See third code block)

Wait until the container service state changes to “ACTIVE” before continuing to the next step. Your container service should become active after a few minutes.
```commandline
$ aws lightsail create-container-service --service-name flask-service --power small --scale 1
```
```
{
    "containerService": {
        "containerServiceName": "flask-service",
         ...
        "state": "PENDING",
```
 
### 4.2 —Push the application container to Lightsail with the push-container-image command. 

Note: the X in ":flask-service.flask-container.X" will be a numeric value. If this is the first time you’ve pushed an image to your container service, this number will be 1. You will need this number in the next step.
```commandline
$ aws lightsail push-container-image --service-name flask-service --label flask-container --image flask-container
```

...
Refer to this image as ":flask-service.flask-container.X" in deployments.

Step 5: Deploy the container
--------------

Complete the following steps to create deployment and public endpoint configuration JSON files, and then deploy your container image to your container service.
### 5.1 — Create a new file, containers.json. 

Edit the file and add the following code. 

Replace the X in :flask-service.flask-container.X with the numeric value from the previous step. 

Save the file.

The containers.json file describes the settings of the containers that will be launched on the container service. In this instance, the containers.json file describes the flask container, the image it will use and the port it will expose.

```json
{
    "flask": {
        "image": ":flask-service.flask-container.X",
        "ports": {
            "5000": "HTTP"
        }
    }
}
```
### 5.2 —Create a new file, public-endpoint.json. 

Edit the file and add the following code.

Save the file.

The public-endpoint.json file describes the settings of the public endpoint for the container service. In this instance, the public-endpoint.json file indicates the flask container will expose port 5000. Public endpoint settings are only required for services that require public access.
After creating containers.json and public-endpoint.json files, your project directory should look like the second code block.
```json
{
    "containerName": "flask",
    "containerPort": 5000
}
```
```commandline
$ tree
.
├── app.py
├── containers.json
├── Dockerfile
├── public-endpoint.json
└── requirements.txt

0 directories, 5 files
```

### 5.3 — Deploy the container to the container service with the AWS CLI using the create-container-service-deployment command.

The output of the create-container-servicedeployment command indicates that the state of the container service is now “DEPLOYING”. As shown in the second code block.
```commandline
$ aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json

{
    "containerServices": [{
        "containerServiceName": "flask-service",
         ...
        "state": "DEPLOYING",
```
### 5.4 — Use the get-container-services command to monitor the state of the container until it changes to “RUNNING” before continuing to the next step.

The get-container-service command also returns the endpoint URL for container service.
```commandline
$ aws lightsail get-container-services --service-name flask-service
{
    "containerServices": [{
        "containerServiceName": "flask-service",
         ...
        "state": "RUNNING",
         ...
        "url": "https://flask-service...
```
### 5.5 —After the container service state changes to “RUNNING”, which typically takes a few minutes, navigate to this URL in your browser to verify your container service is running properly. Your browser output should show “Hello, World!” as before.

Congratulations. You have successfully deployed a containerized Flask application using Amazon Lightsail containers.

Step 6: Cleanup
------

Complete the following steps to the Lightsail container service that you created as part of this tutorial.
### 6.1 —To cleanup and delete Lightsail resources, use the delete-container-service command.

The delete-container-service removes the container service, any associated container deployments, and container images.
```terminal
$ aws lightsail delete-container-service --service-name flask-service
```