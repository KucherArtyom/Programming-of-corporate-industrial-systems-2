# Programming-of-corporate-industrial-systems-2

## Кучер Артем Сергеевич ЭФМО-02-24

### Практика 2 
### Анализатор текстовых файлов (Многопоточное консольное приложение)
### Задание
Необходимо разработать многопоточное консольное приложение, которое анализирует содержимое нескольких текстовых файлов, подсчитывая количество слов и символов в каждом файле. Приложение должно использовать структуры данных, потоки, асинхронное программирование и мьютексы для синхронизации данных.
### Реализуемые задачи
1. Создание структуры данных для хранения результатов анализа:
+ Разработать структуру FileAnalysis, которая хранит имя файла, количество слов и количество символов.
2. Реализация многопоточной обработки файлов:
+ Создать пул потоков для обработки нескольких файлов одновременно.
+ Использовать мьютексы или атомарные переменные для синхронизации доступа к разделяемым данным.
3. Асинхронная обработка файлов:
+ Использовать async/await для чтения содержимого файлов.
+ Обработать ошибки чтения файлов (например, файл не найден, недоступен).
+ Данные должны обрабатываться и считываться.
4. Вывод результатов в консоль:
+ Отобразить список файлов с количеством слов и символов для каждого.
+ Добавить общий итог для всех обработанных файлов.

### Пример использования
```
Введите путь к файлу (или Enter для завершения): D://text.txt

Текущие результаты анализа:
1. D://text.txt: 149 слов, 1315 символов

Итог: 149 слов, 1315 символов.

Введите путь к файлу (или Enter для завершения): D://text1.txt

Текущие результаты анализа:
1. D://text.txt: 149 слов, 1315 символов
2. D://text1.txt: 25 слов, 197 символов

Итог: 174 слов, 1512 символов.

Введите путь к файлу (или Enter для завершения): 

Финальные результаты:

Текущие результаты анализа:
1. D://text.txt: 149 слов, 1315 символов
2. D://text1.txt: 25 слов, 197 символов

Итог: 174 слов, 1512 символов.
```

### Код программы
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
```

#### view.py
```
class ConsoleView:

    # Запрос пути/путей к файлам
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

    # Вывод результатов анализа
    @staticmethod
    def display_results(results, total_words, total_chars):
        print("\nТекущие результаты анализа:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.filename}: {result.word_count} слов, {result.char_count} символов")
        print(f"\nИтог: {total_words} слов, {total_chars} символов.\n")

    # Сообщение, если не было введено пути к файлам
    @staticmethod
    def display_no_files():
        print("\nНе указано ни одного файла для анализа. Программа завершена.")

    # Сообщение об ошибке при обработке
    @staticmethod
    def display_file_error(filepath, error):
        print(f"\nОшибка при обработке файла {filepath}: {error}")

    # Вывод общих результатов
    @staticmethod
    def display_final():
        print("\nФинальные результаты:")
```

#### controller.py
```
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

```

#### file_service.py
```
import aiofiles
from model import FileAnalysis

class FileService:

    # Чтение и анализ файла
    @staticmethod
    async def analyze_file(filepath: str) -> FileAnalysis:
        try:
            async with aiofiles.open(filepath, mode='r', encoding='utf-8') as file:
                content = await file.read()

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
import asyncio

if __name__ == "__main__":
    app = AnalyzerController()
    asyncio.run(app.run())
```
