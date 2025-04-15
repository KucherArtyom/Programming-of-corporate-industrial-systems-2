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
        self.view.display_welcome()

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