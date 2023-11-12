import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'invoicesai',
    'password': '1234',
    'database': 'invoices_ai',
}

def client_search_by_keyword(keyword):
    result = {}
    connection = mysql.connector.connect(**db_config)

    try:
        cursor = connection.cursor()
        query = "SELECT * FROM clients WHERE name LIKE %s"
        cursor.execute(query, ('%' + keyword + '%',))
        records = cursor.fetchall()

        if records:
            for item in records:
                result[f"client:{item[0]}"] = f"Name: {item[1]}"
            result["client:new"] = "New Client"

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

        return result