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
    es_endpoint="https://search-your-opensearch-domain-here.aws-region-name.es.amazonaws.com",
    test=False,
)