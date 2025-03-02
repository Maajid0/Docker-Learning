# Docker Assignment 🚀

---

# Table of Contents
- [Creating a Simple Web Application](#creating-a-simple-web-application)
- [Containerising the Application](#containerising-the-application)
- [Building and Running the Docker Image](#building-and-running-the-docker-image)
- [Linking Containers Together](#linking-containers-together)
- [Creating a Docker Network and Running MySQL](#creating-a-docker-network-and-running-mysql)
- [Building and Running the Updated Image](#building-and-running-the-updated-image)
- [Debugging with Docker Logs](#debugging-with-docker-logs)
- [Conclusion](#conclusion)

---

# Creating a Simple Web Application

Ensure you have Python installed on your device. You can verify the installation by running:

```sh
python3 --version
```

## Create a directory for your web application and navigate into it:

```sh
mkdir hello_flask && cd hello_flask
```

## Create a file called `app.py` with the following content:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
```

---

# Containerising the application 🐳

## Create a file named Dockerfile in the same directory with the following content:

```Dockerfile
FROM python:3.8-slim    # Uses a lightweight Python 3.8 image.
WORKDIR /app           # Sets the working directory inside the container.
COPY . .               # Copies all files from the current directory to the container.
RUN pip install flask  # Installs Flask in the container.
EXPOSE 5002            # Exposes port 5002 for incoming connections.
CMD ["python", "app.py"]  # Specifies the command to run the application.
```

---

# Building and Running the Docker Image 🏗️

## Build the Docker image by running:

```sh 
docker build -t hello-flask . #. represents the current directory
```

## Run the container with:

```sh
docker run -d -p 5002:5002 hello-flask
```

## To stop the container, run:

```sh
docker stop <container_id>
```

---

# Linking Containers Together 🔗

## Modify your `app.py` to connect to a MySQL database by replacing its content with:

```python 
from flask import Flask
import MySQLdb

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Connect to the MySQL database
    db = MySQLdb.connect(
        host="mydb",           # Hostname of the MySQL container.
        user="root",           # Username for MySQL.
        passwd="my-secret-pw", # Password for the MySQL user.
        db="mysql"             # Name of the database to connect to.
    )
    cur = db.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    return f'Hello, World! MySQL version: {version[0]}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

    # This modification allows your web application to interact with a MySQL container.
```

---

# Creating a Docker Network and Running MySQL 🗃️

## Update your Dockerfile to include the necessary MySQL dependencies:


```Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    pkg-config
RUN pip install flask mysqlclient
EXPOSE 5002
CMD ["python", "app.py"]
```

## Create a custom Docker network to allow the containers to communicate:

```sh
docker network create my-custom-network
```

## Run a MySQL container on this network with:

```sh
docker run -d --name mydb --network my-custom-network -e MYSQL_ROOT_PASSWORD=my-secret-pw mysql:8

# This command pulls MySQL 8 (or 5.7, depending on your machine) from Docker Hub if it is not already available on your machine.
```

---

# Building and Running the Updated Image 🔨

## Build the updated Docker image with:

```sh
docker build -t hello-flask-mysql .
```

## Then, run the updated container and connect it to the custom network:

```sh
docker run -d --name myapp --network my-custom-network -p 5002:5002 hello-flask-mysql
```

---

# Debugging with Docker Logs 🐞

## If you encounter any errors, check the container logs by running:

```sh
docker logs <filename>

# This will display the log output from your application container, helping you to identify any issues.
```

---

# Conclusion 🎉

You have now successfully created a simple Flask web application, containerised it using Docker, and linked it with a MySQL container using a custom Docker network. Now your app is ready to scale! 🌱
