#from kube_provider.clusters.kube_client import kube_cluster, existing_cluster_factory, kind_cluster_factory, giantswarm_cluster_factory
from kube_provider.clusters import *
from kube_provider.clusters.kube_client import kube_cluster
from kube_provider.clusters.clusters import Cluster
import pytest
import pytest_kube_provider
import logging
from pykube import HTTPClient

logger = logging.getLogger(__name__)


def test_app_running(kube_cluster: Cluster):
    logger.info(kube_cluster)
    assert True
