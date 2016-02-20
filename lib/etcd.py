from apiclient import APIClient


class Etcd(APIClient):
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
        self.BASE_URL = base_url + '/v2'
        super(Etcd, self).__init__()

    def fetch_services(self, key='services'):
        req = self.call('/keys/' + key, sorted='true')
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
        req = self.call(service['path'], sorted='true')
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
