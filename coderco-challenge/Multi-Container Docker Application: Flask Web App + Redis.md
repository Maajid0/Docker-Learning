# Basic Multi-Container Docker Application: Flask Web App + Redis 🐳

This project demonstrates how to use **Docker Compose** to create a multi-container application with a **Flask** web app and a **Redis** database. The goal of this setup is to show how to configure and run multiple Docker containers using a simple `docker-compose.yml` file.

## Overview 🚀

The application is a basic Flask web app that connects to a Redis container. When the Flask app runs, it connects to Redis to keep track of the number of times the page has been visited. The visit count is stored in Redis, and it increments every time you visit the `/count` route.

## Application Components ⚙️

1. **Flask Web App** (`app.py`): A simple Python web app using Flask that connects to Redis and tracks visit count.
2. **Redis Database**: A Redis container used as a key-value store to track visit counts.
3. **Docker Compose** (`docker-compose.yml`): Used to configure and run both the web app and Redis containers in parallel.
4. **Dockerfile**: A file used to build the Docker image for the Flask app.

## Code Breakdown 💻

### 1. `app.py` - Flask Web Application 🌐

This is the basic Flask app that connects to the Redis container to track the visit count.

```python
from flask import Flask
import redis

app = Flask(__name__)

# Connect to Redis (using the service name defined in docker-compose.yml)
r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

@app.route('/')
def hello_world():
    return 'Welcome to my Flask app'

@app.route('/count')
def visit_count():
    # Increment the visit count stored in Redis
    count = r.incr('visits')
    print(f"Visit count: {count}")  # Debug print to check the value of count
    return f'This page has been visited {count} times.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```
- This app connects to Redis using the hostname `redis` (as defined in the `docker-compose.yml`).
- It increments the `visits` key in Redis and displays the current count when visiting `/count`.

### 2. Dockerfile - Building the Web App Image 🏗️

The Dockerfile is used to build the Docker image for the Flask app. It installs dependencies and configures the environment to run the app.

```dockerfile
# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5001 for the Flask app
EXPOSE 5001

# Run the Flask app when the container starts
CMD ["python", "app.py"]
```

- This `Dockerfile` uses the official Python image, installs dependencies from `requirements.txt`, and runs the Flask app on port `5001`.

### 3. `docker-compose.yml` - Defining the Multi-Container Setup 📝

The `docker-compose.yml` file defines both the Flask web app and the Redis container as services and handles the orchestration of the two containers.

```yaml
version: '3.8'

services:
  flask-app:
    build: .
    ports:
      - "5001:5001"
    depends_on:
      - redis  

  redis:
    image: "redis:latest"
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data  # Persist Redis data

volumes:
  redis-data:
```

- `flask-app`: The Flask app service is built using the `Dockerfile` in the current directory.
    - The app listens on port `5001`.
    - It depends on the `redis` service to ensure the Redis container starts before the Flask app.
- `redis`: The Redis service uses the latest official Redis image.
    - It exposes port `6379` and uses a volume to persist Redis data
- `volumes`: Defines a volume `redis-data` to persist Redis data across restarts.

### 4. Running the Application 🏃‍♂️

To run the multi-container application, follow these steps:

1. Build and start the containers:

Run the following command to build the Docker images and start both the Flask web app and the Redis database:

```bash
docker-compose up -d
```

This will:

- Build the Flask app image using the `Dockerfile`.
- Start both the Flask app container and the Redis container in the background with the `-d` flag.

2. Access the application: 

Open your web browser and go to`http://localhost:5001`. You should see the "Welcome to my Flask app!" message.

Next, go to `http://localhost:5001/count`. This should display something like:

```yaml
This page has been visited 1 times.
```

Each time you refresh the `/count` route, the visit count will increment.

3. Stop the services:

To stop and remove the containers, use:

```bash
docker-compose down
```

---

## Conclusion 🎉

This project demonstrates how to set up a simple multi-container Docker application with Flask and Redis using Docker Compose. You can easily extend this setup by adding more services or modifying the app's functionality.

---

## Notes 📝

- If you're testing locally, ensure you have Docker and Docker Compose installed.
- Redis data will be persisted using the `redis-data` volume to avoid data loss on container restart.

---

## Bonus Tasks 🎯

### Persistent Storage for Redis

To ensure Redis retains data even after the container stops or restarts, you have already configured a volume in the `docker-compose.yml` file. The `redis` service is using a volume called `redis-data`, which persists the data at `/data` inside the container.

```yaml
 redis:
  image: "redis:latest"
  ports:
    - "6379:6379"
  volumes:
    - redis-data:/data  # Persist Redis data
```

### Environment Variables for Redis Connection

To make the Flask app more flexible and configurable, the Redis connection details (`REDIS_HOST` and `REDIS_PORT`) are now passed as environment variables. This allows the Flask app to connect to Redis using values defined in the `docker-compose.yml` file.

```yaml
flask-app:
  environment:
    - FLASK_APP=app.py
    - FLASK_RUN_HOST=0.0.0.0
    - REDIS_HOST=redis
    - REDIS_PORT=6379
```

In the `app.py`, these values are accessed using `os.getenv()`.

```python
import os

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', 6379)
```

### Scaling the Flask Application

You can scale the Flask app by running multiple instances of it and load balancing between them using Docker Compose. To `scale` the Flask app, you can add the scale option to the `docker-compose.yml` file or run the following command:

```bash
docker-compose up --scale flask-app=3 -d
```

This will run 3 instances of the Flask app container. Docker Compose will automatically load balance the traffic between these instances.

You can view the logs from all containers by running:

```bash
docker-compose logs -f
```

To stop the scaled services, use:

```bash
docker-compose down
```

--- 

## Conclusion 🎉

This project demonstrates how to set up a simple multi-container Docker application with Flask and Redis using Docker Compose. You also learned how to add persistent storage for Redis, use environment variables for configuration, and scale the Flask application using Docker Compose.

---

## Notes 📝

- If you're testing locally, ensure you have Docker and Docker Compose installed.
- Redis data will be persisted using the `redis-data` volume to avoid data loss on container restart.