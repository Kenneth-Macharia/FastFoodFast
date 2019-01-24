''' This module include the various evirnonments to run the app.
To switch enironments, type at the prompt before runing the app:
> export APP_SETTINGS=<the desired environment> '''
import os


class AppBaseConfigs(object):
    ''' App base congigs class '''
    SECRET = os.getenv('SECRET')


class AppDevelopmentConfigs(AppBaseConfigs):
    ''' Development app configs '''
    DEBUG = True

class AppTestingConfigs(AppBaseConfigs):
    ''' Testing app configs '''
    DEBUG = True
    TESTING = True


class AppStagingConfigs(AppBaseConfigs):
    ''' Staging app configs '''
    DEBUG = False
    TESTING = False


class AppProductionConfigs(AppBaseConfigs):
    ''' Production app configs '''
    DEBUG = False
    TESTING = False


ENV_APP_CONFIGS = {
    'development': AppDevelopmentConfigs,
    'testing': AppTestingConfigs,
    'staging': AppStagingConfigs,
    'production': AppProductionConfigs
}
