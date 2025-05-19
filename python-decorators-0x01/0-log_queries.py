#!/usr/bin/env python3
import sqlite3
import functools

def log_queries(func):
    """
    Decorator to log SQL queries before executing them.
    Assumes the first argument passed to the function is the SQL query.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            print(f"[LOG] Executing SQL Query: {args[0]}")
        else:
            print("[LOG] No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Connects to the users.db SQLite database,
    executes the given query, and returns the results.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
