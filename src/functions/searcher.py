from mysql.connector import Error
from connection.db import MySQLConnection
from functions.string_matcher.string_matcher import StringMatcher
from functions.levenshtein_fuzzy import LevenshteinFuzzy
from functions.pdf_reader import PDFReader

import time

from PyPDF2 import PdfReader
import os

class Searcher:
    def __init__(self, connection: MySQLConnection, algo: StringMatcher = None):
        self.connection = connection;
        self.exact_algo = algo;
        self.fuzzy_algo = LevenshteinFuzzy()
        self.pdf_reader = PDFReader()

    def set_algorithm(self, algo: StringMatcher):
        self.exact_algo = algo;

    def _exact_match(self, patterns, target_count):
        results = {}
        try:
            with self.connection as cursor:
                cursor.execute("SELECT * FROM ApplicationDetail");
                records = cursor.fetchall();

                if not records:
                    print("No records found.")
                    return

                for row in records:

                    # if(target_count == 0): break

                    path = os.path.abspath(f"../{row[3]}")
                    print("reading ", path)

                    text = self.pdf_reader.open_pdf(path)

                    occurences = {key: 0 for key in patterns}
                    has_found = False
                    for pattern in patterns:
                        found = len(self.exact_algo.search(pattern, text))
                        if(found > 0): has_found = True
                        occurences[pattern] += found

                    if(has_found):
                        target_count -= 1
                        results[row[0]] = {"data": row[1:], "occurences": occurences}

        except Error as e:
            print(f"Error saat melakukan pencarian: {e}")

        return results

    def _fuzzy_match(self, results, patterns, target_count):
        try:
            with self.connection as cursor:
                cursor.execute("SELECT * FROM ApplicationDetail");
                records = cursor.fetchall();

                if not records:
                    print("No records found.")
                    return

                for row in records:
                    # if(target_count == 0): break
                    path = os.path.abspath(f"../{row[3]}")
                    print("reading ", path)
                    reader = PdfReader(path)
                    found = 0;
                    create_new = row[0] not in results
                    if create_new:
                        occurences = {key: 0 for key in patterns}
                    text = self.pdf_reader.open_pdf(path)
                    for pattern in patterns:
                        found = len(self.fuzzy_algo.fuzzy_search(pattern, text))

                        if(found > 0):
                            if create_new:
                                occurences[pattern] += found
                            else:
                                results[row[0]]["occurences"][pattern] += found

                    if create_new:
                        results[row[0]] = {"data": row[1:], "occurences": occurences}
                        target_count -= 1

        except Error as e:
            print(f"Error saat melakukan pencarian: {e}")

        return results

    def search(self, patterns, target_count):
        pattern_list = [pattern.strip() for pattern in patterns.split(",")]

        # do exact matching
        exact_start = time.time()
        self.exact_algo.preprocessPattern(pattern_list)
        res = self._exact_match(pattern_list, target_count)
        exact_end = time.time()

        # check total matches
        total_cv_exact = len(res)
        cv_remaining = target_count - total_cv_exact
        if cv_remaining <= 0:
            return (res, (exact_end - exact_start) * 1000, 0)
        print("exact target < target_count")

        # do fuzzy matching if not enough
        fuzzy_start = time.time()
        self._fuzzy_match(res, pattern_list, cv_remaining)
        fuzzy_end = time.time()

        res = dict(sorted(res.items(), key=lambda item: sum(item[1]["occurences"].values()), reverse=True))

        return (res, (exact_end - exact_start) * 1000, (fuzzy_end - fuzzy_start) * 1000)



