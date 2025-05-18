import os
import logging
from dotenv import load_dotenv
from pathlib import Path
import argparse

from rag.road_file import RoadFile
from rag.chunking import Chunker
from rag.vector import Vectorizer
from db.models import Embedding, Base
from sqlalchemy import create_engine
from sqlalchemy.sql import text as text_sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class PhilosophyQAsystem:
    """
    main class for Philosophy QA system
    manage the flow of the system, and coordinate each component
    """
    def __init__(self):
        load_dotenv()

        self.road_file = RoadFile("")
        self.chunker = Chunker()
        self.vectorizer = Vectorizer()

        self.engine = self._connect_db()

        logger.info("Philosophy QA system initialized")

    def _connect_db(self):
        """
        PostgreSQLデータベースへの接続を確立する
        """
        try:
            user = os.getenv("POSTGRES_USER", "POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD", "POSTGRES_PASSWORD")
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("POSTGRES_DB", "philosophy_db")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise e

        database_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        return create_engine(database_url, echo=True)

    def _save_vectors(self, book, text, vector):
        engine = self._connect_db()

        # リストを文字列に変換
        sentence_str = str(text) if isinstance(text, list) else text
        cleaned_text = sentence_str.replace('\x00', '')
        # ベクトルをパディング
        # vector = self.vectorizer.pad_vector(vector, 1536)
        
        with engine.connect() as connection:
            connection.execute(
                text_sql(
                    """
                    INSERT INTO embeddings (book, text, embedding, created_at, updated_at)
                    VALUES (:book, :text, :embedding, NOW(), NOW())
                    """
                ),
                {"book": book, "text": cleaned_text, "embedding": vector}
            )
            connection.commit()
            logger.debug(f"Saved vector for text from {book}")


    def process_document(self, file_path=None, book_name=None):
        """
        process the document and save the vector to the database
        1. load the document
        2. extract text from the document
        3. chunk the text 100 characters with overlap of 25 characters
        4. vectorize the chunked text
        5. save the vector to the database
        """
        try:

            chunks = self.chunker.serve()
            logger.debug(f"chunks: {len(chunks)}")
            logger.debug(f"type chunks: {type(chunks)}")
            
            # vectors = self.vectorizer.vectorize
            # logger.debug(f"vectors")

            logger.info("Document processed successfully")
            
            try:
                for i, chunk in enumerate(chunks):
                    vector = self.vectorizer.vectorize(chunk)
                    logger.debug(f"vector {i}")
                    # logger.debug(f"vector: {type(vector)}")
                
                    self._save_vectors(book_name, chunk, vector)
                    logger.debug(f"Saved vector {i}")
            except Exception as e:
                logger.error(f"Error saving vectors: {e}")
                return False

            logger.debug(f"Document processed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return False
        
    def serve(self, file_path=None, book_name="論理哲学論考"):
        """
        serve the document
        """
        try:
            self.process_document(file_path, book_name)
        except Exception as e:
            logger.error(f"Error serving document: {e}")

if __name__ == "__main__":
    system = PhilosophyQAsystem()
    system.serve()
    # logger.debug("calling file")
    # from rag.road_file import RoadFile
    # road_file = RoadFile("")
    # print(road_file.serve())