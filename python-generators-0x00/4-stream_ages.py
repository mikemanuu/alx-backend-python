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


def stream_user_ages():
    """
    A generator that streams user ages from the database one by one.
    Yields:
        age (float): Age of each user in the user_data table.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # Unpacking tuple for each row
            yield age  # Yield each age one by one

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def calculate_average_age():
    """
    Calculates the average age of users using the stream_user_ages generator.
    Returns:
        float: The average age of the users.
    """
    total_age = 0
    count = 0

    # Using the generator to get user ages and compute the sum and count
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        return 0  # To handle the case where there are no users

    return total_age / count  # Return the average age


# Usage
if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")
