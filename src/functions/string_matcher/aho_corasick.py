from functions.string_matcher.string_matcher import StringMatcher
from typing import Optional, Dict, List

class _AhoCorasickState:
    '''Aho-Corasick algorithm automaton state'''

    def __init__(self):
        self.output: Optional[str] = None
        self.transitions: Dict[str, _AhoCorasickState] = {}
        self.link: _AhoCorasickState = self

class AhoCorasick(StringMatcher):
    def __init__(self):
        self.root = None
        self.matches: Dict[str, List[int]] = {}
        self.processed = False

    def preprocessPattern(self, patterns):
        self.root = _AhoCorasickState()
        for pattern in patterns:
            head = self.root
            self.matches[pattern] = []
    
            for c in pattern:
                next = head.transitions.get(c)
    
                if not next:
                    next = _AhoCorasickState()
                    next.link = self.root
                    head.transitions[c] = next
                
                head = next
            
            head.output = pattern
        
        queue: List[_AhoCorasickState] = []
        
        for node in self.root.transitions.values():
            queue.append(node)
            node.link = self.root
    
        while queue:
            current_node = queue.pop(0)
            for key, next_node in current_node.transitions.items():
                queue.append(next_node)
                link = current_node.link
                
                while link and key not in link.transitions:
                    link = link.link

                    if link == link.link:
                        next_node.link = self.root
                        break
                else:
                    next_node.link = link.transitions[key]

    def search(self, pattern, string):
        if not self.processed:
            current = self.root
            for i in range(len(string)):
                c = string[i]
    
                next = current.transitions.get(c)
                link = current
    
                while not next:
                    next = link.transitions.get(c)
    
                    if link == self.root and not next:
                        next = self.root
    
                    link = link.link
    
                current = next
                link = current
    
                while link != self.root:
                    if link.output:
                        self.matches[link.output].append(i - len(link.output) + 1)
                    link = link.link
            
            self.processed = True

        return self.matches[pattern]

if __name__ == "__main__":
    matcher = AhoCorasick()
    patterns = ["amet", "am", "dol", "ip"]
    string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    matcher.preprocessPattern(patterns)
    for pattern in patterns:
        output = matcher.search(pattern, string)
        print(f"{pattern}: {', '.join(string[(i - 3):(i + 3)] for i in output)}")