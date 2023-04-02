
MLM Library Management System
This is a simple library management system API built using Django and Django REST framework. The API allows users to manage books, checkouts and users.

API Endpoints
The API endpoints are:

api/users - to manage users
api/books - to manage books
api/checkouts - to manage checkouts
api/login - to authenticate users

How to Run
Prerequisites
Make sure you have the following installed:

Docker
Docker Compose
Installation
Clone the repository


git clone https://github.com/username/mlm.git
Go to the project directory

cd mlm
Build the Docker containers

docker-compose build
Start the application

docker-compose up
The application should now be running on http://localhost:8000/

Database Migrations
To make and run database migrations, use the following commands:


docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
Load Fixtures
To load fixtures, use the following command:

docker-compose exec web python manage.py loaddata fixtures/initial_data.json
