import mysql.connector

def establish_database_connection():
    db_config = {
        'host': 'localhost',
        'user': 'invoicesai',
        'password': '1234',
        'database': 'invoices_ai',
    }
    connection = mysql.connector.connect(**db_config)
    return connection

def create_mysql_cursor(connection):
    cursor = connection.cursor()
    return cursor

def close_database_connection(connection, cursor):
    cursor.close()
    connection.close()


def client_search_by_keyword(keyword):
    result = {}
    connection = establish_database_connection()
    cursor = create_mysql_cursor(connection)

    try:
        query = "SELECT * FROM clients WHERE company_name LIKE %s OR first_name LIKE %s OR last_name LIKE %s"
        cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
        records = cursor.fetchall()

        if records:
            for item in records:
                result[f"client:{item[0]}"] = f"Name: {item[1]}"
            result["client:new"] = "New Client"

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        close_database_connection(connection, cursor)
        return result

def save_client(client):
    connection = establish_database_connection()
    cursor = create_mysql_cursor(connection)
    insert_query = """
    INSERT INTO clients (company_name, registration_number, vat_number, address, phone_number, email, bank_account, first_name, last_name, type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    client_data = (
        client.get('company_name', ''),
        client.get('registration_number', ''),
        client.get('vat_number', ''),
        client.get('address', ''),
        client.get('phone_number', ''),
        client.get('email', ''),
        client.get('bank_account', ''),
        client.get('first_name', ''),
        client.get('last_name', ''),
        client.get('type', '')
    )
    try:
        cursor.execute(insert_query, client_data)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        close_database_connection(connection, cursor)

def save_invoice(client_id, invoice):
    print("hello world")