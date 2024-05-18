import os
import numpy as np
from numpy.linalg import norm
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer


# Environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')

# Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
index_raw = pc.Index('prototype')


def fetch_all_by_id(
    ids: list[str]
) -> list[dict]:
    """Fetches all vectors with given IDs.
    
    Args:
        ids: A list strings representing the ID of each vector.

    Returns:
        A list of dict, each containing ID and np.ndarray embedding values. For 
        example:

        [{
            'id': '2d55992d-2c6c-4d04-b52c-d90d75765ffe',
            'vector': array([ ... ])
        } ,{
            'id': '2eb6176a-ce47-48c9-af08-3c2aa742d6fa',
            'vector': array([ ... ])
        }]
    """
    results = index_raw.fetch(ids=ids, namespace="raw_v2")["vectors"]
    
    return [{
        "id": results[id]["id"],
        "vector": np.asarray(results[id]["values"]),
    } for id in results]


def cosine_similarity(
    a: np.ndarray,
    b: np.ndarray
) -> float:
    """Calculates cosine similarity of two vectors."""
    return np.dot(a, b) / (norm(a) * norm(b))


def rank_by_similarity(
    src: np.ndarray,
    tgt: list[dict],
    k: int
) -> list[str]:
    """Filters vector by similarity score.
    
    Args:
        src: A single source vector.
        tgt: A list of dict, each containing ID and embedding of the vector.
        k: Number of elements to return.

    Returns:
        A list of strings representing the ID of top K vectors.
    """
    tgt.sort(
        reverse=True,
        key=lambda x: cosine_similarity(src, x["vector"]))
    
    return [vec["id"] for vec in tgt[:k]]
