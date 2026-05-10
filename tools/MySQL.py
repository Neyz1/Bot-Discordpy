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
        url VARCHAR(255) NOT NULL UNIQUE,
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

def save_jobs_to_db(jobs: list) -> int:
    """
    Sauvegarde une liste d'objets JobOffer dans la base de données.
    Retourne le nombre de nouvelles offres insérées.
    """
    conn = connect_db()
    if not conn:
        print("[MySQL] Impossible de se connecter à la base de données.")
        return 0

    cursor = conn.cursor()
    inserted = 0

    check_query = "SELECT COUNT(*) FROM offres_creatorsArea WHERE url = %s"
    insert_query = """
    INSERT INTO offres_creatorsArea (url, pricing, username, tags, posted_at)
    VALUES (%s, %s, %s, %s, %s)
    """

    for job in jobs:
        # Extraction du budget depuis le champ company (ex: "Creators Area (Développeur) — 500€")
        budget = 0
        if "—" in job.company:
            budget_str = job.company.split("—")[-1].strip()
            if budget_str.endswith("€"):
                try:
                    budget = int(budget_str.replace("€", "").replace(" ", ""))
                except ValueError:
                    budget = 0

        tags_str = ", ".join(job.tags) if job.tags else ""

        try:
            # Vérifier si l'URL existe déjà
            cursor.execute(check_query, (job.url,))
            exists = cursor.fetchone()[0] > 0

            if not exists:
                cursor.execute(insert_query, (
                    job.url,
                    budget,
                    job.company,
                    tags_str[:20],  # VARCHAR(20)
                    job.posted_at,
                ))
                inserted += 1
        except Error as e:
            print(f"[MySQL] Erreur insertion {job.url}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"[MySQL] {inserted} nouvelle(s) offre(s) insérée(s) sur {len(jobs)}")
    return inserted


def main():
    conn = connect_db()
    
    if conn:
        create_tables(conn)
        conn.close()
        print("Connexion fermée")

if __name__ == "__main__":
    main()
