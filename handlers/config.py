from datetime import timedelta

SECRET_KEY = "5f98079c7458d648234ee38b2d3dbd0ed78817f09f5cf225379dd0d5c8d78f85"
CSRF_ENABLED = True
DEBUG = True
SESSION_COOKIE_NAME = "session"
PERMANENT_SESSION_LIFETIME = timedelta(days=31)
SESSION_REFRESH_EACH_REQUEST = True
EXPLAIN_TEMPLATE_LOADING = True
MAX_COOKIE_SIZE = 0
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 0
UPLOAD_FOLDER = 'static/img/uploads'
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Vbn_78900@localhost:5432"
SQLALCHEMY_TRACK_MODIFICATIONS = True
