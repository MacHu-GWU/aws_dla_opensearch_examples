# -*- coding: utf-8 -*-

"""
Maintain an importable OpenSearch client connection to use.
"""

from .boto_ses import boto_ses
from .opensearch import create_connection

# oss = open search service
oss = create_connection(
    boto_ses=boto_ses,
    aws_region="us-east-1",
    es_endpoint="https://search-sanhe-dev-ce5xh5zovkiwjkf2x4c4k2saf4.us-east-1.es.amazonaws.com",
    test=False,
)