# Vaccine-Management-Portal-Assignment

1. Create a virtual environment "venv"
2. Activate virtual environment -> _[source venv/bin/activate]_ or _[venv\scripts\activate]_
3. Install dependencies -> _pip install -r requirements.py_
4. Assignment makes use of PostgreSQL. 
   Create the following databases: -> _CREATE DATABASE vaccination;_
6. Change DB_CONNECTION_STRING in file config.json The format for the same is "_postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName_"
7. To initialise database -> _python run_app.py -ac config.json migrate --init_
8. Apply migrations -> _python run_app.py -ac config.json migrate --migrate_
9. _python run_app.py -ac config.json migrate --upgrade_
10. Finally, to run the server -> _python run_app.py -ac config.json run_

**Run using Docker:**
1. Change DB_CONNECTION_STRING in file config.json The format for the same is "postgres://YourUserName:YourPassword@host.docker.internal:5432/YourDatabaseName"
2. Build Docker Image: _docker build -t <docker-image-name> ._
3. Run Docker Image: _docker run -p 8080:8080 <docker-image-name>_
4. Sample Postman collection link for Testing: https://www.getpostman.com/collections/d4ce17bac155c6ea3057

  
Note: APIs have been authorised by JSON web tokens hence the steps to follow are:
1. Register a user account
2. Login through valid credentials.
3. Upon successful login, you will receive a token in the response body. This token needs to be copied and sent as a part of "Authorization" headers.
