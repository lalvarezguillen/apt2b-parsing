import mysql.connector
from .config import DB_PARAMS


INSERT_STATEMENT = (
    "INSERT INTO apt2b (retailer_code, retailer_name, "
    "sku, url, category, product_name, sleeper, sale_price, "
    "regular_price, width, depth, height, image, description) "
    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)
# SQL statement to insert Cora rows in DB


def setup_db():
    """
    Connects to the DB and creates a cursor.
    
    Returs:
        the connection and the cursor
    """
    conn = mysql.connector.connect(**DB_PARAMS)
    cursor = conn.cursor()
    sql_create_table = (
        "CREATE TABLE IF NOT EXISTS `apt2b`("
        "`id` int(10) unsigned primary key auto_increment, "
        "`retailer_code` int(11), "
        "`retailer_name` varchar(500), "
        "`sku` varchar(255), "
        "`url` varchar(1000), "
        "`category` varchar(500), "
        "`product_name` varchar(500), "
        "`sleeper` int(11), "
        "`sale_price` float, "
        "`regular_price` float, "
        "`width` varchar(500), "
        "`depth` varchar(500), "
        "`height` varchar(500), "
        "`image` varchar(500), "
        "`description` text) ENGINE=InnoDB"
    )
    cursor.execute(sql_create_table)
    return conn, cursor
