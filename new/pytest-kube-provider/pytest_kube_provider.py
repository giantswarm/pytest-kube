import os.path
import sys
import logging
from pathlib import Path
from typing import Callable, List, Iterable

import pytest
from pykube import HTTPClient

from kube_provider.clusters import ExistingCluster, Cluster

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    group = parser.getgroup("kube-provider")
    group.addoption(
        "--cluster-type",
        action="store",
        default="kind",
        help="Select cluster type. Supported values: 'kind', 'existing'."
    )
    group.addoption(
        "--kube-config",
        action="store",
        default=os.path.join(str(Path.home()), ".kube", "config"),
        help="The path to 'kube.config' file. Used when '--cluster-type existing' is used as well."
    )
    group.addoption(
        "--values-file",
        action="store",
        help="Path to the values file used for testing the chart."
    )
    group.addoption(
        "--chart-path",
        action="store",
        help="The path to a helm chart under test."
    )
    group.addoption(
        "--chart-version",
        action="store",
        help="Override chart version for the chart under test."
    )


@pytest.fixture(scope="module")
def chart_path(pytestconfig) -> str:
    return pytestconfig.getoption("chart_path")


@pytest.fixture(scope="module")
def chart_version(pytestconfig) -> str:
    return pytestconfig.getoption("chart_version")


@pytest.fixture(scope="module")
def values_file_path(pytestconfig) -> str:
    return pytestconfig.getoption("values_file")


@pytest.fixture(scope="module")
def kube_config(pytestconfig) -> str:
    return pytestconfig.getoption("kube_config")


@pytest.fixture(scope="module")
def cluster_type(pytestconfig) -> str:
    return pytestconfig.getoption("cluster_type")


ConfigFactoryFunction = Callable[[], Cluster]


@pytest.fixture(scope="module")
def existing_cluster_factory(kube_config: str) -> ConfigFactoryFunction:
    def _fun() -> HTTPClient:
        return ExistingCluster(kube_config)
    return _fun


@pytest.fixture(scope="module")
def kind_cluster_factory() -> ConfigFactoryFunction:
    def _fun() -> HTTPClient:
        # FIXME: implement
        return Cluster()
    return _fun


@pytest.fixture(scope="module")
def giantswarm_cluster_factory() -> ConfigFactoryFunction:
    def _fun() -> HTTPClient:
        # FIXME: implement
        return Cluster()
    return _fun


@pytest.fixture(scope="module")
def kube_cluster(cluster_type: str,
                 existing_cluster_factory: ConfigFactoryFunction,
                 kind_cluster_factory: ConfigFactoryFunction,
                 giantswarm_cluster_factory: ConfigFactoryFunction) -> Iterable[Cluster]:
    cluster: Cluster
    created_clusters: List[Cluster] = []
    if cluster_type == "existing":
        cluster = existing_cluster_factory()
    elif cluster_type == "kind":
        cluster = kind_cluster_factory()
    elif cluster_type == "giantswarm":
        cluster = giantswarm_cluster_factory()
    else:
        raise ValueError("Unsupported cluster type '{}'.".format(cluster_type))

    logger.info("Creating new cluster of type '{}'.".format(cluster_type))
    cluster.create()
    logger.info("Cluster created")
    created_clusters.append(cluster)
    yield cluster

    for c in created_clusters:
        try:
            logger.info("Destroying cluster")
            c.destroy()
        except:
            exc = sys.exc_info()
            logger.error("Error of type {} when destroying cluster. Value: {}\nStacktrace:\n{}".format(
                exc[0], exc[1], exc[2]
            ))
