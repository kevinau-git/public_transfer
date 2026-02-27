import os 
from difflib import SequenceMatcher

class SimilarityDiff:
    """
    A class for calculating string similarity and coverage scores.
    Supports both English and Chinese text processing.
    """
    
    def __init__(self):
        """Initialize the SimilarityDiff class."""
        pass
    
    def similarity_score(self, a, b, method='levenshtein'):
        """
        Calculate similarity score between two strings.
        
        Args:
            a (str): First string
            b (str): Second string  
            method (str): 'levenshtein', 'jaccard', 'cosine', 'jaro', 'ratio'
        
        Returns:
            int: Similarity score (0-100)
        """
        if a == b:
            return 100
        if not a or not b:
            return 0
        
        if method == 'levenshtein':
            return self._levenshtein_similarity(a, b)
        elif method == 'jaccard':
            return self._jaccard_similarity(a, b)
        elif method == 'cosine':
            return self._cosine_similarity(a, b)
        elif method == 'jaro':
            return self._jaro_similarity(a, b)
        elif method == 'ratio':
            return self._ratio_similarity(a, b)
        else:
            raise ValueError("Method must be 'levenshtein', 'jaccard', 'cosine', 'jaro', or 'ratio'")
    
    def coverage_score(self, a, b, method='character'):
        """
        Calculate coverage score of how much string b covers string a.
        
        Args:
            a (str): Target string to be covered
            b (str): Source string that provides coverage
            method (str): 'character', 'substring', 'word', or 'sequential'
        
        Returns:
            int: Coverage score (0-100)
        """
        if not a:
            return 100  # Empty string is fully covered
        if not b:
            return 0    # Empty source provides no coverage
        
        if method == 'character':
            return self._character_coverage(a, b)
        elif method == 'substring':
            return self._substring_coverage(a, b)
        elif method == 'word':
            return self._word_coverage(a, b)
        elif method == 'sequential':
            return self._sequential_coverage(a, b)
        else:
            raise ValueError("Method must be 'character', 'substring', 'word', or 'sequential'")
    
    # Private similarity methods
    def _levenshtein_similarity(self, a, b):
        """Calculate Levenshtein distance based similarity."""
        def levenshtein_distance(s1, s2):
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)
            if len(s2) == 0:
                return len(s1)
            
            previous_row = list(range(len(s2) + 1))
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            
            return previous_row[-1]
        
        distance = levenshtein_distance(a.lower(), b.lower())
        max_len = max(len(a), len(b))
        similarity = (max_len - distance) / max_len
        return int(similarity * 100)
    
    def _jaccard_similarity(self, a, b):
        """Calculate Jaccard similarity based on character sets."""
        set_a = set(a.lower())
        set_b = set(b.lower())
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return int((intersection / union) * 100) if union > 0 else 0
    
    def _cosine_similarity(self, a, b):
        """Calculate cosine similarity based on character frequency."""
        def char_frequency(text):
            freq = {}
            for char in text.lower():
                freq[char] = freq.get(char, 0) + 1
            return freq
        
        freq_a = char_frequency(a)
        freq_b = char_frequency(b)
        
        # Get all unique characters
        all_chars = set(freq_a.keys()).union(set(freq_b.keys()))
        
        # Create vectors
        vec_a = [freq_a.get(char, 0) for char in all_chars]
        vec_b = [freq_b.get(char, 0) for char in all_chars]
        
        # Calculate cosine similarity
        dot_product = sum(a_val * b_val for a_val, b_val in zip(vec_a, vec_b))
        magnitude_a = sum(val ** 2 for val in vec_a) ** 0.5
        magnitude_b = sum(val ** 2 for val in vec_b) ** 0.5
        
        if magnitude_a == 0 or magnitude_b == 0:
            return 0
        
        cosine_sim = dot_product / (magnitude_a * magnitude_b)
        return int(cosine_sim * 100)
    
    def _jaro_similarity(self, a, b):
        """Calculate Jaro similarity."""
        def jaro_similarity(s1, s2):
            if s1 == s2:
                return 1.0
            
            len1, len2 = len(s1), len(s2)
            if len1 == 0 or len2 == 0:
                return 0.0
            
            match_window = max(len1, len2) // 2 - 1
            if match_window < 0:
                match_window = 0
            
            s1_matches = [False] * len1
            s2_matches = [False] * len2
            matches = 0
            transpositions = 0
            
            # Find matches
            for i in range(len1):
                start = max(0, i - match_window)
                end = min(i + match_window + 1, len2)
                for j in range(start, end):
                    if s2_matches[j] or s1[i] != s2[j]:
                        continue
                    s1_matches[i] = s2_matches[j] = True
                    matches += 1
                    break
            
            if matches == 0:
                return 0.0
            
            # Count transpositions
            k = 0
            for i in range(len1):
                if not s1_matches[i]:
                    continue
                while not s2_matches[k]:
                    k += 1
                if s1[i] != s2[k]:
                    transpositions += 1
                k += 1
            
            return (matches/len1 + matches/len2 + (matches-transpositions/2)/matches) / 3.0
        
        jaro_score = jaro_similarity(a.lower(), b.lower())
        return int(jaro_score * 100)
    
    def _ratio_similarity(self, a, b):
        """Calculate similarity using Python's built-in SequenceMatcher ratio."""
        matcher = SequenceMatcher(None, a.lower(), b.lower())
        return int(matcher.ratio() * 100)
    
    # Private coverage methods
    def _character_coverage(self, a, b):
        """Calculate character-level coverage."""
        a_chars = set(a.lower())
        b_chars = set(b.lower())
        covered_chars = a_chars.intersection(b_chars)
        return int((len(covered_chars) / len(a_chars)) * 100)
    
    def _substring_coverage(self, a, b):
        """Calculate substring coverage."""
        a_lower = a.lower()
        b_lower = b.lower()
        covered_length = 0
        used_positions = set()
        
        # Find longest matches first
        for i in range(len(a)):
            for j in range(i + 1, len(a) + 1):
                substring = a_lower[i:j]
                if substring in b_lower and i not in used_positions:
                    # Check if this position hasn't been used
                    if all(pos not in used_positions for pos in range(i, j)):
                        covered_length += len(substring)
                        used_positions.update(range(i, j))
                        break
        
        return int((covered_length / len(a)) * 100)
    
    def _word_coverage(self, a, b):
        """Calculate word-level coverage."""
        words_a = set(a.lower().split())
        words_b = set(b.lower().split())
        if not words_a:
            return 100
        covered_words = words_a.intersection(words_b)
        return int((len(covered_words) / len(words_a)) * 100)
    
    def _sequential_coverage(self, a, b):
        """Calculate sequential coverage using longest common subsequence."""
        a_lower = a.lower()
        b_lower = b.lower()
        
        # Dynamic programming for longest common subsequence
        dp = [[0] * (len(b_lower) + 1) for _ in range(len(a_lower) + 1)]
        
        for i in range(1, len(a_lower) + 1):
            for j in range(1, len(b_lower) + 1):
                if a_lower[i-1] == b_lower[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return int((dp[len(a_lower)][len(b_lower)] / len(a)) * 100)
    
    # Test methods
    def run_coverage_tests(self):
        """Run coverage test cases."""
        print("=== STRING COVERAGE TESTS ===")
        coverage_cases = [
            ("hello world", "world hello programming", "character"),
            ("hello world", "world hello programming", "substring"), 
            ("hello world", "world hello programming", "word"),
            ("hello world", "world hello programming", "sequential"),
            ("abc", "cba", "character"),
            ("abc", "cba", "sequential"), 
            ("python", "java python code", "word"),
            ("", "anything", "character"),
            ("something", "", "character"),
            # Chinese test cases
            ("你好世界", "世界你好编程", "character"),
            ("你好世界", "世界你好编程", "substring"),
            ("你好 世界", "世界 你好 编程", "word"),
            ("中国人", "人中国", "sequential"),
            ("学习编程", "我在学习Python编程语言", "substring")
        ]
        
        for a, b, method in coverage_cases:
            score = self.coverage_score(a, b, method)
            print(f"'{a}' covered by '{b}' ({method}): {score}%")
    
    def run_similarity_tests(self):
        """Run similarity test cases."""
        print("=== STRING SIMILARITY TESTS ===")
        similarity_cases = [
            ("hello", "hallo", "levenshtein"),
            ("hello", "hallo", "jaccard"),
            ("hello", "hallo", "cosine"),
            ("hello", "hallo", "jaro"),
            ("hello", "hallo", "ratio"),
            ("kitten", "sitting", "levenshtein"),
            ("abc", "def", "levenshtein"),
            ("programming", "program", "ratio"),
            # Chinese similarity tests
            ("你好", "as您好dfdd", "levenshtein"),
            ("中国", "中华", "jaccard"),
            ("编程", "编码", "cosine"),
            ("学习", "学习", "ratio"),
        ]
        
        for a, b, method in similarity_cases:
            score = self.similarity_score(a, b, method)
            print(f"'{a}' vs '{b}' ({method}): {score}%")
    
    def interactive_calculator(self):
        """Run interactive string comparison calculator."""
        while True:
            print("\nString Comparison Calculator")
            print("1. Coverage Score (how much B covers A)")
            print("2. Similarity Score (how similar A and B are)")
            print("3. Exit")
            
            choice = input("Choose option (1-3): ").strip()
            
            if choice == '3':
                break
            elif choice in ['1', '2']:
                string_a = input("Enter string A: ").strip()
                if not string_a:
                    continue
                string_b = input("Enter string B: ").strip()
                
                if choice == '1':
                    print("\nCoverage methods:")
                    print("1. Character coverage")
                    print("2. Substring coverage") 
                    print("3. Word coverage")
                    print("4. Sequential coverage")
                    
                    method_choice = input("Enter choice (1-4): ").strip()
                    method_map = {'1': 'character', '2': 'substring', '3': 'word', '4': 'sequential'}
                    method = method_map.get(method_choice, 'character')
                    
                    score = self.coverage_score(string_a, string_b, method)
                    print(f"\nCoverage Score: {score}%")
                    print(f"Method: {method}")
                    print(f"How much '{string_b}' covers '{string_a}'")
                    
                elif choice == '2':
                    print("\nSimilarity methods:")
                    print("1. Levenshtein (edit distance)")
                    print("2. Jaccard (set similarity)")
                    print("3. Cosine (frequency similarity)")
                    print("4. Jaro (position similarity)")
                    print("5. Ratio (sequence matching)")
                    
                    method_choice = input("Enter choice (1-5): ").strip()
                    method_map = {'1': 'levenshtein', '2': 'jaccard', '3': 'cosine', '4': 'jaro', '5': 'ratio'}
                    method = method_map.get(method_choice, 'levenshtein')
                    
                    score = self.similarity_score(string_a, string_b, method)
                    print(f"\nSimilarity Score: {score}%")
                    print(f"Method: {method}")
                    print(f"How similar '{string_a}' and '{string_b}' are")
            else:
                print("Invalid choice. Please try again.")


# Example usage and testing
if __name__ == "__main__":
    # Create an instance of the class
    analyzer = SimilarityDiff()
    
    # Run test cases
    analyzer.run_coverage_tests()
    print("\n" + "="*50)
    analyzer.run_similarity_tests()
    print("\n" + "="*50)
    
    # Run interactive calculator (uncomment to use)
    # analyzer.interactive_calculator()
