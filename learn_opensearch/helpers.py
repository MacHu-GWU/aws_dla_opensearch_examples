# -*- coding: utf-8 -*-

"""
Put common operations into python function.
"""

from opensearchpy import OpenSearch


def create_index(es: OpenSearch, index: str, body: dict = None):
    """
    create index if not exists
    """
    return es.indices.create(index=index, body=body, ignore=400)


def delete_index(es: OpenSearch, index: str):
    """
    delete index if exists
    """
    return es.indices.delete(index=index, ignore=[400, 404])


def reset_index(es: OpenSearch, index: str, body: dict = None):
    """
    delete and recreate an index
    """
    delete_index(es, index)
    create_index(es, index, body)
