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
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None


def stream_users():
    """
    A generator function that fetches rows from the user_data table one by one.
    Yields:
        tuple: A row from the user_data table.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")

        # Yield rows one by one
        for row in cursor:
            yield row
    finally:
        # Ensure the database connection is closed
        if connection.is_connected():
            cursor.close()
            connection.close()
