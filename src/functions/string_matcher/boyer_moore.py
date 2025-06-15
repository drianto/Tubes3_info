from functions.string_matcher.string_matcher import StringMatcher

class BoyerMoore(StringMatcher):
    def __init__(self):
        self.preprocessedPattern = {}

    def preprocessPattern(self, patterns):
        self.preprocessedPattern.clear()

        for pattern in patterns:
            last_occurence = [-1] * 95
            m = len(pattern)
            for i in range(m):
                last_occurence[ord(pattern[i]) - 32] = i

            self.preprocessedPattern[pattern] = last_occurence

    def search(self, pattern, string):
        res = []

        n = len(string)
        m = len(pattern)
        i = 0
        last_occurence = self.preprocessedPattern[pattern]
        while(i <= n-m):
            j = m-1

            while j >= 0 and pattern[j] == string[i+j]:
                j -= 1

            if j < 0:
                res.append(i)

                idx = ord(string[i+m]) - 32
                i += (m - (last_occurence[idx] if idx > -1 and idx < 95 else -1) if i+m < n else 1)
            else:
                idx = ord(string[i+j]) - 32
                i += max(1, j - (last_occurence[idx] if idx > -1 and idx < 95 else -1))
        return res