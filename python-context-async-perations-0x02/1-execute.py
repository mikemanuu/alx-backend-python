#!/usr/bin/python3

import mysql.connector


class ExecuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Establish the MySQL database connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="username",
            password="",
            database="ALX_prodev"
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the cursor and the connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self):
        # Execute the query and fetch results
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()


# Usage
query = "SELECT * FROM users WHERE age > %s"
params = (25,)

with ExecuteQuery(query, params) as context_manager:
    result = context_manager.execute()
    print(result)
