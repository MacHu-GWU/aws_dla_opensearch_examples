Why OpenSearch is fast in searching
==============================================================================

.. contents::
    :depth: 1
    :local:


Search in RDBMS: MySQL Example
------------------------------------------------------------------------------
**Two type of IO**:

- random read / write
- sequential read / write

**Schema**::

    Event
    |--- id (String, primary_key=True)  # 128 bytes
    |--- time (String, index=True)      # 64 bytes

**Example**::

    {"id": "452da269c2b17ba970c1305161c70629", "time": "2022-01-01 08:30:00"}

**Data Storage on Disk**::

    # Sequence Write on Disk
         |   meta    |    id     |   time    |
    row1 | [][]...[] | [][]...[] | [][]...[] |
    row2 | [][]...[] | [][]...[] | [][]...[] |

**key / value typed Index**::

    # An in memory hash map structure
    hash_of_id -> disk_address

**range typed Index**::

    # An in memory data structure
    # each segment has start value and end value
    sorted_segment_1: list of disk_address for each row
    sorted_segment_2: ...
    sorted_segment_3: ...
    ...
    sorted_segment_n: ...

    # Search behavior:
    1. use binary search to locate segment
    2. locate rows based on disk address
    3. return

**Con**:

- Primary key are not always exists, so partition can't be natively support. (some people create many table based on year / month / day, this is called application level partition).
- Performance going down over Million / Billion rows.
- Not easy to scale.


Search in Big Data: Hive + HDFS Example
------------------------------------------------------------------------------

**Schema**::

    Event
    |--- id (String, partition_key=True) # 128 bytes
    |--- time (String)                   # 64 bytes

**Big Data Architect**::

    Cluster

    - Partition 1 ( Mod(hash(event_id), N) = 1 )
    - Partition 2 ( Mod(hash(event_id), N) = 2 )
    - Partition 3
    - ...
    - Partition N

**Block Storage on Disk** (64, 128, 256MB)::

    # column storage
    id | 1th [][]...[] | 2th [][]...[] | ...
    time | 1th [][]...[] | 2th [][]...[] | ...

    # index storage
    id index ...
    time index ...

    # block statistics storage
    block address
    n records
    min time
    max time
    ...

**Block Index**::

    time index -> block address

**How Search Works**::

    # example: SELECT events WHERE time BETWEEN start AND end

    1. distribute query to all partition
    2. use block index to locate block
    3. within each block, use in-block index to filter records
    4. sequential scan required column only to filter the data
    5. return data from each partition, aggregate and return

**Con**:

- Still need full scan for full text search
- There's no such rank by relevance score


Search in OpenSearch: Example
------------------------------------------------------------------------------
**Schema**::

    News
    |--- id (String, id=True) # 128 bytes
    |--- time (String)        # 64 bytes
    |--- content (String)     # 0 ~ 1MB

**Architect**::

    Cluster

    - Data Node 1
        - shard 1 ( Mod(hash(news_id), 20) = 1 )
        - shard 2 ( Mod(hash(news_id), 20) = 2 )
        - ...
        - shard 20 ( Mod(hash(news_id), 20) = 0 )
    - Data Node 2
        - shard 1 replica
        - ...
    - Data Node 3
        - shard 1 replica
        - ...

**What is Term?**

- Term ~= word in different form
- Term can be ngram

**Term Index** (also benefit full text search)::

    - shard 1
        term1: id set ...
        term2: id set ...
        ...
    - shard 2
        term1: id set ...
        term2: id set ...
        ...
    - ...
    - shard 20
        term1: id set ...
        term2: id set ...
        ...

**Range Index**::

    - shard 1
        # eatch segment with a min / max value
        segment 1: id_set
        segment 2: id_set
        ...
        segment 3: id_set
    - ...

**How Search Works**::

    # example: find news between date1, date2, having two term: "Iphone", "Finance"
    1. distribute query to each shard
    2. fetch term id set for "Iphone", "Finance", and get the intersection
    3. if only a few (<=1000) matched documents, just scan those 1000 doc and filter by time
    4. if still has a lot matched documents, use Range Index to get the id_set, then get the intersection
    5. fetch documents
    6. ranking, ordering
    7. aggregate and return
