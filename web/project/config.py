import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"
    COVERS_FOLDER = f"{os.getenv('APP_FOLDER')}/project/covers_dir"
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
    UPLOAD_PATH = f"{os.getenv('APP_FOLDER')}/project/media/profile/"  # noqa
    PROFILE_PICS = f"{os.getenv('APP_FOLDER')}/project/static/images/avatars/"  # noqa
    SECRET_KEY = "e0ebacd2434401268911e86b15544660d98e68ca"
    CSRF_SESSION_KEY = "e0ebacd2434401268911e86b15544660d98e68ca"
    SERVER_NAME = "lon1.apankov.net:8092"
    TEMPLATES_AUTO_RELOAD = True
