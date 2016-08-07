# haproxy-etcd

Simple tool to generate a haproxy config file based on `etcd` and gracefully reload haproxy.


### Goal

Objective is to dynamically update `haproxy.cfg` with new servers on each backend (when registred with etcd) and reload haproxy.

### Installation

Simply run:

    $ pip install .


### Usage

To use it:

    $ haproxy-etcd --help

**Important**: Services are expected to be registred at `/keys/services`; 
For each service instance, the expected value is formatted as `[HOST|IP]:PORT`

e.g. for a service named `api`, a `GET` from `/keys/services/api` could return the following instances/nodes:
```json
{
    "action": "get",
    "node": {
    "key": "/services/api",
    "dir": true,
    "nodes": [
        {
        "key": "/services/api/172.10.0.1",
        "value": "172.10.0.1:80",
        "modifiedIndex": 4,
        "createdIndex": 4
        },
        {
        "key": "/services/api/172.10.0.2",
        "value": "172.10.0.2:80",
        "modifiedIndex": 5,
        "createdIndex": 5
        }
    ],
    "modifiedIndex": 4,
    "createdIndex": 4
    }
}
```
    

### Contributing

1. Fork this repo and make changes in your own fork.
2. Commit your changes and push to your fork `git push origin master`
3. Create a new pull request and submit it back to the project.


### Bugs & Issues

To report bugs (or any other issues), use the [issues page](https://github.com/aksalj/haproxy-etcd/issues).

