#!/usr/bin/python3

import mysql.connector


def connect_to_prodev():
    """
    Connects to the ALX_prodev MySQL database.
    Returns:
        connection: A MySQL connection object.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def paginate_users(page_size, offset):
    """
    Fetches a specific page of data from the user_data table.

    Args:
        page_size (int): Number of rows per page.
        offset (int): Offset for the SQL query.
    Returns:
        list: A page of rows from the user_data table.
    """
    connection = connect_to_prodev()
    if not connection:
        return []

    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        cursor.execute(query)
        page = cursor.fetchall()
        return page
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def lazy_paginate(page_size):
    """
    A generator function that lazily loads data one page at a time.

    Args:
        page_size (int): Number of rows per page.
    Yields:
        list: A page of rows from the user_data table.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Stop if no more data
            break
        yield page
        offset += page_size  # Move to the next page


# Usage
if __name__ == "__main__":
    PAGE_SIZE = 5  # Adjust as needed
    print("Fetching paginated data lazily:")
    for page in lazy_paginate(PAGE_SIZE):
        print("Page:")
        for row in page:
            print(row)
