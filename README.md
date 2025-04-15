# Programming-of-corporate-industrial-systems-2

## Кучер Артем Сергеевич ЭФМО-02-24

### Практика 2

#### model.py
```
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
```

#### view.py
```
class ConsoleView:

    @staticmethod
    def get_file_path() -> list[str]:
        input_paths = input("Введите путь к файлу (или Enter для завершения): ").strip()
        if not input_paths:
            return []

        paths = []
        current_path = []
        in_quotes = False

        for char in input_paths:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_path: 
                    paths.append(''.join(current_path))
                    current_path = []
            else:
                current_path.append(char)

        if current_path: 
            paths.append(''.join(current_path))

        return paths


    @staticmethod
    def display_results(results, total_words, total_chars):
        print("\nТекущие результаты анализа:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.filename}: {result.word_count} слов, {result.char_count} символов")
        print(f"\nИтог: {total_words} слов, {total_chars} символов.\n")

    @staticmethod
    def display_no_files():
        print("\nНе указано ни одного файла для анализа. Программа завершена.")

    @staticmethod
    def display_file_error(filepath, error):
        print(f"\nОшибка при обработке файла {filepath}: {error}")

    @staticmethod
    def display_final():
        print("\nФинальные результаты:")
```

#### controller.py
```
from concurrent.futures import ThreadPoolExecutor
from model import FileAnalyzerModel
from file_service import FileService
from view import ConsoleView
import os


class AnalyzerController:
    def __init__(self):
        self.model = FileAnalyzerModel()
        self.view = ConsoleView()
        self.file_service = FileService()

    def process_single_file(self, filepath: str) -> bool:
        if not filepath:
            return False

        if not os.path.isfile(filepath):
            self.view.display_file_error(filepath, "Файл не найден")
            return True

        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self.file_service.analyze_file, filepath)
                analysis = future.result()
                self.model.add_result(analysis)
        except Exception as e:
            self.view.display_file_error(filepath, str(e))

        self.view.display_results(
            self.model.results,
            self.model.total_words,
            self.model.total_chars
        )
        return True

    def run(self):
        while True:
            filepaths = self.view.get_file_path()
            if not filepaths:
                break

            for filepath in filepaths:
                if not self.process_single_file(filepath):
                    break

        if not self.model.results:
            self.view.display_no_files()
        else:
            self.view.display_final()
            self.view.display_results(
                self.model.results,
                self.model.total_words,
                self.model.total_chars
            )
```

#### file_service.py
```
from model import FileAnalysis


class FileService:
    @staticmethod
    def analyze_file(filepath: str) -> FileAnalysis:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            words = len(content.split())
            chars = len(content)

            return FileAnalysis(
                filename=filepath,
                word_count=words,
                char_count=chars
            )
        except Exception as e:
            raise Exception(f"Ошибка при обработке файла: {str(e)}")
```

#### main.py
```
from controller import AnalyzerController


if __name__ == "__main__":
    app = AnalyzerController()
    app.run()
```
