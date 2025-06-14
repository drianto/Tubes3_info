from mysql.connector import Error
from connection.db import MySQLConnection
from functions.string_matcher.string_matcher import StringMatcher

import time

from PyPDF2 import PdfReader
import os

class Searcher:
    def __init__(self, connection: MySQLConnection, algo: StringMatcher = None):
        self.connection = connection;
        self.algorithm = algo;

    def set_algorithm(self, algo: StringMatcher):
        self.algorithm = algo;

    def _exact_match(self, target_count):
        results = []
        try:
            with self.connection as cursor:
                cursor.execute("SELECT * FROM ApplicationDetail");
                records = cursor.fetchall();
                if records:
                    for row in records:
                        if(target_count == 0): break
                        path = os.path.abspath(f"../data/{row[3]}")
                        reader = PdfReader(path)
                        found = 0;
                        for page in reader.pages:
                            text = page.extract_text()
                            found += len(self.algorithm.search(text))
                        if(found > 0 ):
                            target_count -= 1
                            results.append((row, found))
                else:
                    print("No records found.")
        except Error as e:
            print(f"Error saat melakukan pencarian: {e}")
        return results

    def _fuzzy_match(self, pattern, target_count):
        pass

    def search(self, pattern, target_count):
        start = time.time()
        self.algorithm.preprocessPattern(pattern)
        res = self._exact_match(target_count)
        end = time.time()

        return (res, (end - start) * 1000)



