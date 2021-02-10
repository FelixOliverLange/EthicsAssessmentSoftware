Setup:

The docker-compose.yaml file in this repo specifies a mariadb container with the credentials used within this project. 

First start that container. Then, connect to it via 

mysql -h 127.0.0.1 -u root -p

and create the database by running 

CREATE DATABASE ethicsdb;

Following that, exit the DB and from within this repositories folder, run

python3 manage.py migrate EthicAssessmentSoftware

To create the necessary Tables
