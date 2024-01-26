# Fampay-Backend Assignment(Intern)

## Tech Stacks used:
### Backend- Flask, Rabbitmq, Docker, MongoDB
### Frontend- ReactJS

# Routes 
## Sample Cached videos Route->  
 http://127.0.0.1:5000/videos/cached?page=1  or
 http://127.0.0.1:5000/videos/cached
## Sample search Videos Route-> 
 http://127.0.0.1:5000/videos?query=cars&page=1 or
 http://127.0.0.1:5000/videos?query=cars 

# Functionalities:
### -> GET routes for getting the data from the backend of the application.
### -> Asynchornous processing in the background that runs for every 10 seconds.
### -> Dashboard for viewing the videos on the frontend side
### -> Can use multiple alternative api keys for handling the case when one of them is expired


# Getting started:

### Clone the application: 
git clone https://github.com/viwinkumarpadala/Fampay-assignment.git
### Go to the the Backend of the application:
cd FAMPAY
### Go to the Backend part of the application:
cd backend
### Create a virtual environment:
python -m venv venv
### activate:
source venv/Scripts/activate

### choose the python interpreter in the view part of vs code
## upgrade pip:
### python -m pip install --upgrade pip
## install the dependencies:
### python -m pip install flask
### python -m pip install celery
### python -m pip install dotenv
### python -m pip install pymongo
### python -m pip install datetime
### python -m pip install googleapiclient
### python -m pip install flask-cors

## create a dotenv file with these values:
### db_url=
### api_key=
### api_key2=
### api_key3=
### api_key4=
### api_key5=

## Also make sure to change the rabbitq default user and password in the docker-compose.yml file:
### RABBITMQ_DEFAULT_USER: username
### RABBITMQ_DEFAULT_PASS: password


### run the flask server:
python -m flask --app server run

### build the docker-compose:
docker-compose build

### up the docker compose:
docker-compose up

### now open another terminal and redirect to the frontend folder
cd frontend

### install the dependencies:
npm init
npm install

### Start the frontend part of the application:
npm start

## With this the application is ready with all the requirements
## Now go get some popcorn and have fun watching utube videos( There wont be any ads here hehehe...😂😂)




# THANK YOU
