import asyncio
from concurrent.futures import ThreadPoolExecutor
from model import FileAnalyzerModel
from file_service import FileService
from view import ConsoleView
import os

class AnalyzerController:
    def __init__(self):
        self.model = FileAnalyzerModel() # Хранение результатов анализа файлов
        self.view = ConsoleView() # Взаимодействие с пользователем через консоль
        self.file_service = FileService() # Чтение и анализа файлов

    #  Синхронная обертка для обработки одного файла. Запускает асинхронную обработку внутри потока.
    def process_single_file_sync(self, filepath: str):
        asyncio.run(self._process_single_file_async(filepath))

    # Асинхронная обработка одного файла: чтение и анализ файла, добавление результатов
    async def _process_single_file_async(self, filepath: str) -> bool:
        if not filepath:
            return False

        if not os.path.isfile(filepath):
            self.view.display_file_error(filepath, "Файл не найден")
            return True

        try:
            analysis = await self.file_service.analyze_file(filepath)
            self.model.add_result(analysis)
        except Exception as e:
            self.view.display_file_error(filepath, str(e))

        self.view.display_results(
            self.model.results,
            self.model.total_words,
            self.model.total_chars
        )
        return True

    # Многопоточная обработка списка файлов. Для каждого файла запускаем поток, который вызывает синхронную обертку.
    async def process_multiple_files(self, filepaths: list[str]):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            tasks = [
                loop.run_in_executor(pool, self.process_single_file_sync, filepath)
                for filepath in filepaths
            ]
            await asyncio.gather(*tasks)

    # Запрос путей к файлам у пользователя, обработка и вывод результатов
    async def run(self):
        while True:
            filepaths = self.view.get_file_path()
            if not filepaths:
                break

            await self.process_multiple_files(filepaths)

        if not self.model.results:
            self.view.display_no_files()
        else:
            self.view.display_final()
            self.view.display_results(
                self.model.results,
                self.model.total_words,
                self.model.total_chars
            )

if __name__ == "__main__":
    controller = AnalyzerController()
    asyncio.run(controller.run())
