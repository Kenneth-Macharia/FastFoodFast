''' This module defines the API documentation resource '''

from flask import redirect
from flask_restful import Resource


class Documentation(Resource):

    def get(self):
        ''' This function handles the 'GET/' endpoint '''

        return redirect("https://documenter.getpostman.com/view/5300721/Rztsom84?version=latest", 302)
