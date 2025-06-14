from functions.string_matcher.string_matcher import StringMatcher

class BoyerMoore(StringMatcher):
    def __init__(self):
        self.last_occurence = []
        self.m = 0
        self.pattern = ""

    def preprocessPattern(self, pattern):
        self.pattern = pattern
        self.last_occurence = [-1] * 95
        self.m = len(pattern)
        for i in range(self.m):
            self.last_occurence[ord(pattern[i]) - 32] = i

    def search(self, string):
        res = []

        n = len(string)
        i = 0
        while(i <= n-self.m):
            j = self.m-1

            while j >= 0 and self.pattern[j] == string[i+j]:
                j -= 1

            if j < 0:
                res.append(i)

                idx = ord(string[i+self.m]) - 32
                i += (self.m - (self.last_occurence[idx] if idx > -1 and idx < 95 else -1) if i+self.m < n else 1)
            else:
                idx = ord(string[i+j]) - 32
                i += max(1, j - (self.last_occurence[idx] if idx > -1 and idx < 95 else -1))
        return res