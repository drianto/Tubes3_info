class LevenshteinFuzzy:
    def _levenshtein_distance(self, s1, s2):
        len_s1, len_s2 = len(s1), len(s2)
        dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

        for i in range(len_s1 + 1):
            dp[i][0] = i
        for j in range(len_s2 + 1):
            dp[0][j] = j

        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,        # deletion
                    dp[i][j - 1] + 1,        # insertion
                    dp[i - 1][j - 1] + cost  # substitution
                )

        return dp[len_s1][len_s2]

    def _levenshtein_distance_limit(self, s1, s2, max_dist):
        len_s1, len_s2 = len(s1), len(s2)
        if abs(len_s1 - len_s2) > max_dist:
            return max_dist + 1

        prev_row = list(range(len_s2 + 1))
        for i, c1 in enumerate(s1, 1):
            curr_row = [i]
            min_row = i
            for j, c2 in enumerate(s2, 1):
                insert_cost = curr_row[j - 1] + 1
                delete_cost = prev_row[j] + 1
                replace_cost = prev_row[j - 1] + (0 if c1 == c2 else 1)
                cost = min(insert_cost, delete_cost, replace_cost)
                curr_row.append(cost)
                min_row = min(min_row, cost)
            if min_row > max_dist:
                return max_dist + 1
            prev_row = curr_row
        return prev_row[-1]

    def fuzzy_search(self, pattern, text, max_distance=2):
        matches = []
        m = len(pattern)
        for i in range(len(text) - m + 1):
            window = text[i:i + m]
            dist = self._levenshtein_distance_limit(pattern, window, max_distance)
            if dist <= max_distance:
                matches.append((i, window, dist))
        return matches
        # m = len(pattern)
        # best_match = None
        # best_distance = float('inf')
        # matches = []

        # for i in range(len(text) - m + 1):
        #     substring = text[i:i + m]
        #     dist = self._levenshtein_distance(pattern, substring)
        #     if max_distance is None or dist <= max_distance:
        #         matches.append((i, substring, dist))
        #         if dist < best_distance:
        #             best_distance = dist
        #             best_match = (i, substring, dist)

        # return best_match, matches