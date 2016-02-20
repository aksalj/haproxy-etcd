import click
from apiclient import APIClient
from mako.template import Template


class EtcdAPI(APIClient):

    def __init__(self, base_url):
        super(EtcdAPI, self).__init__()
        self.BASE_URL = base_url + '/v2'
        self.connection_pool = self._make_connection_pool(self.BASE_URL)

    def services(self):
        req = self.call('/keys/services')
        return req['node']['nodes']

    def service(self, key):
        req = self.call(key)
        return req['node']['nodes']


@click.command()
@click.option('--template', '-t', default='templates/haproxy.tpl', required=False, help='Haproxy template')
@click.option('--client-url', '-c', default='http://localhost:4001', required=False, help='etcd client url')
@click.option('--haproxy', '-h', default='haproxy', required=False, help='Haproxy binary')
def main(template, client_url, haproxy):
    """Generate a haproxy config file based on etcd then gracefully reload haproxy"""

    etcd = EtcdAPI(client_url)
    print etcd.services()


if __name__ == "__main__":
    main()
