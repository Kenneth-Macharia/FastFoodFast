[![Build Status](https://travis-ci.org/Kenneth-Macharia/FastFoodFast.svg?branch=challenge_2-API_endpoints)](https://travis-ci.org/Kenneth-Macharia/FastFoodFast)
[![Coverage Status](https://coveralls.io/repos/github/Kenneth-Macharia/FastFoodFast/badge.svg?branch=challenge_2-API_endpoints)](https://coveralls.io/github/Kenneth-Macharia/FastFoodFast?branch=challenge_2-API_endpoints)
[![Maintainability](https://api.codeclimate.com/v1/badges/27b3a3a8da654d6c0183/maintainability)](https://codeclimate.com/github/Kenneth-Macharia/FastFoodFast/maintainability)

# The FastFoodFast Web App
## Introduction 
This repository hosts the development of an online app for FastFoodFast, a 5 star restaurant. Users will iteractive with the website frontend to order food for delivery.

## The Components
The app is made up of: 

    1.UI templates developed using HTML5 and CSS3

    2.A RESTful API developed using the Python Flask microframework

    3.A PostgreSQL database

## Getting started
Before any of the above components can be tested, the following must be done:

    1.Clone this repo to a local machine.

    2.Checkout the 'develop' branch while in the project root folder:
    
        /FastFoodFast~$git checkout develop

    3.Install PostgreSQL, create a database and a full rights user to the database:
    
    https://www.tutorialspoint.com/postgresql/index.htm
  
    4.Install virtulenv to create a virtual environement for the API:
    
        /FastFoodFast~$pip install virualenv

    5.While in the project root folder create a virtual environment to isolate the app:
    
        /FastFoodFast~$virtualenv <your-virtual-environment-name>

    6.Active the virtual environment; the prompt will then be preceeded by '(your_env_name)':
    
        /FastFoodFast~$. <your-virtual-environment-name>/bin/activate

    7.Install all the API dependancies in the virtual environment:
    
        (your_env_name)/FastFoodFast~$pip install -r requirements.txt

    8.Export the OS environment variables required to run the API (See .env sample file):
    
        /FastFoodFast~$export <the_environement_variable>=<the_environment_value>
        
## Viewing the UI templates
To view the UI templates:

    1.Navigate to the 'templates' folder:
    
        /FastFoodFast/app/v1/views/templates
    
    2.Open index.html.
    

## Running the automated tests on the API
To run the test suite on the app source code:

    1.Ensure all the steps are done from the 'Getting started' section above.

    2.Run the test and generate a test report:
    
        /FastFoodFast~$py.test --cov=app

## Testing the API
To test the API endpoints: 

    1.Run the API and ensure the Flask server is running:
    
        /FastFoodFast~$python run.py

    2.Follow the link to the API documentation below:
    
        https://documenter.getpostman.com/view/5300721/Rztsom84
        
    3.Test the endpoints as illustrated in the documentation, on postman or in terminal.

## Author
Kenneth Macharia
