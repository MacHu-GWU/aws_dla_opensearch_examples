Read Throughput Optimization
==============================================================================

System Level

1. more sharding, help with more concurrency, but slow down the aggregation
2. more replica, can increase read throughput, because we only need 1 replica to acknowledge write success, other replica can serve read traffic

Application Level

1. Filtered Query, apply filter query on those field doesn't participate scoring
2. Avoid expensive query, if necessary, use filtered query combine with expensive query
3. Return less field to save for IO bandwidth.

Reference:

- Optimize Searching: https://www.elastic.co/blog/found-optimizing-elasticsearch-searches
- Tune for Search Speed: https://www.elastic.co/guide/en/elasticsearch/reference/7.11/tune-for-search-speed.html#_give_memory_to_the_filesystem_cache_2
- Caching: https://www.elastic.co/blog/elasticsearch-caching-deep-dive-boosting-query-speed-one-cache-at-a-time