# The superwise project
super wise task



# How to use the server

the flow should do:
- start flask server on docker
- open endpoint for client to do get to specific route
- parse the request from the client 
- db retrival data
- parse data from db and calculate recall
- send the result of the recall to kafka
- send a response back to the client


## Features

- x


## ToDos:
- Change prints into Logs logic - first save it to local file .log, in the feature to elastic search schema or logs.io infrastructure

- Split the logics from the app.py file into different files/modules/ or maybe even folders - db logics, parsing data logic, kafka logics and leave only the routes and basic calls from the app.py file (as the main Flask server backend logic that calls and refer to all the other logics and functionalities)

- Build and deploy the server on a docker using DockerFile / docker.yaml for Docker Compose in order to make it more reslient and robust.

- Consider adding asyncio for the concurrency working on the same DB with 2 different tables (same for different topics of kafka)

- Consider adding reversed proxy and load balancer for the server backend (nginx, apache httpd)

- Update the psycopg2 library into something more known maybe like Pyodbc or SQLalchemy

- Add Type Hints for each function

- Exceptions and Errors wider consideration

- Adding caching to the Database - instead of referring to it every request of a client, but retrieve it actively pariodically every X seconds/minutes/hours - it's probably not changing all the time (at least for this exercise)

## Tech & Installation

The superwise project uses a number of sources to work properly:

- [Python] - Python 3.4+ to run the code on your computer