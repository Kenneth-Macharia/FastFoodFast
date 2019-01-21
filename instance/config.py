''' This module include the various evirnonments to run the app. '''
''' To switch enironments, type at the prompt before runing the app:
        > export APP_SETTINGS=<the desired environment> '''
        
import os

class app_base_configs(object):
    SECRET = os.getenv('SECRET')

class app_development_configs(app_base_configs):
    DEBUG = True
    
class app_testing_configs(app_base_configs):
    DEBUG = True
    TESTING = True

class app_staging_configs(app_base_configs):
    DEBUG = False
    TESTING = False

class app_production_configs(app_base_configs):
    DEBUG = False
    TESTING = False

env_app_configs = {
    'development': app_development_configs,
    'testing': app_testing_configs,
    'staging': app_staging_configs,
    'production': app_production_configs
}