import abc
import numpy as np
import torch

from adapters import AutoAdapterModel
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer


class Embedding(metaclass=abc.ABCMeta):
    """
    Interface for embedding model
    """

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def encode(self, text: dict) -> torch.Tensor:
        raise NotImplementedError
    
    @abc.abstractmethod
    def encode_query(self, text: dict) -> torch.Tensor:
        raise NotImplementedError
    

class ParaphraseAlbert(Embedding):
    """
    SentenceTransformer implementation for `Embedding`
    """

    def __init__(self):
        model_name = "paraphrase-albert-small-v2"
        self.model = SentenceTransformer(model_name)

    def encode(self, text: dict) -> torch.Tensor:
        text_batch = ["".join([text[k] for k in text])]
        emb: np.ndarray = self.model.encode(text_batch)[0]
        return torch.from_numpy(emb)
    
    def encode_query(self, text: dict) -> torch.Tensor:
        return self.encode(text)


class Specter2(Embedding):
    """
    SPECTER2 implementation for `Embedding`
    """

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("allenai/specter2_base")
        
        # Embed candidate papers
        self.model = AutoAdapterModel.from_pretrained(
            "allenai/specter2_base")
        self.adapter_name = self.model.load_adapter(
            "allenai/specter2", source="hf", set_active=True)
        
        # Embed short adhoc queries
        self.query_model = AutoAdapterModel.from_pretrained(
            "allenai/specter2_base")
        self.query_adapter_name = self.query_model.load_adapter(
            "allenai/specter2_adhoc_query", source="hf", set_active=True)
        
    def embed_input(self, model, text: dict):
        # preprocess the input
        text_batch = [self.tokenizer.sep_token.join([text[k] for k in text])]

        inputs = self.tokenizer(
            text_batch, padding=True, truncation=True, return_tensors="pt", 
            return_token_type_ids=False, max_length=512)
        
        output = model(**inputs)

        return output.last_hidden_state[:, 0, :][0]
    
    def encode(self, text: dict) -> torch.Tensor:
        return self.embed_input(self.model, text)

    def encode_query(self, text: dict) -> torch.Tensor:
        return self.embed_input(self.query_model, text)
    