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