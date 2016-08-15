"""Settings package initialization."""

import dotenv
dotenv.load()

# Ensure development settings are not used in testing and production:
if dotenv.get('ENVIRONMENT') == 'HEROKU':
    from .production import *
elif dotenv.get('ENVIRONMENT') == 'TRAVIS':
    from .testing import *
else:
    from .local import *
