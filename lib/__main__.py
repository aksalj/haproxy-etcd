import click
import time
from etcd import Etcd
from haproxy import Haproxy


@click.command()
@click.option('--template', '-t', required=True, help='haproxy template')
@click.option('--client-url', '-c', required=True, help='etcd client url')
@click.option('--haproxy-binary', '-b', required=False, help='path to haproxy binary')
@click.option('--haproxy-pid', '-p', required=False, help='path to haproxy binary. Required if using --haproxy-binary')
@click.option('--haproxy-service', '-s', required=False, help='name of haproxy service. Not needed if using --haproxy-binary')
@click.option('--haproxy-config', '-f', required=False, help='where to save config file')
@click.option('--interval-check', '-i', default=5, help='Service interval check; in seconds')
def main(template, client_url, haproxy_binary, haproxy_pid, haproxy_service, haproxy_config, interval_check):
    """Generate a haproxy config file based on etcd then gracefully reload haproxy"""

    # TODO: if haproxy_binary, make sure haproxy_pid is provided

    etcd = Etcd(client_url)

    haproxy = Haproxy(haproxy_service, haproxy_binary, haproxy_pid)
    if template:
        haproxy.set_template(template)
    if haproxy_config:
        haproxy.set_config_file(haproxy_config)

    while True:
        data = []
        services = etcd.fetch_services()
        for service in services:
            instances = etcd.fetch_instances_of(service)
            data.append({'service': service, 'instances': instances})
        haproxy.reload(data)
        time.sleep(interval_check)

if __name__ == "__main__":
    main()
