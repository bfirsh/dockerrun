import docker
from docker.errors import APIError
from docker.utils import kwargs_from_env

class ProcessError(Exception):
    def __init__(self, container, exit_status, command, image, stderr):
        self.container = container
        self.exit_status = exit_status
        self.command = command
        self.image = image
        self.stderr = stderr
        super(ProcessError, self).__init__("Command '%s' in image '%s' returned non-zero exit status %s: %s" % (command, image, exit_status, stderr))

CREATE_KWARGS = ["hostname", "user", "detach", "stdin_open", "tty", "mem_limit", "ports", "environment", "dns", "volumes", "volumes_from", "network_disabled", "name", "entrypoint", "cpu_shares", "working_dir", "domainname", "memswap_limit", "cpuset", "host_config", "mac_address", "labels"]

START_KWARGS = ["binds", "port_bindings", "lxc_conf", "publish_all_ports", "links", "privileged", "dns", "dns_search", "volumes_from", "network_mode", "restart_policy", "cap_add", "cap_drop", "devices", "extra_hosts", "read_only", "pid_mode", "ipc_mode", "security_opt", "ulimits"]

def _dict_filter(d, keys):
    return dict((k, v) for k, v in d.items() if k in keys)

def from_env():
    return Client.from_env()

class Client(docker.Client):
    def run(self, image, command=None, detach=False, stdout=True, stderr=False, **kwargs):
        create_kwargs = _dict_filter(kwargs, CREATE_KWARGS)
        try:
            container = self.create_container(image, command, **create_kwargs)
        except APIError as e:
            if e.response.status_code == 404 \
                    and e.explanation \
                    and 'No such image' in str(e.explanation):
                self.pull(image)
                container = self.create_container(image, command)


        start_kwargs = _dict_filter(kwargs, START_KWARGS)
        self.start(container, **start_kwargs)

        if detach:
            return container

        exit_status = self.wait(container)
        if exit_status != 0:
            raise ProcessError(
                container,
                exit_status,
                command,
                image,
                self.logs(container, stdout=False, stderr=True)
            )
        return self.logs(container, stdout=stdout, stderr=stderr)
