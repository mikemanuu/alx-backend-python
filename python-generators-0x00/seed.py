#!/usr/bin/python3
"""
Set up MySQL database and seed it with data from user_data.csv
"""

import uuid
import mysql.connector
from mysql.connector import Error
import csv
import os

""" Connecting to MySQL server """


def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        if connection.is_connected():
            print("Connected to MySQL Server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL Server: {e}")
        return None


""" Creating the ALX_prodev database if it does not exist. """


def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully!")
    except Error as e:
        print(f"Error creating database: {e}")


""" Connecting to the ALX_prodev database. """


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


""" Creating the user_data table if it does not exist. """


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        print("Table user_data ensured.")
    except Error as e:
        print(f"Error creating table: {e}")


""" Inserting data into the user_data table if it does not exist. """


def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        for row in data:
            user_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
        print(f"Inserted {len(data)} records into user_data table.")
    except Error as e:
        print(f"Error inserting data: {e}")


""" Load data from CSV. """


def load_csv_data(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            print(f"Loaded {len(data)} rows from {file_path}")
            return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []


""" Main logic. """


def main():
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

    prodev_connection = connect_to_prodev()
    if prodev_connection:
        create_table(prodev_connection)
        sample_data = load_csv_data("user_data.csv")
        insert_data(prodev_connection, sample_data)
        prodev_connection.close()


if __name__ == "__main__":
    main()
