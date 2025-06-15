from functions.string_matcher.string_matcher import StringMatcher

class KnuthMorrisPratt(StringMatcher):
    def __init__(self):
        self.preprocessedPattern = {}

    def preprocessPattern(self, patterns):
        self.preprocessedPattern.clear()

        for pattern in patterns:
            m = len(pattern)
            border = [0] * m

            j = 0
            i = 1
            while i < m:
                if pattern[i] == pattern[j]:
                    j += 1
                    border[i] = j
                    i += 1
                else:
                    if j != 0:
                        j = border[j - 1]
                    else:
                        border[i] = 0
                        i += 1
            self.preprocessedPattern[pattern] = border

    def search(self, pattern, string):
        n = len(string)
        m = len(pattern)

        res = []

        i = 0
        j = 0

        border = self.preprocessedPattern[pattern]

        while i < n:
            if string[i] == pattern[j]:
                i += 1
                j += 1

                if j == m:
                    res.append(i - j)

                    j = border[j - 1]

            else:
                if j != 0:
                    j = border[j - 1]
                else:
                    i += 1
        return res