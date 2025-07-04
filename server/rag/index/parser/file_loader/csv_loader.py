import os
import pandas as pd

from server.logger.logger_config import my_logger as logger
from server.rag.index.parser.file_loader.fitz_loader import PyMuPdfLoader

USE_LLAMA_PARSE = int(os.getenv('USE_LLAMA_PARSE', 0))
LLAMA_CLOUD_API_KEY = os.getenv('LLAMA_CLOUD_API_KEY')


class AsyncCsvLoader:
    def __init__(self, file_path: str) -> None:
        logger.info(f"[FILE LOADER] init csv/pdf, file_path: '{file_path}'")
        self.file_path = file_path

    async def get_content(self) -> str:
        try:
            content = ''

            # Dacă este setat USE_LLAMA_PARSE, folosim loaderul local PyMuPdfLoader pentru PDF-uri
            if USE_LLAMA_PARSE and self.file_path.lower().endswith('.pdf'):
                loader = PyMuPdfLoader(self.file_path)
                content = loader.load()

            # Pentru CSV-uri normale
            elif self.file_path.lower().endswith('.csv'):
                df = pd.read_csv(self.file_path)
                content = df.to_markdown(index=False)

            else:
                logger.warning(f"Unsupported file type: {self.file_path}")

            if not content:
                logger.warning(f"file_path: '{self.file_path}' is empty!")
            return content
        except Exception as e:
            logger.error(f"get_content is failed, exception: {e}")
            return ''
