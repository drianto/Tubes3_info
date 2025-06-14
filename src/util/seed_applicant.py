import mysql.connector
def main() -> None:
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            database="cv",
            port=3306,
            auth_plugin="caching_sha2_password"
        )
        print("Koneksi berhasil")
        mycursor = mydb.cursor()

        sql = "INSERT INTO ApplicantProfile (applicant_id, first_name, last_name, date_of_birth, address, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (0, "Joe", "Iwok", "1961-05-21", "Surakarta", "0869420")
        mycursor.execute(sql, val)
        mydb.commit()

        print(f"{mycursor.rowcount} record inserted.")
        print(f"ID record terakhir: {mycursor.lastrowid}") # Jika ada auto-increment ID


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

if __name__ == "__main__":
    main()