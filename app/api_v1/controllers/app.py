''' Test resources module '''

from flask_restful import Resource

class Test_app(Resource):

    def get(self):
        ''' Displays a msg on home page '''
        return {"data":"Hello world"}
