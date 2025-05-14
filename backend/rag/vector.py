from transformers import AutoTokenizer, AutoModel
import torch
import logging

logger = logging.getLogger(__name__)

class Vectorizer:
    """
    文章をベクトルに変換するクラス
    """
    def __init__(self):
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

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
    

if __name__ == "__main__":
    vectorizer = Vectorizer()
    text = "Now we are developing a new product."
    vector = vectorizer.vectorize(text)
    print(vector)
