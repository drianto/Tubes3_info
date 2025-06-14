from functions.string_matcher.string_matcher import StringMatcher

class BoyerMoore(StringMatcher):
    def __init__(self):
        self.last_occurence = []

    def preprocessPattern(self, pattern):
        pass

    def search(self, string):
        pass