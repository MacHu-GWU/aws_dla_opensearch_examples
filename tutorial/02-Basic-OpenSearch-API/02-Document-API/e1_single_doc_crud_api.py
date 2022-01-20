# -*- coding: utf-8 -*-

"""
Ref: https://opensearch.org/docs/latest/opensearch/rest-api/document-apis/index/

- Create = index in ES
- Read = get in ES
- Update = update in ES
- Delete = delete in ES
"""

import base64
from rich import print
from learn_opensearch.connection import oss

index = "single_doc_api_test"


def serialize_binary(b) -> str:
    return base64.b64encode(b).decode("utf-8")


def deserialize_binary(s) -> bytes:
    return base64.b64decode(s.encode("utf-8"))


def e00_reset_index():
    # delete if exists
    oss.indices.delete(index=index, ignore=[400, 404])

    # create if exists
    oss.indices.create(index=index, ignore=400)


def e01_index():
    # --- index
    print("--- index response")
    body = {
        "id": 1,
        "a_int": 1,
        "a_float": 3.14,
        "a_str": "this is string",
        "a_bytes": serialize_binary("this is bytes".encode("utf-8")),
    }
    res = oss.index(index=index, id=1, body=body)
    print(res)


def e02_get():
    # --- get
    print("--- get response")
    res = oss.get(index=index, id=1)
    print(res)


def e03_update():
    # --- update
    print("--- update response")

    # method 1, script update
    update_body = {
        "script": {
            "source": "ctx._source.a_float = params.a_float",
            "lang": "painless",
            "params": {
                "a_float": 2.72
            }
        }
    }
    res = oss.update(index=index, id=1, body=update_body)
    print(res)

    # method 2, set key value update
    update_body = {
        "doc": {
            "a_int": 9,
        }
    }
    res = oss.update(index=index, id=1, body=update_body)
    print(res)

    print("--- after update")
    res = oss.get(index=index, id=1)
    print(res)


def e04_delete():
    # --- delete
    print("--- delete response")
    res = oss.delete(index=index, id=1)
    print(res)

    print("--- get response")
    res = oss.get(index=index, id=1, ignore=[400, 404])
    print(res)


def faq1_index_full_replacement_or_not():
    """
    insert a new doc, if id already exists, what gonna happen?

    1. raise Exception?
    2. full replacement?
    3. version id change or not?

    conclusion:

    1. no exception
    2. full replacement
    3. version + 1
    """
    id_ = "test_index_full_replacement_or_not"

    print("--- first index response")
    res = oss.index(index=index, id=id_, body={"name": "alice", "email": "alice@google.com"})
    print(res)

    res = oss.get(index=index, id=id_)
    print("--- get response")
    print(res)

    print("--- second index response")
    res = oss.index(index=index, id=id_, body={"email": "alice@outlook.com"})
    print(res)

    res = oss.get(index=index, id=id_)
    print("--- get response")
    print(res)


def faq2_upsert_or_not():
    """
    update a document, id not exists

    1. upsert?

    conclusion:

    1. no auto upsert
    """
    id_ = "test_upsert_or_not"

    # ensure doc not exists
    oss.delete(index=index, id=id_, ignore=[404])

    update_body = {
        "script": {
            "source": "ctx._source.a_int = 99",
            "lang": "painless",
        }
    }
    res = oss.update(index=index, id=id_, body=update_body)
    print(res)


def faq3_update_increase_version_or_not():
    """
    update a document, id already exists, version id + 1 or not?

    conclusion: yes
    """
    id_ = "test_update_increase_version_or_not"

    # insert initial doc
    oss.index(index=index, id=id_, body={"count": 0})

    print("--- before")
    res = oss.get(index=index, id=id_)
    print(res)

    update_body = {
        "script": {
            "source": "ctx._source.count = params.increment",
            "lang": "painless",
            "params": {
                "increment": 1
            }
        }
    }
    res = oss.update(index=index, id=id_, body=update_body)
    # print(res)

    print("--- after")
    res = oss.get(index=index, id=id_)
    print(res)


def faq4_delete_reset_version_or_not():
    """
    delete a doc, reset version to 0 or not?

    conclusion: no
    """
    id_ = "test_delete_reset_version_or_not"

    # refresh version to at least 2
    oss.index(index=index, id=id_, body={"name": "alice"})
    oss.index(index=index, id=id_, body={"name": "bob"})

    res = oss.get(index=index, id=id_)
    print(res)

    # delete doc
    oss.delete(index=index, id=id_)

    # re-index doc
    oss.index(index=index, id=id_, body={"name": "cathy"})
    res = oss.get(index=index, id=id_)
    print(res)


if __name__ == "__main__":
    # e00_reset_index()
    # e01_index()
    # e02_get()
    # e03_update()
    # e04_delete()

    # faq1_index_full_replacement_or_not()
    # faq2_upsert_or_not() # it should raise exception
    # faq3_update_increase_version_or_not()
    # faq4_delete_reset_version_or_not()
    pass
