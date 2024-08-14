import psycopg2

db_params = {
    'dbname': 'dlaibd',
    'user': 'dlaibd',
    'password': 'dlaibd',
    'host': 'localhost',
    'port': '5432'
}

create_table_query = """
CREATE TABLE dlaibd (
    id SERIAL PRIMARY KEY,
    role VARCHAR(255),
    request TEXT,
    socketid BIGINT
);
"""
insert_data_query = """
INSERT INTO dlaibd (role, request, socketid) VALUES (%s, %s, %s);
"""

def start_bd():
    try:
        conn = psycopg2.connect(**db_params)
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def insert_into_bd(role: str,request: str,id: int):
    try:
        conn = psycopg2.connect(**db_params)
        with conn.cursor() as cursor:
            cursor.execute(insert_data_query,(role,request,id))
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def fetch_records(socket_id):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    query = '''
    SELECT id, role, request, socketid
    FROM your_table_name
    WHERE socketid = %s
    ORDER BY id;
    '''

    cursor.execute(query, (socket_id,))    
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return records
