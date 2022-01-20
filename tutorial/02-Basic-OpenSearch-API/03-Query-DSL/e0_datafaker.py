# -*- coding: utf-8 -*-

import os
import time
import json
from opensearchpy.helpers import bulk
from learn_opensearch.connection import oss
from learn_opensearch.datafaker import gen_data

index = "query_dsl_test"

p_data_json = os.path.join(os.path.dirname(__file__), "data.json")


def e00_reset_index():
    # delete if exists
    oss.indices.delete(index=index, ignore=[400, 404])
    time.sleep(1)

    # create if exists
    body = {
        "settings": {
            "index.knn": True
        },
        "mappings": {
            "properties": {
                "account_balance": {"type": "integer"},
                "account_creation_date": {"type": "keyword"},
                "account_type": {"type": "keyword"},
                "owner_lastname": {"type": "keyword"},
                "owner_firstname": {"type": "keyword"},
                "owner_ssn": {"type": "keyword"},
                "owner_billing_address": {"type": "text"},
                "owner_email": {"type": "text"},
                "owner_preference_vector": {"type": "knn_vector", "dimension": 10},
            }
        }
    }
    oss.indices.create(index=index, body=body)


def e01_index_data():
    # clear existing data
    query_search_all = {"query": {"match_all": {}}}
    oss.delete_by_query(index=index, body=query_search_all)
    time.sleep(1)

    def gen_actions(json_file):
        if os.path.exists(json_file):
            os.remove(json_file)
        with open(json_file, "a") as f:
            n = 1000
            for doc in gen_data(n):
                f.write(json.dumps(doc) + "\n")
                account_id = doc.pop("account_id")
                action = {
                    "_index": index,
                    "_id": account_id,
                    "_source": doc,
                }
                yield action

    bulk(oss, gen_actions(p_data_json))


if __name__ == "__main__":
    # e00_reset_index()
    # e01_index_data()
    pass
