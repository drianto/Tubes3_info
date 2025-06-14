from mysql.connector import Error

import mysql.connector

class MySQLConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MySQLConnection, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.connection = None

    def connect(self, host, database, user, password):
        if not self.connection:
            try:
                self.connection = mysql.connector.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=password
                )
                if self.connection.is_connected():
                    print("Terhubung ke MySQL database")
            except Error as e:
                print(f"Error saat menghubungkan MySQL: {e}")
                self.connection = None

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Koneksi MySql ditutup")
            self.connection = None
    def __enter__(self):
        """
        Memperoleh koneksi dari pool saat masuk ke blok 'with'.
        """
        try:
            self.cursor = self.connection.cursor()
            return self.cursor
        except Error as e:
            print(f"Error mengambil kursor: {e}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Menangani commit/rollback dan mengembalikan koneksi ke pool saat keluar dari blok 'with'.
        """
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
                print(f"Terjadi error. Melakukan Rollback: {exc_val}")

            if self.cursor:
                self.cursor.close()