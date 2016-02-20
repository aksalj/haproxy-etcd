import click
import time
from apiclient import APIClient
from mako.template import Template


class EtcdAPI(APIClient):
    """
        Get services from etcd
        Expects them at /keys/services, for each service, the value expected is (HOST|IP):PORT
        e.g. for a service called api:
                /keys/services/api could return
                {
                  "action": "get",
                  "node": {
                    "key": "/services/api",
                    "dir": true,
                    "nodes": [
                      {
                        "key": "/services/api/172.10.0.1:8000",
                        "value": "172.10.0.1:8000",
                        "modifiedIndex": 4,
                        "createdIndex": 4
                      },
                      {
                        "key": "/services/api/172.10.0.2:8000",
                        "value": "172.10.0.1:8000",
                        "modifiedIndex": 5,
                        "createdIndex": 5
                      }
                    ],
                    "modifiedIndex": 4,
                    "createdIndex": 4
                  }
                }
    """

    def __init__(self, base_url):
        super(EtcdAPI, self).__init__()
        self.BASE_URL = base_url + '/v2'
        self.connection_pool = self._make_connection_pool(self.BASE_URL)

    def fetch_services(self, key='services'):
        req = self.call('/keys/' + key)
        nodes = req['node']['nodes']
        services = []
        for node in nodes:
            service = {
                'path': '/keys' + node['key'],
                'name': node['key'].split('/')[2]
            }
            services.append(service)
        return services

    def fetch_instances_of(self, service):
        req = self.call(service['path'])
        nodes = req['node']['nodes']
        instances = []
        counter = 0
        for node in nodes:
            values = node['value'].split(':')
            instance = {
                'key': node['key'],
                'name': service['name'] + '_' + repr(counter),
                'host': values[0],
                'port': values[1]
            }
            instances.append(instance)
            counter += 1
        return instances


@click.command()
@click.option('--template', '-t', default='templates/haproxy.tpl', required=False, help='Haproxy template')
@click.option('--client-url', '-c', default='http://localhost:4001', required=False, help='etcd client url')
@click.option('--haproxy', '-h', default='haproxy', required=False, help='Haproxy binary')
@click.option('--interval-check', '-i', default=1, help='Service interval check; in seconds')
def main(template, client_url, haproxy, interval_check):
    """Generate a haproxy config file based on etcd then gracefully reload haproxy"""

    etcd = EtcdAPI(client_url)

    while True:
        services = etcd.fetch_services()
        for service in services:
            instances = etcd.fetch_instances_of(service)
            for instance in instances:
                print instance
            # TODO: Prepare template
            # TODO: Reload haproxy
            time.sleep(interval_check)


if __name__ == "__main__":
    main()
