from pykube import HTTPClient, KubeConfig


class Cluster:
    def create(self) -> HTTPClient:
        raise NotImplementedError

    def destroy(self) -> None:
        raise NotImplementedError


class ExistingCluster(Cluster):
    def __init__(self, kube_config: str) -> None:
        self.kube_config = kube_config
        self.kube_client: HTTPClient = None

    def create(self) -> HTTPClient:
        self.kube_client = HTTPClient(KubeConfig.from_file(self.kube_config))
        return self.kube_client

    def destroy(self) -> None:
        if self.kube_client is None:
            return
        self.kube_client.session.close()
        self.kube_client = None
