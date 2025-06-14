from functions.string_matcher.string_matcher import StringMatcher

class KnuthMorrisPratt(StringMatcher):
    def __init__(self):
        self.pattern = ""
        self.border = []
        self.m = 0

    def preprocessPattern(self, pattern):
        self.pattern = pattern

        self.m = len(self.pattern)
        self.border = [0] * self.m

        j = 0
        i = 1
        while i < self.m:
            if self.pattern[i] == self.pattern[j]:
                j += 1
                self.border[i] = j
                i += 1
            else:
                if j != 0:
                    j = self.border[j - 1]
                else:
                    self.border[i] = 0
                    i += 1

    def search(self, string):
        n = len(string)

        res = []

        i = 0
        j = 0

        while i < n:
            if string[i] == self.pattern[j]:
                i += 1
                j += 1

                if j == self.m:
                    res.append(i - j)

                    j = self.border[j - 1]

            else:
                if j != 0:
                    j = self.border[j - 1]
                else:
                    i += 1
        return res