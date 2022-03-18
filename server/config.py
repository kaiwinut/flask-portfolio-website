import os
from datetime import date

DB_NAME = 'database.db'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
SECRET_KEY = os.urandom(24)

INVITATION = 'sha256$FjbHCDZZzAFOQBQg$0de7bc75241e7fabd8862f71d3c73c5b20f1e5b7c7d880b6e2c6a63a68e3d3ef'
CURRENT_YEAR = date.today().year