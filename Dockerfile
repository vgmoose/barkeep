from ubuntu

maintainer vgmoose version: 0.5

workdir /code

run apt-get update

run apt-get install -y python python-pip libmysqlclient-dev

add requirements.txt /code

run pip install -r requirements.txt

env FLASK_CONFIG development
env FLASK_APP run.py

add . /code

cmd ["python", "run.py"]
