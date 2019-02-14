[![Build Status](https://travis-ci.org/Kenneth-Macharia/FastFoodFast.svg?branch=challenge_2-API_endpoints)](https://travis-ci.org/Kenneth-Macharia/FastFoodFast)
[![Coverage Status](https://coveralls.io/repos/github/Kenneth-Macharia/FastFoodFast/badge.svg?branch=challenge_2-API_endpoints)](https://coveralls.io/github/Kenneth-Macharia/FastFoodFast?branch=challenge_2-API_endpoints)
[![Maintainability](https://api.codeclimate.com/v1/badges/27b3a3a8da654d6c0183/maintainability)](https://codeclimate.com/github/Kenneth-Macharia/FastFoodFast/maintainability)

# The FastFoodFast Web App
## Introduction 
This repository hosts the development of an online app for FastFoodFast, a 5 star restaurant. On the front, users will iteractive with a website to order food for delivery from.

## The Components
The app is made up of: 

    1.UI templates developed using HTML5 and CSS3
    2.A RESTful API developed using the Python Flask microframework
    3.A PostgreSQL database

## Getting started
Before any of the above components can be tested, the following must be done:

    1.Clone this repo to a local machine
    2.Checkout the 'develop' branch while in the project root folder: 
        /FastFoodFast~$git checkout develop
    3.To view the UI templates, navigate to the 'templates' folder and open index.html
        /FastFoodFast/app/v1/views/templates
    4.To test the API, first install PostgreSQL on the local machine
    5.Create a database to use for the testing
    6.Create a user with full right to the database above
    7.Install virtulenv to create a virtual environement for the API:
        /FastFoodFast~$pip install virualenv
    8.While in the project root folder create a virtual environment to isolate the app
        /FastFoodFast~$virtualenv <your-virtual-environment-name>
    8.Active the virtual environment, the prompt is now preceeded by '(your_env_name)'
        /FastFoodFast~$. <your-virtual-environment-name>/bin/activate
    9.Install all the API dependancies in the virtual environment:
        (your_env_name)/FastFoodFast~$pip install -r requirements.txt
    10.Export the OS environment variable required to run the API (See .env sample file)
        /FastFoodFast~$export <the_environement_variable>=<the_environment_value>
    11.Test to ensure the API runs and start the Flask server on the local machine:
        /FastFoodFast~$python run.py

## Running the automated tests on the API
To run the test suite on the app source code:

    1.Ensure steps 1 to 10 are done from the 'Getting started' section above.
    2.Run the test and generate a test report: /FastFoodFast~$py.test --cov=app

## Testing the