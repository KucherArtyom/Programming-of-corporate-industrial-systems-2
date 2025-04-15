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