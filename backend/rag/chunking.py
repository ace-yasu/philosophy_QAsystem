from road_file import RoadFile
from typing import List
import logging
import time

logger = logging.getLogger(__name__)

class Chunker:
    """
    読み込んだテキストのチャンク化を行うクラス。

    主な機能は以下の通り：
    1. road_file.pyで読み込んだテキストを読み込み
    2. テキストを100文字に分割=チャンク化
    3. 次のチャンクのうち最初の25文字は前のチャンクとかぶせる
    4. チャンクのテキストをベクトル化

    
    """
    def __init__(self):
        self.road_file = RoadFile("")  # 環境変数FILE_PATHを使用するため、空文字列を渡す

    def chunk_text(self, text: str) -> List[str]:
        """
        テキストを100文字ずつに分割=チャンク化
        次のチャンクのうち最初の25文字は前のチャンクとかぶせる
        args:
            text: str

        returns:
            List[str]
        """
        try:
            chunks = []
            chunk_size = 100
            overlap = 25
            start = 0

            while start < len(text):
                end = min(start + chunk_size, len(text))
                print(f"now chunk: {end}")
                chunk = text[start:end]
                chunks.append(chunk)
                if end == len(text):
                    break
                start = end - overlap
                # time.sleep(0.1)
            return chunks
            
        except Exception as e:
            raise ValueError(f"チャンク化に失敗しました: {e}")

    def chunk_to_vector(self, chunk: str) -> List[float]:
        """
        チャンクのテキストをベクトル化
        args:
            chunk: str
        returns:
            List[float]
        """


        
    def serve(self):
        text = self.road_file.serve()
        logger.debug(f"テキスト: {text}")
        chunks = chunker.chunk_text(text)
        return chunks

if __name__ == "__main__":
    chunker = Chunker()
    chunks = chunker.serve()
    # text = chunker.road_file.serve()
    # chunks = chunker.chunk_text(text)
    print(chunks)
