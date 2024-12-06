#!/usr/bin/python3

import sqlite3
import functools

# Decorator to log SQL queries


def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0] if args else None
        if query:
            print(f"Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

# Function to fetch all users from the database while logging the query


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Usage: Fetch users while logging the query
query = "SELECT * FROM users"
users = fetch_all_users(query=query)
print(users)
