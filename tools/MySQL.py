import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "creatorsArea",
    "port": 3306,
    }

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Connecté à MySQL")
            return conn
    except Error as e:
        print(f"Erreur connexion : {e}")
        return None

def create_tables(conn):
    cursor = conn.cursor()

    create_users_table = """
    CREATE TABLE IF NOT EXISTS offres_creatorsArea (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url VARCHAR(255) NOT NULL,
        pricing INT DEFAULT 0, 
        username VARCHAR(50) NOT NULL,
        tags VARCHAR(20),
        posted_at DATETIME NOT NULL
    )
    """

    try:
        cursor.execute(create_users_table)
        conn.commit()
        print("Table créée")
    except Error as e:
        print(f"Erreur création table : {e}")
    finally:
        cursor.close()

def main():
    conn = connect_db()
    
    if conn:
        create_tables(conn)
        conn.close()
        print("Connexion fermée")

if __name__ == "__main__":
    main()