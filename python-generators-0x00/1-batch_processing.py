import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that fetches user_data in batches from the database.
    Yields lists of user dictionaries in chunks of batch_size.
    """
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
            while offset < total_rows:  # Loop #1
                cursor.execute(
                    "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                    (batch_size, offset)
                )
                rows = cursor.fetchall()
                yield rows
                offset += batch_size

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size):
    """
    Processes batches of users and yields those over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop #2
        for user in batch:  # Loop #3
            if user['age'] > 25:
                yield user
