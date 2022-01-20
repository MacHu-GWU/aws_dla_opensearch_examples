Optimize Write Throughput and Speed
==============================================================================

.. contents::
    :depth: 1
    :local:


Client Strategy
------------------------------------------------------------------------------


1. Bulk Indexing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ES offers a Bulk API for document indexing. As one would expect, it makes indexing much faster. It is recommended to do some benchmarks to determine the right batch size for your data.


2. Parallelization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ES scales horizontally by nature — and so should your indexing jobs. Make sure you distribute the data you need to ingest across multiple workers that can run in parallel. Pay attention to errors like TOO_MANY_REQUESTS (429) that happens when ES thread pool queues are full (and make sure you have `exponential backoff <https://en.wikipedia.org/wiki/Exponential_backoff>`_ when that happens).


3. Response Filtering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
filter_path parameter that can be used to reduce the response returned by Elasticsearch. This parameter takes a comma-separated list of filters expressed with the dot notation::

    POST "es-endpoint/index-name/_bulk?filter_path=-took,- items.index._index,-items.index._type"


4. Aggregate Before Saving
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is especially important if you’re updating your documents through “random” operations (like a user updating their username) instead of running batch jobs that already have aggregated information.

Let's say you use ES for full-text search on your social network project and you need to update your user document each time a user gets a new follower.
You will soon start seeing multiple timeout issues and lag across the board.
You may be just updating a simple field, but ES is forced to delete the current document and create an entirely new one!

A simple solution here is to “buffer” those user changes using Redis, Kafka, or any other means and then aggregate those multiple document edits into a single one before saving to Elasticsearch. Better yet, group by “key” for a window of time and then use bulk operations to send those docs to ES.


Index Strategy
------------------------------------------------------------------------------

1. Refresh Interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is probably one of the configurations at the index level that will make the most difference.

The refresh operation makes new data available for search. When a refresh happens, the recently indexed data that only exists in memory is transferred to a new Lucene segment. This operation does not flush/commit those segments to disk but the data is safe thanks to the translog, more on this later.

Elasticsearch will execute a refresh every second if the index received one search request or more in the last 30 seconds.

If you’re using Elasticsearch, your system is probably already prepared for eventual consistency, and increasing the refresh interval could be a good option for you.

You can set a bigger refresh_interval for your index during a batch ingest job and then set it back again to your standard value after the job finishes.

If you have a lot of different concurrent jobs happening, it could try to understand how big of a refresh interval you can live with.

More info `here <https://www.elastic.co/guide/en/elasticsearch/reference/master/index-modules.html#index-refresh-interval-setting>`_.


2. Auto-Generated IDs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Allowing ES to generate ids on your behalf should increase document creation speed since ES won’t need to check for uniqueness.

The performance increase of using auto-generated ids was way more evident before version 1.4. Since then, ES id lookup speed was greatly increased, reducing the penalty when your using self-ids.

But that is only true if you use a “Lucene friendly” format. A great article about good ids can be found here.


3. Disable Replicas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you can disable your replicas during a bulk index job, it will also greatly increase indexing speed.
When you index a document, it will be indexed by each replica, effectively multiplying the work by the number of replicas you have.
On the other hand, if you disable them before the bulk job and only enable them afterward, the new information will be replicated in a serialized binary format without the need to analyze or merge segments.


Node Strategy
------------------------------------------------------------------------------


1. Indexing Buffer Size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This setting will control how much memory ES will reserve for indexing. The default is 10% of the heap.
Since this will be shared among all the indexes of your node, you need to make sure you have at least 512MB allocated per index.
If you increase your translog size, you’ll also need to increase these settings to avoid flushing prematurely.
More info about those settings `here <https://www.elastic.co/guide/en/elasticsearch/reference/current/indexing-buffer.html>`_.

Seems like AWS OpenSearch doesn't allow to change https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-operations.html


2. Translog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Translog is the ES transaction log. You have 1 per shard and it is updated alongside the in-memory buffer and in case of a crash, it can be used to persist data to disk in Lucene. When it reaches a certain size (512MB is the default), it will trigger a flush operation that will commit all in-memory Lucene segments to disk.
This flush operation takes the form of a Lucene commit. During a commit, all the segments in memory are merged into a single segment and saved to disk.
As you can imagine, this is an expensive operation. You can increase the translog to create bigger segments in disk (better performance overall) while also reducing this expensive operation cadence.
The field that is responsible for that value is flush_threshold_size . Read more about it `here <https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-translog.html>`_.


3. Cross-Cluster Replication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
With this setup, you can direct all your reads to the “follow” index and write only to the “leader” index. This way you don’t have reads competing with writes.


Operating System and Server Strategies
------------------------------------------------------------------------------


1. Disable Swapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Swapping will kill your performance. ES uses a lot of memory so if you’re not careful, there’s a good chance it might start swapping.
You have multiple ways of `disabling swap <https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-configuration-memory.html>`_.


2. Filesystem Cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Linux automatically uses free ram to cache files. Elastic recommends having at least half the memory of the machine running Elasticsearch available for the filesystem cache.
Make sure you don’t set ES_HEAP_SIZE to be more than 50% of your machine memory so the rest is free for the filesystem cache.
You should also avoid having more than 32GB of HEAP since it will start using uncompressed pointers that will hinder performance and use double the memory.


3. Storage Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Avoid network disks like NFS or EFS and try to always use SSD (NVMe if possible). Hardware like AWS EBS can be a good option but directly connected disks will always be faster, especially if you have a RAID setup.
