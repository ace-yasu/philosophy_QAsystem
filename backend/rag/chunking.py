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
        # Circular importを避けるため、RoadFileクラスのインポートをここでは行わない
        pass

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
            raise ValueError(f"failed to chunk text: {e}")

    def chunk_to_vector(self, chunk: str) -> List[float]:
        """
        args:
            chunk: str
        returns:
            List[float]
        """


    def serve(self):
        # Circular importを避けるため、ここでインポート
        from rag.road_file import RoadFile
        # serveメソッド内でRoadFileをインスタンス化
        road_file = RoadFile("")
        text = road_file.serve()
        logger.debug(f"テキスト: {text}")
        chunks = self.chunk_text(text)
        return chunks

if __name__ == "__main__":
    chunker = Chunker()
    text = "これはテスト用のテキストです。チャンク化のテストを行います。100文字以上のテキストを用意して、正しくチャンク化されるかを確認します。テキストの分割とオーバーラップが正しく機能しているかを検証するためのサンプルテキストです。"
    chunks = chunker.chunk_text(text)
    print(chunks)
