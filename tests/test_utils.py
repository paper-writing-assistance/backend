import pytest
import torch

from app.utils import *


def test_cosine_similarity():
    a = torch.tensor([0, 1, 1], dtype=torch.float64)
    b = torch.tensor([1, 0, 1], dtype=torch.float64)
    c = torch.tensor([2, 0, 2], dtype=torch.float64)

    assert cosine_similarity(a, b) == pytest.approx(0.5)
    assert cosine_similarity(b, c) == pytest.approx(1)
    assert cosine_similarity(c, a) == pytest.approx(0.5)


def test_create_embedding():
    paper = {
        'title': 'BERT', 
        'abstract': 'We introduce a new language representation model'
    }
    embedding = create_embedding(paper)
    
    assert type(embedding) == torch.Tensor
    assert len(embedding) == 768


def test_normalize_text():
    text1 = "   Some-RANDO-\nM!?# t--ext "
    text2 = "some random text"

    assert normalize_text(text1) == normalize_text(text2)
