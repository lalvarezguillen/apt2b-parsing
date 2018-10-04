# Apt2B catalog parser

This program parses products catalogs from Apt2b.

## Requirements:
* Python 3.6++
* mysql

## Running the program

This program relies on environment variables for configuration. Check apt2b/config.py for documentation on each configurable setting.

* Install dependencies
```bash
pip install -r requirements.txt
```

* Setup environment variables
```bash
export DB_USER=dummy-user
export DB_PASS=dummy-pass
export DB_HOST=dummy-host
export DB_NAME=dummy-db
export IMAGES_FOLDER=some-folder
export MAX_THREADS=50
``` 

* Run the program, passing a product catalog to it
```bash
python run_script.py apt2b-catalog.csv
```