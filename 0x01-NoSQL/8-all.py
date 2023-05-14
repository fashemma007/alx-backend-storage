#!/usr/bin/env python3
"""a Python function that lists all documents in a collection and
returns an empty list if no document in the collection mongo_collection will be
the pymongo collection object
"""


def list_all(mongo_collection):
    """Return list of all docs in collection"""
    # Collection objects do not implement truth value testing or bool()
    # hence we use None to compare instead
    if mongo_collection is None:
        return []
    docs = mongo_collection.find()
    return list(docs)
