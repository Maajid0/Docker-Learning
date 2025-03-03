# Basic Multi-Container Docker Application: Flask Web App + MySQL 🐳

This project demonstrates how to use **Docker Compose** to create a multi-container application with a **Flask** web app and a **MySQL** database. The goal of this setup is to show how to configure and run multiple Docker containers using a simple `docker-compose.yml` file.

## Overview 🚀

The application is a basic Flask web app that connects to a MySQL database container. When the Flask app runs, it connects to the MySQL database, retrieves the MySQL version, and displays it alongside a "Hello, World!" message.

## Application Components ⚙️

1. **Flask Web App** (`app.py`): A simple Python web app using Flask that connects to the MySQL database.
2. **MySQL Database**: A MySQL database running in a Docker container.
3. **Docker Compose** (`docker-compose.yml`): Used to configure and run both the web app and MySQL database in separate containers.
4. **Dockerfile**: A file used to create the Docker image for the Flask app.

## Code Breakdown 💻

### 1. `app.py` - Flask Web Application 🌐

This is the basic Flask app that connects to the MySQL database.

```python
from flask import Flask
import MySQLdb

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Connect to the MySQL database
    db = MySQLdb.connect(
        host="mydb",    # Hostname of the MySQL container
        user="root",    # Username to connect to MySQL
        passwd="my-secret-pw",  # Password for the MySQL user
        db="mysql"      # Name of the database to connect to
    )
    cur = db.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    return f'Hello, World! MySQL version: {version[0]}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
```

- This app connects to the MySQL container using the hostname mydb, as defined in the Docker Compose file.
- It runs a query to fetch the MySQL version and displays the result along with a "Hello, World!" message.

### 2. `Dockerfile` - Building the Web App Image 🏗️

The Dockerfile is used to build the Docker image for the Flask app. It installs dependencies and configures the environment to run the app.

```dockerfile
# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    pkg-config

# Install Python dependencies
RUN pip install flask mysqlclient

# Expose port 5002 for the Flask app
EXPOSE 5002

# Run the Flask app when the container starts
CMD ["python", "app.py"]
```

### 3. `docker-compose.yml` - Defining the Multi-Container Setup 📝

The `docker-compose.yml` file defines both the Flask web app and the MySQL database as services and handles the orchestration of the two containers.

```yaml
version: '3'

services:
  web:
    build:
      context: .
    ports:
      - "5002:5002"
    depends_on:
      - db
    environment:
      - FLASK_APP=app.py
      - FLASK_RUN_HOST=0.0.0.0
    networks:
      - app_network

  db:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
      MYSQL_DATABASE: mysql
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - app_network

volumes:
  db-data:

networks:
  app_network:
    driver: bridge
```

- `web`: The Flask app service is built using the `Dockerfile` in the current directory.
    - The app listens on port `5002`.
    - It depends on the `db` service (MySQL), ensuring the database container is started before the web app.
    - The environment variables set `FLASK_APP` and `FLASK_RUN_HOST`.
- `db`: The MySQL database service uses the latest official MySQL image.
    - It sets the root password and initialises a `mysql` database.
    - Data is persisted using the `db-data` volume.
- `depends_on`: Ensures the Flask app waits for the MySQL container to be ready before starting.
- `networks`: Both services are connected to the `app_network` network, allowing them to communicate with each other.

### 4. Running the Application 🏃‍♂️

To run the multi-container application, follow these steps:

1. Build and start the containers: 
    
Run the following command to build the Docker images and start both the Flask web app and the MySQL database:

```bash
docker-compose up -d
```

This will:

- Build the Flask app image using the `Dockerfile`.
- Start both the Flask app container and the MySQL container in the background with the -d flag. 

2. Access the application:

Open your web browser and go to `http://localhost:5002`. You should see something similar to:

```yaml
Hello, World! MySQL version: 8.0.25
```

3. Stop the services:

To stop and remove the containers, use:

```bash
docker-compose down
```

---

## Conclusion 🎉

This simple project demonstrates how to configure a multi-container Docker application using Docker Compose. It consists of a Flask web app container that connects to a MySQL database container. Docker Compose makes it easy to define, configure, and manage these services in a single file.