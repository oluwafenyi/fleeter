# Fleeter

Postman Collection: https://www.getpostman.com/collections/616585310306f8d81990

Staging Link: https://fleeter-api.herokuapp.com/


### Running Tests Locally
1. Activate a virtual environment.
2. Install requirements with `pip install -r requirements.txt`
3. Create a .env file in the CWD using .env.sample as a template and source it in your shell.
4. run python manage.py test

### How to Run Locally with Docker
1. Clone this repository and change directory
2. Create a .env file in the CWD using .env.sample as a template
3. Run docker-compose up and find the api server at http://localhost:8000/

