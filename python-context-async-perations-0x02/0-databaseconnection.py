#!/usr/bin/python3

import mysql.connector


class DatabaseConnection:
    def __init__(self, host, user, password, database):
        """Initialize the connection parameters."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return the cursor."""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the cursor and the connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


# Usage
if __name__ == "__main__":
    # Replace with your MySQL credentials and database
    db_config = {
        "host": "localhost",
        "user": "your_username",
        "password": "your_password",
        "database": "ALX_prodev"
    }

    query = "SELECT * FROM users"

    with DatabaseConnection(**db_config) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

        # Print the results
        for row in results:
            print(row)
