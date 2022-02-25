Practice: Create AWS OpenSearch Domain
==============================================================================


Locate the Console Menu
------------------------------------------------------------------------------
- https://console.aws.amazon.com/esv3/home?region=us-east-1#opensearch/domains/create-domain


Create Your First Cluster with Following Configuration
------------------------------------------------------------------------------
This is a Cluster configuration for development, DON't USE THIS IN PRODUCTION.

- Name: dev-cluster (or anything you like)
- Customer Endpoint: uncheck (unless you want to your own domain)
- Deployment Type: development and testing
- Version: latest
- Enable Compatibility Mode: uncheck
- Auto-Tune: use default
- Data node:
    - Instance type: r6g.large.search
    - Number of nodes: 1
    - Storage type: EBS
    - EBS volume type: General Purpose SSD
    - EBS storage per size: 10
- Dedicated master nodes: uncheck
- Warm and cold data storage: default
- Snapshot configuration: default
- Network: Public access
- Fine-grained access control: uncheck
- SAML authentication for OpenSearch Dashboards/Kibana: default
- Amazon Cognito authentication: default
- Access policy: Configure domain level access policy
- Visual editor:
    - type ``aws sts get-caller-identity`` in AWS Cloud9 terminal
    - copy the ``ARN`` to ``Principal`` field, set ``Action`` = ``Allow``
- Encryption: default
- Advanced cluster settings: default


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
