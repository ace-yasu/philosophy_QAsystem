import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)

class RoadFile:
    def __init__(self, file_path: str):
        load_dotenv()
        self.file_path = os.getenv('FILE_PATH')
        print(f"__init__で読み込まれた環境変数: FILE_PATH={self.file_path}")
        
    def load_file(self, file_path: Optional[str] = None) -> str:
        """
        ファイルからテキストを読み込む
        
        Args:
            file_path (str, optional): ファイルパス。Noneの場合、FILE_PATH環境変数から読み込む
            
        Returns:
            str: file path
            
        Raises:
            ValueError: ファイルパスが指定されておらず、環境変数も設定されていない場合
            FileNotFoundError: 指定されたファイルが存在しない場合
            ValueError: サポートされていないファイル形式の場合
        """
        if not file_path:
            if not self.file_path:
                raise ValueError("ファイルパスが指定されておらず、環境変数も設定されていません")
            file_path = self.file_path

        try:
            # PROJECT_ROOTを使って絶対パスを構築
            project_root = os.getenv('PROJECT_ROOT', os.getcwd())
            
            # ファイルパスが./で始まる場合は相対パス
            if file_path.startswith('./'):
                # 先頭の./を削除して、project_rootと結合
                file_path = file_path[2:]
                abs_path = Path(project_root) / file_path
            else:
                # 絶対パスとして扱う
                abs_path = Path(file_path)
            
            abs_path = abs_path.resolve()
            
            logger.debug(f"ファイルを読み込んでいます: {abs_path}")

            if not abs_path.is_file():
                logger.error(f"ファイルが存在しません: {abs_path}")
                
                if abs_path.parent.exists():
                    files = list(abs_path.parent.glob('*'))
                    logger.info(f"ディレクトリ内のファイル: {[f.name for f in files]}")
                else:
                    logger.error(f"ディレクトリが存在しません: {abs_path.parent}")
                
                raise FileNotFoundError(f"ファイルが見つかりません: {abs_path}")
            abs_path = str(abs_path)
            return abs_path
        
        except Exception as e:
            logger.error(f"ファイル読み込みエラー: {e}")
            raise

    def pdf_to_text(self, file_path: str) -> str:
        """
        PDFファイルをテキストに変換する
        
        Args:
            file_path (str): PDFファイルのパス
            
        Returns:
            str: pdf内のテキスト
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            logger.error(f"PDFファイルのテキスト変換エラー: {e}")
            raise

    def serve(self):
        """
        """
        logger.info("road_file.serve()が呼び出されました")
        try:
            file_path = self.load_file()
            text = self.pdf_to_text(file_path)
            return text
        except Exception as e:
            logger.error(f"ファイル読み込みエラー: {e}")
            raise

if __name__ == "__main__":
    print(f"__main__で読み込まれた環境変数: FILE_PATH={os.getenv('FILE_PATH')}")
    road_file = RoadFile("")
    text = road_file.serve()
    print(f"PDFテキスト: {text}")