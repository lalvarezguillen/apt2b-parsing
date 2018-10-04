import os


DB_PARAMS = {
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASS"],
    "host": os.environ["DB_HOST"],
    "database": os.environ["DB_NAME"],
}
IMAGES_FOLDER = os.environ["IMAGES_FOLDER"]
MAX_THREADS = 50
