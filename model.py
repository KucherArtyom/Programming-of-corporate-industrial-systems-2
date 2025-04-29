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
        self.results: List[FileAnalysis] = [] # Cписок для хранения объектов FileAnalysis
        self.lock = Lock() #Объект Lock для потокобезопасного доступа к результатам
        self.total_words = 0
        self.total_chars = 0

    # Добавление результатов в общий список
    def add_result(self, analysis: FileAnalysis):
        with self.lock:
            self.results.append(analysis)
            self.total_words += analysis.word_count
            self.total_chars += analysis.char_count