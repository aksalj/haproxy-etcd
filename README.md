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
    

### Contributing

1. Fork this repo and make changes in your own fork.
2. Commit your changes and push to your fork `git push origin master`
3. Create a new pull request and submit it back to the project.


### Bugs & Issues

To report bugs (or any other issues), use the [issues page](https://github.com/aksalj/haproxy-etcd/issues).

