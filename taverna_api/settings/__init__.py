"""
Settings package initialization.
"""

import dotenv
dotenv.load()

# Ensure development settings are not used in testing and production:
if dotenv.get('ENVIRONMENT') == 'LOCAL':
    from .local import *

if dotenv.get('ENVIRONMENT') in ['HEROKU', 'TRAVIS']:
    from .production import *
