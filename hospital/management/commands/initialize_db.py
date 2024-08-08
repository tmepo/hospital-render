import psycopg2

hostname = 'dpg-cqqai1d6l47c73ar3lv0-a.oregon-postgres.render.com'  # Full hostname with domain
database = 'hospital_database_i0uo'  # Corrected database name
username = 'hospital_database_i0uo_user'
pwd = 'QyjHNLXDNTEv1jnksT3Khg5v9lXX5KPe'
port_id = 5432

def get_db_connection():
    return psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )

def tables():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        with open('sql/create_tables.sql', 'r') as file:
            cur.execute(file.read())
        conn.commit()
        print("Tables created successfully")
    except Exception as error:
        print(f'The error is: {error}')
    finally:
        if cur is not None:
            cur.close()  # Close the cursor first
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    tables()
