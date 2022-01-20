# -*- coding: utf-8 -*-

import boto3
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection


def create_connection(
    boto_ses: boto3.session.Session,
    aws_region: str,
    es_endpoint: str,
    test: bool = True,
) -> OpenSearch:
    """
    Create an AWS Opensearch connection to a domain.
    """
    if es_endpoint.startswith("https://"):
        es_endpoint = es_endpoint.replace("https://", "", 1)
    credentials = boto_ses.get_credentials()
    aws_auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        aws_region,
        "es",
        session_token=credentials.token,
    )
    es = OpenSearch(
        hosts=[{"host": es_endpoint, "port": 443}],
        http_auth=aws_auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    if test:
        es.info()
    return es
