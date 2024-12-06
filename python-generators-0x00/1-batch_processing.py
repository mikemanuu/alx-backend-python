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


def stream_users_in_batches(batch_size):
    """
    A generator function that fetches rows in batches from the user_data table.

    Args:
        batch_size (int): The number of rows to fetch per batch.
    Yields:
        list: A batch of rows from the user_data table.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.

    Args:
        batch_size (int): The number of rows to fetch and process per batch.
    Yields:
        list: A filtered list of users over the age of 25 from each batch.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user[3] > 25]
        yield filtered_users


# Usage
if __name__ == "__main__":
    BATCH_SIZE = 10  # Adjust as needed
    print("Processing users over the age of 25:")
    for processed_batch in batch_processing(BATCH_SIZE):
        for user in processed_batch:
            print(user)
