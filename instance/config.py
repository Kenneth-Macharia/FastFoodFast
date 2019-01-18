''' This module include the various evirnonments to run the appself.
    To switch enironments, type at the prompt before runing the app:
        > export APP_SETTINGS="<the desired environment>" '''
        
import os

class app_base_configs(object):
    SECRET = os.getenv('SECRET')

class app_development_configs(app_base_configs):
    DEBUG = True
    # DATABASE_URL="postgresql:///devdb"
    # DATABASE_USERNAME="kmacharia"
	# DATABASE_PASSWORD="123456"
    
class app_testing_configs(app_base_configs):
    DEBUG = True
    TESTING = True
    # DATABASE_URL="postgresql:///testdb"
    # DATABASE_USERNAME="kmacharia"
	# DATABASE_PASSWORD="123456"

class app_staging_configs(app_base_configs):
    DEBUG = False
    TESTING = False
    # DATABASE_URL="postgresql://<your staging database URL>"
	# DATABASE_USERNAME="<your database user, for both databases"
	# DATABASE_PASSWORD="your database password, for both databases"

class app_production_configs(app_base_configs):
    DEBUG = False
    TESTING = False
    # DATABASE_URL="postgresql://<your production database URL>"
	# DATABASE_USERNAME="<your database user, for both databases"
	# DATABASE_PASSWORD="your database password, for both databases"

env_app_configs = {
    'development': app_development_configs,
    'testing': app_testing_configs,
    'staging': app_staging_configs,
    'production': app_production_configs
}