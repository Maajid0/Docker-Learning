# this is your base image
FROM python:3.9

# we set the working dir in yourr container
WORKDIR /usr/src/app

# copying reqs file to your container so you can install the app reqs ygm
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy your app code fam
COPY . .

# expose/open up the port on your container so you can access your app ygm
EXPOSE 5001

# running app in container
CMD ["python", "app.py"]