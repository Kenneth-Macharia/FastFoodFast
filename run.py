''' This module runs the apps versions in their respective main.py modules '''

import os
from app.v1.main import app

# Set the app environment
RUN = os.getenv('FLASK_ENV')

if not RUN or RUN == '':
    exit('Set app runtime environment - See .env sample file')
elif RUN == 'development':
    debug_status = True
else:
    debug_status = False

# Run the app
if __name__ == "__main__":
    app.run(debug=debug_status)
    