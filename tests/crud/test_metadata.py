import pytest
import uuid

from app.core.database import collection
from app.crud.metadata import *


@pytest.fixture(name="collection")
def collection_fixture():
    yield collection


id = uuid.uuid4()
title = 'Test Title'


def test_create_paper(collection):
    src_data = {
        'title': title,
        'abstract': 'This is the abstract of the paper',
        'body': [{
            'paragraph_id': 1,
            'section': 'Introduction',
            'text': 'Hello world!'
        }, {
            'paragraph_id': 1999,
            'section': 'References',
            'text': 'Reference Paper'
        }],
        'impact': 100,
        'published_year': '2000',
        'reference': ['Paper 1', 'Paper 2'],
        'figures': [{
            'idx': 0,
            'name': 'fig 1.1',
            'caption': 'caption for fig 1.1',
            'related': [5, 10, 15],
            'summary': 'summary for fig 1.1'
        }],
        'tables': [],
        'authors': ['John', 'Doe']
    }
    data = Metadata(**src_data)
    result = create_metadata(collection, id, data)

    assert result.inserted_id == id


def test_get_metadata_by_id(collection):
    result = get_metadata_by_id(collection, id)
    
    assert title == result.title
