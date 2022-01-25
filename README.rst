AWS Opensearch Examples
==============================================================================

.. contents::
    :depth: 1
    :local:

Overview
------------------------------------------------------------------------------
This is an unofficial tutorial to boost your AWS OpenSearch (The open source version of ElasticSearch) knowledge level from ZERO to HERO.

This tutorial is NOT designed for self pace learning, it is given by an experienced AWS Opensearch expert.

Prerequisite:

- a sandbox AWS Account to play with
- basic Python knowledge


Setup Development Environment
------------------------------------------------------------------------------
You can do the develop from your local MAC laptop. For windows computer, some linux command may not work properly.

Another easy way is to create a AWS Cloud 9 dev environment, it is a cloud IDE environment on a EC2 virtual machine. It only takes a few clicks and a few minutes to create one, so you can start development from any computer. You can find a `simple AWS Cloud 9 tutorial here <https://github.com/MacHu-GWU/aws_dla_lbd_development_examples/blob/main/README.rst#id4>`_

1. Check your current system Python and virtualenv CLI

.. code-block:: bash

    # show full path of python interpreter
    which python

    # show python version
    python --version

    # show full path of virtualenv cli
    which virtualenv

2. Clone this repo and CD into it

.. code-block:: bash

    # clone the repo
    git clone https://github.com/MacHu-GWU/aws_dla_opensearch_examples.git

    # cd into the repository root directory
    cd ./aws_dla_opensearch_examples

3. Create virtualenv:

.. code-block:: bash

    # create virtualenv
    virtualenv venv

    # activate the virtualenv, you should see (venv) at begin
    source ./venv/bin/activate

    # pip install learn_opensearch package on your local
    # you can make your code importable from virtual env
    pip install -e .

4. Configure Runner to use virtualenv python.

Cloud 9 top menu -> Run -> Run With -> New Runner

.. code-block:: javascript

    // Create a custom Cloud9 runner - similar to the Sublime build system
    // For more information see http://docs.aws.amazon.com/console/cloud9/create-run-config
    {
        "cmd" : ["/home/ec2-user/environment/venv/bin/python", "$file", "$args"],
        "info" : "Started $project_path$file_name",
        "env" : {},
        "selector" : "source.ext"
    }


Follow the Jump Start Tutorial
------------------------------------------------------------------------------
Read through this `tutorial <tutorial>`_, and replay those sample python scripts.


Additional Learning Resource
------------------------------------------------------------------------------

- OpenSearch doc: https://opensearch.org/docs/latest
