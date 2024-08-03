from pinecone import Index

from app.api.routes.search import select_index
from app.core.db import index
from app.models import PaperQuery
from app.crud import get_vectors_by_ids, create_vector

import uuid


dps: PaperQuery = PaperQuery(
    domain="Computer Vision",
    problem="I have a problem",
    solution="But I've also got a solution"
)

dp: PaperQuery = PaperQuery(
    domain="NLP",
    problem="Some problem"
)

ds: PaperQuery = PaperQuery(
    domain="Deep Learning",
    solution="I have a solution for a problem that I don't know"
)

d: PaperQuery = PaperQuery(
    domain="Machine Learning"
)


def test_insert_vector():
    d_dict = dps.model_dump()
    d_dict.pop("problem")
    d_dict.pop("solution")
    d_from_dps: PaperQuery = PaperQuery(**d_dict)

    dp_dict = dps.model_dump()
    dp_dict.pop("solution")
    dp_from_dps: PaperQuery = PaperQuery(**dp_dict)

    ds_dict = dps.model_dump()
    ds_dict.pop("problem")
    ds_from_dps: PaperQuery = PaperQuery(**ds_dict)

    for item in [d_from_dps, dp_from_dps, ds_from_dps, dps]:
        tgt_index: Index = select_index(item, index)
        test_id: str = str(uuid.uuid4())
        create_vector(tgt_index, test_id, item)
        assert get_vectors_by_ids(tgt_index, [test_id]) is not None
