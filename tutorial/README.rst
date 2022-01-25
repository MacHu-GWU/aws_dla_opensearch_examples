AWS OpenSearch Tutorial
==============================================================================

Table of Content:

1. What is ElasticSearch
    - `Why it is fast in searching, comparing to RDBMS / Big Data <01-What-is-OpenSearch/01-Why-it-is-fast-in-Searching>`_
        - Search in RDBMS: MySQL Example
        - Search in Big Data: Hive + HDFS Example
        - Search in Elasticsearch: Example
    - `Important Concepts <01-What-is-OpenSearch/02-Important-Concepts>`_:
        - **Document**: ~= RDBMS row
        - **Index**: ~= RDBMS Table
        - **Mapping**: ~= RDBMS Index
        - **Cluster**: ~= AWS OpenSearch Domain
        - **Node**: ~= Physical Server / VM / AWS EC2
            - Dedicated Master Node: No Data, coordinator only
            - Data Node
        - **Shard**: smallest unit
        - **Understand the Architect**
    - `Practice: Create AWS OpenSearch Domain <01-What-is-OpenSearch/03-Practice-Create-AWS-Opensearch-Domain>`_
        - Locate the Console Menu
        - Understand Creation Options
        - Configure Authentication Options:
            - Fine grained
            - IAM Role Based Policy
        - Connect to the domain using in Python

2. Basic Elastic Search API
    - `Index API <02-Basic-OpenSearch-API/01-Index-API>`_
        - Create
        - Delete
        - Update: update settings / mappings
        - Statistics
        - List
        - Open
        - Close
    - `Document API <02-Basic-OpenSearch-API/02-Document-API>`_
        - Single Document API
            - Create
            - Get
            - Update
            - Delete
            - Concurrent Control
        - Bulk Document API
            - Bulk Index
            - Update by Query
            - Delete by Query
    - `Query DSL <02-Basic-OpenSearch-API/03-Query-DSL>`_
        - match
        - term
        - range
        - compound query
        - other expensive search:
            - fuzzy
            - prefix
        - aggregation

3. `Index Optimization <03-Index-Optimization>`_
    - `Write Throughput Optimization <03-Index-Optimization/01-Write-Throughput-Optimization>`_
        - Bulk
        - Parallel
        - Refresh Interval
        - Replica
        - and more ...
    - `Read Throughput Optimization <03-Index-Optimization/02-Read-Throughput-Optimization>`_
        - Sharding
        - Include less field in response
    - Search Optimization
        - Mapping

4. Cluster Ops
    - Disaster Recovery
        - Backup method
        - High availability method
    - Monitoring
    - Security
