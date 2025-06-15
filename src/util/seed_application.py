import mysql.connector
import os
from pathlib import Path

DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'database': "cv",
    'port': 3306,
    'auth_plugin': 'caching_sha2_password'
}

BASE_DIR = Path(__file__).resolve().parent.parent.parent # root folder
DATA_FOLDER = BASE_DIR / "data"

def insert_application_detail(cursor, applicant_id, application_role, cv_path):
    sql = """
    INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(sql, (applicant_id, application_role, str(cv_path)))
        print(f"Inserted: Role='{application_role}', CV='{cv_path}'")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        # dont rolllback here
        raise

def main():
    mydb = None
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        if mydb.is_connected():
            print("Koneksi database berhasil!")
            mycursor = mydb.cursor()

            if not DATA_FOLDER.is_dir():
                print(f"Error: Folder data tidak ditemukan di '{DATA_FOLDER}'")
                return

            print(f"\nTraversing folder: {DATA_FOLDER}")
            records_inserted = 0

            for root, dirs, files in os.walk(DATA_FOLDER):
                if Path(root) != DATA_FOLDER:
                    application_role = Path(root).name

                    for file in files:
                        if file.lower().endswith('.pdf'):
                            full_cv_path = Path(root) / file
                            applicant_id = 0
                            cv_path_relative = full_cv_path.relative_to(DATA_FOLDER)

                            insert_application_detail(mycursor, applicant_id, application_role, cv_path_relative)
                            records_inserted += 1

            mydb.commit()
            print(f"\nProses selesai. Total {records_inserted} record berhasil dimasukkan.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        if mydb and mydb.is_connected():
            mydb.rollback()
            print("Transaksi di-rollback.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if mydb and mydb.is_connected():
            mydb.rollback
            print("Transaksi di-rollback karena error tidak terduga.")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()
            print("Koneksi database ditutup.")

if __name__ == "__main__":
    main()