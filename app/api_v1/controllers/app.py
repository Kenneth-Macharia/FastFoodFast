''' Test resources module '''

from flask import jsonify
from flask_restful import Resource

class Test_api(Resource):

    def get(self):
        ''' Displays a msg on home page '''
        return {"data":"Hello world"}
        