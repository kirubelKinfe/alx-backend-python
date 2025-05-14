import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that fetches user_data in batches from the database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM user_data")
            total_rows = cursor.fetchone()['total']

            for offset in range(0, total_rows, batch_size):
                cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {batch_size} OFFSET {offset}")
                rows = cursor.fetchall()
                yield rows

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users and filters out users older than 25.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop #1
        for user in batch:  # Loop #2
            if user['age'] > 25:
                print(user)  # can also use `yield user` if needed
