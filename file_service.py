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