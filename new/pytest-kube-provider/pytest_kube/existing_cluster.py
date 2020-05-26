from pathlib import Path
from typing import Union

import pykube

from .cluster import Cluster


class ExistingCluster(Cluster):
    def __init__(self, name, kubeconfig_path):
        super().__init__(name)

        self.kubeconfig_path = kubeconfig_path

        config = pykube.KubeConfig.from_file(self.kubeconfig_path)
        self.api = pykube.HTTPClient(config)

    # not implemented
    def load_docker_image(self, docker_image: str):
        pass

    # does not apply
    def delete(self):
        pass
