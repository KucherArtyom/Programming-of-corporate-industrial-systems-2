class ConsoleView:
    @staticmethod
    def display_welcome():
        print("Введите пути к файлам для анализа (один за другим)")

    @staticmethod
    def get_file_path() -> list[str]:
        input_paths = input("Введите путь к файлу (или Enter для завершения): ").strip()
        if not input_paths:
            return []

        # Разделение путей, учитывая кавычки (для путей с пробелами)
        paths = []
        current_path = []
        in_quotes = False

        for char in input_paths:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_path:  # Добавляем путь, если он не пустой
                    paths.append(''.join(current_path))
                    current_path = []
            else:
                current_path.append(char)

        if current_path:  # Добавляем последний путь
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