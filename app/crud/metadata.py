import uuid

from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from app.models.metadata import Metadata


# =========================================================
# Create
# =========================================================
def create_metadata(
    collection: Collection, id: uuid.UUID, data: Metadata
) -> InsertOneResult:
    data_dict = data.model_dump()
    data_dict |= {'_id': id}
    result = collection.insert_one(data_dict)
    return result


# =========================================================
# Read
# =========================================================
def get_metadata_by_id(collection: Collection, id: uuid.UUID) -> Metadata:
    result = collection.find_one({'_id': id})
    return Metadata.model_validate(result)
