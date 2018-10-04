import os


# DB_PARAMS contains configuration necessary to connect to MySQL server
DB_PARAMS = {
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASS"],
    "host": os.environ["DB_HOST"],
    "database": os.environ["DB_NAME"],
}

# IMAGES_FOLDER points to the directory where the product images will be downloaded
IMAGES_FOLDER = os.environ["IMAGES_FOLDER"]

# MAX_THREADS specifies the max number of threads that will be used when downloading
# the product images.
MAX_THREADS = int(os.environ.get("MAX_THREADS", 50))
