from functools import partial

import pytest

from .cluster import Cluster


@pytest.fixture(scope="session")
def cluster_create(request):
    keep = request.config.getoption("keep_cluster")
    cluster = None

    def _cluster_create(request, cluster_cls: Cluster, *args, **kwargs):
        """Provide a Kubernetes kind cluster as test fixture"""
        # FIXME maybe allow a configurable prefix here instead?
        # name = request.config.getoption("cluster_name")

        nonlocal cluster
        if not cluster:
            cluster = cluster_cls(*args, **kwargs)

        return cluster

    yield partial(_cluster_create, request)
    if not keep:
        cluster.delete()


def pytest_addoption(parser):
    group = parser.getgroup("kube")
    # group.addoption(
    #     "--cluster-name",
    #     default="pytest-kind",
    #     help="Name of the Kubernetes kind cluster",
    # )
    group.addoption(
        "--keep-cluster",
        action="store_true",
        help="Keep the Kubernetes cluster (do not delete after test run)",
    )
