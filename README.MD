# Setup
## Creating the Database

The docker-compose.yaml file in this repo specifies a mariadb container with the credentials used within this project. 

First start that container. Then, connect to it via 

`mysql -h 127.0.0.1 -u root -p`

and create the database by running 

`CREATE DATABASE ethicsdb;`

Following that, exit the DB and from within this repositories folder, run

`python3 manage.py migrate EthicAssessmentSoftware`

To create the necessary Tables. If you are first setting up your application you must also create additional tables, do so via 

`python3 manage.py migrate`

# Starting the server
To start the server, run:

`python3.9 manage.py runserver 8080`

# Using the application
The Server will expose the API on the port specified in above command. 

To see the available routes, navigate to http://localhost:8080/

The application can be used directly via tools like cURL, via the provided Postman collection, or via the admin interface.

## Via Postman

within the folder 'docs' you will find a postman collection for version 2.1 of Postman. The file contains all methods, routes and sample data.

When using the collection keep in mind that you will have to adjust e.g. IDs in requests according to your current system state - check that via the GET methods. 

## Via the admin interface
For this to work, you will require a superuser that you must create first. 

To do so, run 

`python3.9 manage.py createsuperuser` 

and provide your username, email and password. 

Then, navigate to http://localhost:8080/admin/

Log in to then on the left side see entries for Anwendung, Stakeholder, Motivation, Ansatz, Anforderung and Konsequenz. 

By clicking on them you can see all elements currently in the system, enter new ones, edit existent ones or delete entries. 

# Application concepts
The application builds on the MEESTAR-FW concept and implements parts of its documentation. 
As a small diversion, there is no data model for 'Recht' or 'Wert'. 
As from a data model perspective they are the same, they are generalized into 'Motivation'. 
Each Motivation has an attribute "ist_recht" which if True indicates that the motivation is a 'Recht', otherwise it is a 'Wert'.

Each application has Stakeholders, Motivations and approaches ('Ansatz'). 
Motivations can again have consequences, which an 'Ansatz' tries to counter (they therefore are linked).
An 'Ansatz' then poses multiple ethical motivated requirements ('Anforderung') that must be completed for that 'Ansatz' to be realised.
Only if an 'Ansatz' is realised, the modeled 'effect' truely happens. The effect is a positive or negative integer that then can added on top of Consequences (field 'bewertung'').

