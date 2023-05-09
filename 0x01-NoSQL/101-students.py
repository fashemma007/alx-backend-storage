#!/usr/bin/env python3
"""Module that houses a function whc students sorted by avg score"""
import pymongo


def top_students(mongo_collection):
    """Python function that returns list of students sorted by avg"""
    return mongo_collection.aggregate([
        {
            '$project': {
                'name': '$name',
                'averageScore': {
                    '$avg': "$topics.score"
                }
            }
        },
        {
            '$sort': {
                "averageScore": -1
            }
        }
    ])
