''' This module runs the created app in instance.__init__.py '''

import os
from instance import create_app

if __name__ == "__main__":

    app = create_app(os.getenv('APP_SETTINGS'))
    app.run()