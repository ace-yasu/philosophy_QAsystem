from transformers import AutoTokenizer, AutoModel
import torch
import logging

# from road_file import RoadFile

logger = logging.getLogger(__name__)

class Vectorizer:

    def __init__(self):
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        # self.road_file = RoadFile("")

    def vectorize(self, text: str):
        """
        文章をベクトルに変換する

        Args:
            text (str): 文章

        Returns:
            list: ベクトル
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
    
    def pad_vector(self, vector: list, target_length: int):
        """
        ベクトルを指定された長さにパディングする

        Args:
            vector (list): 元のベクトル
            target_length (int): 目標のベクトル長

        Returns:
            list: パディングされたベクトル
        """
        return vector + [0.0] * (target_length - len(vector))
    
    def serve(self, text: str):
        """
        チャンクをベクトル化するためのserveメソッド
        
        Returns:
            function: ベクトル化関数の参照
        """
        logger.info("Vectorizer.serve() called")
        # text = self.road_file.serve()
        vector = self.vectorize(text)
        return vector
    

if __name__ == "__main__":
    from road_file import RoadFile
    road_file = RoadFile("")
    vectorizer = Vectorizer()
    # text = "Now we are developing a new product."
    # text = road_file.serve()
    # vector = vectorizer.vectorize(text)
    # print(vector)
