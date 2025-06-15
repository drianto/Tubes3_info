from abc import ABC, abstractmethod

class StringMatcher(ABC):
    @abstractmethod
    def preprocessPattern(self, patterns):
        pass

    @abstractmethod
    def search(self, pattern, string):
        pass