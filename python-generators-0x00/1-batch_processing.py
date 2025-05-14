import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Fetches user_data in batches from the database.
    Returns a list of batches (each batch is a list of user dicts).
    """
    batches = []

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',  # Replace with your actual password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM user_data")
            total_rows = cursor.fetchone()['total']

            offset = 0
            while offset < total_rows:
                cursor.execute(
                    "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                    (batch_size, offset)
                )
                rows = cursor.fetchall()
                batches.append(rows)
                offset += batch_size

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return batches

def batch_processing(batch_size):
    """
    Processes batches of users and returns those over the age of 25.
    """
    filtered_users = []
    batches = stream_users_in_batches(batch_size)
    
    for batch in batches:
        for user in batch:
            if user['age'] > 25:
                filtered_users.append(user)

    return filtered_users
