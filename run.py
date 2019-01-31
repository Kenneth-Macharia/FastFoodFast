''' This module runs the apps versions in their respective main.py modules '''

import os
from app.v1.main import app

# Blueprints umplemenations simultenously run available app versions
    # v1_blueprint = Blueprint('version1_blueprint', __name__)
    # api = Api(v1_blueprint, prefix='/v1')
    # app.register_blueprint(v1_blueprint)

# Set the app environment
run_environment = os.getenv('FLASK_ENV')

if not run_environment:
    assert False, 'Set app runtime environment - See .env sample file'
elif run_environment == 'development':
    debug_status = True
else:
    debug_status = False

# Run the app
if __name__ == "__main__":
    app.run(debug=debug_status)
    