import os
import click
import hashlib
import subprocess
from mako import exceptions
from mako.template import Template
from utils import file_contents

"""
Adapted from https://github.com/markcaudill/haproxy-autoscale
"""

class Haproxy:
    BINARY = None
    SERVICE = None
    TEMPLATE = None
    PID = None
    OUTPUT = None

    _lastConfig = None

    def __init__(self, service='haproxy', path=None, pid=None):
        self.SERVICE = service
        self.BINARY = path
        self.PID = pid

        self.set_template(os.path.abspath('../templates/haproxy.tpl'))
        self.set_config_file(os.path.abspath('../haproxy.cfg'))

    def set_template(self, template):
        self.TEMPLATE = template

    def set_config_file(self, path):
        self.OUTPUT = path

    def _generate_config(self, data):
        try:
            params = {}
            for item in data:
                service = item['service']
                instances = item['instances']
                params[service['name']] = instances

            tpl = Template(filename=self.TEMPLATE)
            cfg = tpl.render(instances=params)

            md5 = hashlib.md5()
            md5.update(cfg)
            cfg_hash = md5.hexdigest()
            if cfg_hash != self._lastConfig:
                self._lastConfig = cfg_hash
                return cfg

        except:
            print(exceptions.text_error_template().render())

        return None

    def _restart_haproxy(self):
        """
        Restart haproxy, either as a service or standalone binary
        """
        click.echo('Restarting haproxy...')

        if self.BINARY:
            # Get PID if haproxy is already running.
            pid = file_contents(self.PID)
            command = '''%s -D -p %s -f %s -sf %s''' % (self.BINARY, self.PID, self.OUTPUT, pid or '')

        else:
            command = "service %s restart" % self.SERVICE

        click.echo('\t%s' % command)
        subprocess.call(command, shell=True)

    def reload(self, data):
        cfg = self._generate_config(data)
        if cfg is None:
            return

        file_contents(self.OUTPUT, cfg)
        self._restart_haproxy()
        return None

