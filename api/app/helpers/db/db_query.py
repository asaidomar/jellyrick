def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

