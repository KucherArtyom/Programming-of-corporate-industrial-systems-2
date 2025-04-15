from dataclasses import dataclass
from typing import List
from threading import Lock


@dataclass
class FileAnalysis:
    filename: str
    word_count: int = 0
    char_count: int = 0


class FileAnalyzerModel:
    def __init__(self):
        self.results: List[FileAnalysis] = []
        self.lock = Lock()
        self.total_words = 0
        self.total_chars = 0

    def add_result(self, analysis: FileAnalysis):
        with self.lock:
            self.results.append(analysis)
            self.total_words += analysis.word_count
            self.total_chars += analysis.char_count