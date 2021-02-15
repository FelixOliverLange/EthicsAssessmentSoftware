# Setup
## With Docker-Compose
This repo contains a Dockerfile that creates a docker image of the ethics assessment software for MEESTAR-FW.
The also included Docker Compose file can be used to spin up that image together with a DB server that serves as persistence layer. 

To run the software using docker, install docker on your system first, including docker-compose. As of 2021, a docker-desktop installation does that for you. 

Once you have docker-compose installed, simply run: 

`docker-compose up`

and to stop it, eiter press CTL + C in your interactive terminal, or run 

`docker-compose down`

from within this repositories root folder. The system will be available at

http://localhost:8080/

If you wish to use the UI (see 'using the application' below), the admin user and his credentials are defined in the docker-compose.yaml file. 
If you wish to change them, edit the file before running `docker-compose up`

## With Docker and an external database server (MariaDB / MySQL)
You can also run the application in combination with an external database server that you already have. 

Please note that that DB sever should be MySQL / MariaDB, the application was tested using MariaDB 10.4. 

In order to do so, adjust the file ./code/EthikBackend/settings.py to have the corresponding DB server name, database name and suitable credentials.

If you wish to use the predefined database name in this application, simply run 

`CREATE DATABASE ethicsdb;`

and ensure you have a user with access to that DB at hand.

Then, you can run the app localy within docker by running (from within this repositories root folder):

`docker build . --tag ethikbackend:latest`

`docker run --env ADMIN_USER=<your username> --env ADMIN_MAIL=<your e-mail> --env ADMIN_PASSWORD=<your password>  -it ethikbackend:latest /bin/bash`

and then within the container run

`python3 manage.py migrate && python3 manage.py initadmin && python3 manage.py runserver 0.0.0.0:8080`

to migrate the DB, create the admin user and start the server. The system will then be available at http://localhost:8080/ .

In order to stop the application, simply type CTL + C inside of the container and then type `exit` to end the container.

## With bare metal
If you do not wish to run the application using docker, you can also do so natively on your system. 
Simply have Python3 in a recent version installed (this was up to now tested with the latest version of Python 3.5) as well as pip3.
To install the required dependencies, run 

`pip3 install -r requirements.txt`

from within this repository. Perhaps best do so in a virtual environment like Venv/Conda. 

Then, adjust the file ./code/EthikBackend/settings.py to have the suitable DB server name, 
database name and suitable credentials configured that you wish to use. 

Then, migrate the DB by running:

`python3 manage.py migrate`

If you wish to use the UI later on, create a super user by running

`python3.9 manage.py createsuperuser` 

and provide your username, email and password. 

As an alternative you can also set the environment variables `ADMIN_USER`, `ADMIN_MAIL` and `ADMIN_PASSWORD` 
and then run `python3.9 manage.py createsuperuser`. Please note that for that to work your environment variables must be defined not only in your shell,
i.e. use the `export` command on GNU/Linux systems.

To finally start the server, run:

`python3.9 manage.py runserver 8080`

The system will then be available at http://localhost:8080/ .

## With alternative database engines
If you're not a fan of MariaDB / MySQL, simply read the docs about the DB engines supported: 

https://docs.djangoproject.com/en/3.1/ref/databases/

and adjust the file ./code/EthikBackend/settings.py accordingly. 

after that, run 

`python3 manage.py makemigrations` 

to create the required DB migrations and run 

`python3 manage.py migrate`

to apply them. 

## Purging Data
Assuming you want to completely reset everything, you can simply purge all data on the DB server side - the application itself does not maintain additional state.

If you're using Docker to run your DB server, stop the running containers and run

`docker volume prune`

NOTE: this will delete ALL your volumes. If you are using Docker for other stuff as well, this is NOT SAFE. 
Instead, run 

`docker volume ls`

to list your volumes and then run 

`docker volume rm <your volume>`

With the volume ID identified to be your DB volume. 
Then, simply restart your docker instance and the web application. 

If you're running a dedicated DB server, you can simply drop the DB and recreate it: 

`DROP DATABASE ethicsdb;`

`CREATE DATABASE ethicsdb;`

# What the application is about
The application you just set up allows you to document (some) outcome of MEESTAR-FW workshops as described in the project thesis available at
https://github.com/FelixOliverLange/ethikarbeit 

As a small diversion, there is no data model for 'Recht' or 'Wert'. 
As from a data model perspective they are the same, they are generalized into 'Motivation'. 
Each Motivation has an attribute "ist_recht" which if True indicates that the motivation is a 'Recht', otherwise it is a 'Wert'.

Within the system, each application that you create has Stakeholders, Motivations and approaches ('Ansatz'). 
Motivations can again have consequences, which an 'Ansatz' tries to counter (they therefore are linked).
An 'Ansatz' then poses multiple ethical motivated requirements ('Anforderung') that must be completed for that 'Ansatz' to be realised.
Only if an 'Ansatz' is realised, the modeled 'effect' truely happens. 
The effect is a positive or negative integer that then can added on top of Consequences (field 'bewertung'').

So within this application, you can create, view, edit and delete: 
* applications (Anwendung), 
* their stakeholders (Stakeholder), 
* their motivations (Motivation, those are either values or laws applicable to the application), 
* their consequences (Konsequenz, affecting a motivation for a stakeholder),
* their solution approaches (Ansatz, which address a consequence)
* their requirements (Anforderung, necessary to be fulfilled to put an Ansatz into effect / realise it)

As of now, Scenarios (governing which Ansatz aktually is being realised / planned to be realised) are not supported.
Neither are the specific UI documentations described in the project thesis.
The data types that currently are supported are descibed in more detail below.

## The data types within
As described above, the application has seven data types. They have following fields with following meanings:

Anwendung: 
* only has a `name` describing the Anwendung

Stakeholder:
* has a `anwendung` for which it is valid
* has a `name` which has to be unique within the system
* has a `beschreibung` (description) describing the stakeholder role and other details

Motivation: 
* has a `anwendung` for which it is valid
* has a `name` which has to be unique within the system
* has a `beschreibung` (description) describing the motivation and other details
* has a `shutzklasse` (protection class) which in MEESTAR-FW typically is either 'Menschheit', 'Gesellschaft', 'Organisation' or 'Individuum'
* has a `priorität` (priority) which is an integer of typically positive value, valid within its protection class 
* has a `ist_rect` (is_right) boolean argument that is 'True' if the motivation is a right of e.g. inernational law, otherwise it is 'False'  (then it is a Wert, a Value)

Konsequenz:
* has a `name` which has to be unique within the system
* has a `beschreibung` (description) describing the konsequenz and other details
* has a `bewertung` (rating) which is an integer. Positve values describe a positive effect onto the Motivation (enforcing and protecting it), negative integers describe a negative effect (damaging the Motivation and keeping it from becoming reality)
* has a `motivation` linking the motivation affected
* has a `betroffener` linking the stakeholder affected

Ansatz:
* has a `anwendung` for which it is valid
* has a `name` which has to be unique within the system
* has a `beschreibung` (description) describing the Ansatz and other details
* has a `adressiert` (addresses) linking the konsequenz that it addresses
* has a `auswirkung` (effect) that describes it's effect towards the Konsequenz, an integer field. A positive value denotes that the konsequence is turned to the better, a negative denotes that it turns the konsequence to the worse. The values are delta values, so it only denote by how much the `bewertung` of the linked konsequenz changes, not the final value!

Anforderung: 
* has a `ansatz` which it affects
* has a `name` which has to be unique within the system
* has a `beschreibung` (description) describing the Anforderung and other details


# Using the application
The Server will expose the API on the port specified in above command that allows creating, editing, viewing and deleting elements of the above described data types.

If you've followed the above commands directly, that's port 8080.

To see all the available routes, navigate to http://localhost:<your port>/, e.g. http://localhost:8080/

The available routes include all data types as lists and details endpoints alongside the admin interface.

The application can be used directly via tools like cURL, via the provided Postman collection, or via the admin interface.

## Via Postman

within the folder 'docs' you will find a postman collection for version 2.1 of Postman. 
The file contains all methods, routes and sample data.
If you wish to test the API directly, this is probably the most convenient approach.

When using the collection keep in mind that you will have to adjust e.g. IDs in requests according to your current system state - check that via the GET methods. 


## Via Swagger UI and redoc
The application also has a swagger UI exposed at "/swagger/", so if you've followed above setup you will find it at http://localhost:8080/swagger/

The UI has all endpoints, responses, models and request payloads documented, so you can easily use it to test the application from within your browser.

Same goes for the Redoc UI which is available at "/redoc/", so with above standard setup you can find it at http://localhost:8080/redoc/

The OpenAPI specification is also available at http://localhost:8080/swagger/?format=openapi and is in version 2.0. 

The Swagger UI, OpenAPI Spec and Redoc view are kindly made possible by https://github.com/axnsan12/drf-yasg

## Via the admin interface
For this to work, you will require a superuser that you must create first. see the 'Setup' section for details.

Once you have one, navigate to http://localhost:8080/admin/

Log in to then on the left side see entries for Anwendung, Stakeholder, Motivation, Ansatz, Anforderung and Konsequenz. 

By clicking on them you can see all elements currently in the system, enter new ones, edit / view existent ones or delete entries.

# Acknowledgement
I followed this tutorial:
https://bezkoder.com/django-crud-mysql-rest-framework/#:~:text=First%2C%20we%20setup%20Django%20Project,operations%20(including%20custom%20finder). 
which served my quite well in getting to Know Django. Apart from that, the following resources were helpful:  
* https://docs.djangoproject.com/en/3.1/intro/tutorial03/
* https://docs.djangoproject.com/en/3.1/topics/db/queries/#field-lookups
* https://docs.djangoproject.com/en/3.1/topics/http/urls/
* https://www.laravelcode.com/post/django-3-crud-tutorial-example-with-mysql-and-bootstrap
* https://sunscrapers.com/blog/the-ultimate-tutorial-for-django-rest-framework-functional-endpoints-and-api-nesting-part-6/
