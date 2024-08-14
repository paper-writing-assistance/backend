import re

import torch

from app.core.config import settings


def cosine_similarity(a: torch.Tensor, b: torch.Tensor) -> float:
    """
    Computes the cosine similarity between two tensors.
    """
    cos = torch.nn.CosineSimilarity(dim=0, eps=1e-8)
    return cos(a, b).item()


def create_embedding(d: dict) -> torch.Tensor:
    """
    Creates an embedding from a dictionary using the configured 
    embedding model.
    """
    return settings.EMBEDDING_MODEL.encode(d)


def normalize_text(s: str) -> str:
    """
    Normalizes the input text by stripping whitespace, removing 
    non-alphanumeric characters, and converting to lowercase.
    """
    s = s.strip()
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return s
