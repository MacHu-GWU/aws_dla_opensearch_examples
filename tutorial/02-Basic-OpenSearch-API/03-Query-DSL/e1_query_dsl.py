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

index = "query_dsl_test"


def e01_term_query_exact_match():
    """
    knowledge:

    1. term is similar to ``WHERE column = value`` in SQL
    2. term usually work with ``long`` and ``keyword``
    3. term is case sensitive by default
    """
    body = {
        "query": {
            "term": {
                "owner_ssn": {
                    "value": "588-29-4214"
                }
            }
        }
    }
    res = oss.search(index=index, body=body)
    print(res)


def e02_term_query_exact_match_case_insensitive():
    """
    knowledge

    1. you can use ``case_insensitive`` parameter
    """
    body = {
        "query": {
            "term": {
                "owner_lastname": {
                    "value": "dixon",
                    "case_insensitive": True
                }
            }
        }
    }
    res = oss.search(index=index, body=body)
    print(res)


def e03_term_query_on_number_field():
    body = {
        "query": {
            "term": {
                "account_balance": {
                    "value": 63200
                }
            }
        }
    }
    res = oss.search(index=index, body=body)
    print(res)


def e04_range_query_on_number_field():
    body = {
        "query": {
            "range": {
                "account_balance": {
                    "gte": 60000,
                    "lte": 70000
                }
            }
        },
    }
    res = oss.search(index=index, body=body)
    print(res)


def e05_range_query_on_keyword_field():
    """
    knowledge:

    1. avoid ``range`` query on ``keyword`` / ``text`` field.
        only use on ``number`` if possible
    2. ``range`` query on ``keyword`` / ``text`` are expensive, by default the index
        turns on ``allow_expensive_queries = True`` settings, you can disable it
        to avoid expensive query
    3.``text`` field are analyzed before store, you may experience wild behavior
        on ``range`` query. For example "2001-06-30" will be tokenize as
        "2001", "06", "30" and "-" is considered as delimiter. So ``range`` query
        between "2001-06-15" to "2001-07-15" won't match the document
    """
    body = {
        "query": {
            "range": {
                "account_creation_date": {
                    "gte": "20160101",
                    "lte": "20160131"
                }
            }
        },
    }
    res = oss.search(index=index, body=body)
    print(res)


def e06_match_query_on_text():
    """
    knowledge:

    1. match query = full text search query
    2. minimal unit is word
    3. word is case insensitive by default
    4. stop word doesn't count (am, is, are, ...)
    5. use logic or when there are multiple words
    """
    body = {
        "query": {
            "match": {
                "owner_billing_address": {
                    # "query": "burke",
                    # "query": "station",
                    # "query": "burke station", # full text search by default is logic OR
                    # "query": "burke station", "operator": "and",
                    # "query": "bur"
                }
            }
        },
    }
    res = oss.search(index=index, body=body)
    print(res)


def e07_fuzzy_search_query():
    """
    knowledge:

    1. fuzzy search are expensive
    2. fuzzy search works with keyword, text field
    3. fuzziness is the max edit distance
    """
    body = {
        "query": {
            "match": {
                "owner_firstname": {
                    # "query": "tomas" # this won't match anything
                    "query": "tomas", "fuzziness": 2  # this will match
                }
            }
        },
    }
    res = oss.search(index=index, body=body)
    print(res)


def e21_knn_query():
    """
    knowledge:

    1. you need to create index with the ``index.knn = True`` setting
    2. you also need to set size = the value of k because of the sharding

    reference:

    - https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html
    """
    body = {
        "size": 5,
        "query": {
            "knn": {
                "owner_preference_vector": {
                    "vector": [100, 88, 61, 68, 81, 97, 36, 49, 92, 86 ], "k": 5
                }
            }
        },
    }
    res = oss.search(index=index, body=body)
    print(res)


if __name__ == "__main__":
    # --- understand ``term``, ``range`` and ``match`` query
    # e01_term_query_exact_match()
    # e02_term_query_exact_match_case_insensitive()
    # e03_term_query_on_number_field()
    # e04_range_query_on_number_field()
    # e05_range_query_on_keyword_field()
    # e06_match_query_on_text()
    # e07_fuzzy_search_query()

    # --- compound query
    # --
    e21_knn_query()
    pass
