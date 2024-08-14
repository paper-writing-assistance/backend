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
    def encode(self, paper: dict) -> torch.Tensor:
        raise NotImplementedError
    

class ParaphraseAlbert(Embedding):
    """
    SentenceTransformer implementation for `Embedding`
    """

    def __init__(self):
        model_name = "paraphrase-albert-small-v2"
        self.model = SentenceTransformer(model_name)

    def encode(self, paper) -> torch.Tensor:
        text_batch = ["".join([paper[k] for k in paper])]
        emb: np.ndarray = self.model.encode(text_batch)[0]
        return torch.from_numpy(emb)


class Specter2(Embedding):
    """
    SPECTER2 implementation for `Embedding`
    """

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("allenai/specter2_base")
        self.model = AutoAdapterModel.from_pretrained("allenai/specter2_base")
        self.adapter_name = self.model.load_adapter(
            "allenai/specter2", source="hf", set_active=True)
    
    def encode(self, paper) -> torch.Tensor:
        text_batch = [self.tokenizer.sep_token.join([paper[k] for k in paper])]
    
        inputs = self.tokenizer(
            text_batch, padding=True, truncation=True, return_tensors="pt", 
            return_token_type_ids=False, max_length=512)
        output = self.model(**inputs)
        
        return output.last_hidden_state[:, 0, :][0]
