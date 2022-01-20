# -*- coding: utf-8 -*-

from rich import print
from learn_opensearch.connection import oss

index = "index_api_test"


def e0_check_index_exists():
    res = oss.indices.exists(index=index)
    print(res)


def e1_create_index():
    res = oss.indices.create(index=index)
    print(res)


def e2_create_index_if_not_exists():
    res = oss.indices.create(index=index, ignore=400)
    print(res)


def e3_get_settings_and_mappings():
    res = oss.indices.get(index=index)
    # res = es.indices.get_settings(index=index)
    # res = es.indices.get_mapping(index=index)
    print(res)


def e4_get_stats():
    res = oss.indices.stats(index=index)
    print(res)


def e5_create_index_with_explicit_mappings():
    body = {
        "mappings": {
            "properties": {
                "firstname": {"type": "keyword"},
                "lastname": {"type": "keyword"},
                "description": {"type": "text"},
                "account_balance": {"type": "integer"},
            }
        }
    }
    res = oss.indices.create(index=index, body=body)
    print(res)


def e6_update_settings():
    body = {
        "index": {
            "number_of_replicas": 2
        }
    }
    print("=== before ===")
    res = oss.indices.get_settings(index=index)
    print(res)
    res = oss.indices.put_settings(index=index, body=body)
    print("=== after ===")
    print(res)
    res = oss.indices.get_settings(index=index)
    print(res)


def e7_open_and_close():
    oss.indices.close(index=index)
    oss.indices.open(index=index)


def e8_delete():
    res = oss.indices.delete(index=index)
    print(res)


def e9_delete_if_exists():
    res = oss.indices.delete(index=index, ignore=[400, 404])
    print(res)


if __name__ == "__main__":
    # e0_check_index_exists()
    # e1_create_index()
    # e2_create_index_if_not_exists()
    # e3_get_settings_and_mappings()
    # e4_get_stats()
    # e5_create_index_with_explicit_mappings()
    # e6_update_settings()
    # e7_open_and_close()
    # e8_delete()
    # e9_delete_if_exists()
    pass
