# -*- coding: utf-8 -*-

"""
Ref:

- https://opensearch.org/docs/latest/opensearch/rest-api/document-apis/bulk/
"""

import time
from rich import print
from opensearchpy.helpers import bulk
from learn_opensearch.connection import oss
from learn_opensearch.timer import DateTimeTimer

index = "bulk_api_test"


def e00_reset_index():
    # delete if exists
    oss.indices.delete(index=index, ignore=[400, 404])

    # create if exists
    oss.indices.create(index=index, ignore=400)


def e01_one_by_one_index():
    # make sure index are empty
    query_search_all = {"query": {"match_all": {}}}
    oss.delete_by_query(index=index, body=query_search_all)
    time.sleep(1)

    print("--- before index ---")
    res = oss.count(index=index, body=query_search_all)
    print(res)

    n = 50
    with DateTimeTimer("one-by-one index"):
        for i in range(1, 1 + n):
            oss.index(index=index, id=i, body={"name": f"user_{i}"})
    time.sleep(1)

    print("--- after index ---")
    res = oss.count(index=index, body=query_search_all)
    print(res)


def e02_bulk_index():
    """
    Concepts:

    1. generator can save memory use.
    2. action has additional information other than the document.
    """
    # make sure index are empty
    query_search_all = {"query": {"match_all": {}}}
    oss.delete_by_query(index=index, body=query_search_all)
    time.sleep(1)

    print("--- before index ---")
    res = oss.count(index=index, body=query_search_all)
    print(res)

    def gen_actions():
        n = 1000
        for i in range(1, 1 + n):
            yield {
                "_index": index,
                "_id": i,
                "_source": {
                    "name": f"user_{i}",
                }
            }

    with DateTimeTimer("bulk index"):
        res = bulk(oss, gen_actions())

    time.sleep(3)  # it takes more time to make all bulk inserted documents available

    print("--- after index ---")
    res = oss.count(index=index, body=query_search_all)
    print(res)


if __name__ == "__main__":
    # e00_reset_index()
    # e01_one_by_one_index()
    # e02_bulk_index()
    pass
