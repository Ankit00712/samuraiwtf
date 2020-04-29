from plugins import Plugin
import docker
import os.path


class Docker(Plugin):

    @classmethod
    def get_aliases(cls):
        return ["docker"]

    def install(self, params):
        self._validate_params(params, ['name', 'image'], 'docker')
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')

        container_list = client.containers.list(filters={'name': params.get('name')}, all=True)

        if len(container_list) > 0:
            return False, "A container named '{}' is already installed.".format(params.get('name'))
        else:
            container = client.containers.create(image=params.get('image'), name=params.get('name'), detach=True)
            container.logs()
            return True, None
