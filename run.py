''' This module runs the apps versions in their respective main.py modules '''

import os
from app.v1.main import app

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
    