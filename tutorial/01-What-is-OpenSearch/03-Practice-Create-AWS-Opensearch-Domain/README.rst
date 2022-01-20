Practice: Create AWS OpenSearch Domain
==============================================================================


Locate the Console Menu
------------------------------------------------------------------------------
- https://console.aws.amazon.com/esv3/home?region=us-east-1#opensearch/domains/create-domain


Understand Creation Options
------------------------------------------------------------------------------

- Deployment type
- Auto-Tune
- Data nodes
- Dedicated master nodes
- Warm and cold data storage
- Snapshot configuration
- Network
- Fine-grained access control
- Access policy
- Encryption


Configure Authentication Options
------------------------------------------------------------------------------
- Fine grained: in-cluster admin console, requires additional setup, but can provide: cluster / node / index / field / document level control.
- IAM Role Based Policy: similar to other Resources Policy like: S3 Bucket Policy, Glue Catalog Policy, etc ...


Connect to the domain using in Python
------------------------------------------------------------------------------
See examples.


Additional Best Practice
------------------------------------------------------------------------------

- `Determine size of the domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sizing-domains.html>`_: how many node? how many disk? how many shard? how many replica? ec2 instance type?
    - `How many data instances do I need <https://aws.amazon.com/blogs/database/get-started-with-amazon-elasticsearch-service-how-many-data-instances-do-i-need/>`_
    - `How many shards do I need <https://aws.amazon.com/blogs/database/get-started-with-amazon-elasticsearch-service-how-many-shards-do-i-need/>`_
- `Dedicated master nodes <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html>`_
