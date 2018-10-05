import os
import csv
import sqlite3
from typing import Iterable, Tuple, Optional
from uuid import uuid1
from concurrent.futures import ThreadPoolExecutor
from .downloading import download_image
from .db import INSERT_STATEMENT, setup_db
from .helpers import iterrows, try_float_cast, read_batch
from .config import IMAGES_FOLDER, MAX_THREADS


# Original columns indexes
PROGRAMNAME_COL_IDX = 0  # PROGRAMNAME is the 1st col
NAME_COL_IDX = 4  # NAME is the 5th col
DESCRIPTION_COL_IDX = 6  # DESCRIPTION is the 7th col
SKU_COL_IDX = 7  # SKU is the 8th col
SALEPRICE_COL_IDX = 13  # SALEPRICE is 14th col
PRICE_COL_IDX = 14  # PRICE is the 15th col
URL_COL_IDX = 17  # SKU is the 18th col
IMAGEURL_COL_IDX = 19  # IMAGEURL is the 20th col
ADVERTISERCATEGORY_COL_IDX = 20  # ADVERTISERCATEGORY is 21th col.
STOCK_COL_IDX = 36  # INSTOCK is the 37th col

# Constant values
RETAILER_CODE = 12
RETAILER_NAME = "Apt2B"


def has_interesting_category(row: list) -> Tuple[bool, str]:
    """
    Obtains the category of the product, and decides whether the product
    is interesting to us based on its category

    Args:
        row: Thw product's row.

    Returns:
        First element denotes whether the product is interesting to us.
        Second element is the product's category.
    """
    category = row[NAME_COL_IDX].lower()
    unwanted = ["chaise", "bench", "daybed", "day bed", "sectional"]
    for token in unwanted:
        if token in category:
            return False, token

    wanted = ["sofa", "loveseat", "love seat", "couch", "settee"]
    for token in wanted:
        if token in category:
            return True, token

    return False, ""


def is_in_stock(row: list) -> bool:
    """
    Whether the product is in stock.
    """
    stock = row[STOCK_COL_IDX].lower()
    return stock == "yes"


def is_sleeper(row: list) -> int:
    """
    Whether the product is in stock.
    """
    if "sleeper" in row[NAME_COL_IDX].lower():
        return 1
    return 0


def create_cora_row(row: list, category: str, img_filename: str) -> tuple:
    """
    Adapts the original data of a product to fit Cora's use case.

    Args:
        row: The original data of a particular product
        category: the category of the product
        img_filename: The filename of the product's image.
    
    Returns:
        The data of the product, adapted and ready to be stored in DB
    """
    return (
        RETAILER_CODE,
        RETAILER_NAME,
        row[SKU_COL_IDX],
        row[URL_COL_IDX],
        category,
        row[NAME_COL_IDX],
        is_sleeper(row),
        try_float_cast(row[SALEPRICE_COL_IDX]),
        try_float_cast(row[PRICE_COL_IDX]),
        "",  # TODO: Figure out width
        "",  # TODO: Figure out depth,
        "",  # TODO: Figure out height
        img_filename,
        row[DESCRIPTION_COL_IDX],
    )


def clean_data(filepath: str) -> Iterable:
    """
    Takes a CSV product catalog from Apt2B and generates its
    clean and interesting rows, next to their corresponding product
    images.
    """
    for row in iterrows(filepath):
        if not is_in_stock(row):
            continue

        is_interesting, category = has_interesting_category(row)
        if not is_interesting:
            continue

        img_name, img_url = get_image_info(row)
        yield create_cora_row(row, category, img_name), (img_name, img_url)


def get_image_info(row: tuple) -> Tuple[str, str]:
    """
    Extracts the URL and name of the image of a product.

    Args:
        row: The product's row
    
    Return:
        The image's name and its URL.
    """
    img_url = row[IMAGEURL_COL_IDX]
    final_path = img_url.split("/")[-1]
    filename = final_path.split("?")[0]
    return f"12+{filename}", img_url


def process_csv(filepath: str):
    """
    Entrypoint of this program. Takes care of setting up DB, 
    cleaning up the CSV file, and inserting its data into DB,
    and downloading the product images.

    Args:
        filepath: The path to the CSV file.
    """
    conn, cursor = setup_db()

    os.makedirs(IMAGES_FOLDER)
    clean_rows = clean_data(filepath)
    with ThreadPoolExecutor(MAX_THREADS) as pool:
        for batch in read_batch(clean_rows):
            data_batch = [data for data, img_url in batch]
            images_batch = [img_url for data, img_url in batch]
            pool.map(lambda args: download_image(*args), images_batch)
            cursor.executemany(INSERT_STATEMENT, data_batch)
            conn.commit()
    cursor.close()
    conn.close()

