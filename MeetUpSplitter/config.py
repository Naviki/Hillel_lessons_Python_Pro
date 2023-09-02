import os

DB_CONFIG = {
    'NAME': os.environ.get('DB_NAME', 'meetupsplitter_base'),
    'USER': os.environ.get('DB_USER', 'Guest_user'),
    'PASSWORD': os.environ.get('DB_PASSWORD', '1488'),
    'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
    'PORT': os.environ.get('DB_PORT', '5432')
}