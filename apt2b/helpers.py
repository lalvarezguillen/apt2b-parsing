import csv
from typing import Iterable, Optional


def iterrows(filepath: str) -> Iterable:
    """
    Iterates over the rows of a CSV file.

    Args:
        filepath: The path to the CSV file.

    Returns:
        a lazy iterable over the file's rows.
    """
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row


def try_float_cast(val: str) -> Optional[float]:
    """
    Attempts to cast a string to float. If it fails returns None
    """
    try:
        return float(val)
    except ValueError:
        return None


def read_batch(rows: Iterable, batch_size: int = 1) -> Iterable:
    """
    Reads batches of elements from an iterable.

    Args:
        rows: The iterable to read from
        batch_size: The max size of the batches.
    
    Returns:
        An iterator over batches of elements of the original iterable.
    """
    batch = []

    for row in rows:
        batch.append(row)

        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch
