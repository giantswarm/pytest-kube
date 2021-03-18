from pathlib import Path
import pytest
from .kubernetes_cluster import KubernetesCluster
import random
import string
import os


@pytest.fixture(scope="session")
def kubernetes_cluster(request):
    """Provide a Kubernetes cluster as test fixture"""

    kubeconfig = request.config.getoption("--kube-config")
    cluster = KubernetesCluster(kubeconfig)

    kubeconfig = request.config.getoption("--kubeconfig-management")
    cluster.management = None
    if kubeconfig:
        management = KubernetesCluster(kubeconfig)
        cluster.management = management

    return cluster


@pytest.fixture(scope="class")
# @pytest.fixture(scope="function")
def random_namespace(request, kubernetes_cluster):
    kubectl = kubernetes_cluster.kubectl
    name = f"pytest-{''.join(random.choices(string.ascii_lowercase, k=5))}"

    kubectl(f"create namespace {name}")
    yield name

    if not request.config.getoption("keep_namespace"):
        kubectl(f"delete namespace {name}", output=None)


# FIXME provide factory to choose namespace with possible random postfix
# https://docs.pytest.org/en/stable/fixture.html#factories-as-fixtures
#
# @pytest.fixture(scope="class")
# def random_namespace_factory(request, kubernetes_cluster, name, random_postfix=true):
#     pass


def pytest_addoption(parser):
    parser.addoption(
        "--kube-config",
        action="store",
        default=os.path.join(str(Path.home()), ".kube", "config"),
        help="The path to 'kube.config' file. Used when '--cluster-type existing' is used as well.",
    )

    parser.addoption(
        "--kubeconfig-management",
        default=None,
        help=(
            "If provided, use the specified kubeconfig "
            "to access the management cluster"
        ),
    )

    parser.addoption(
        "--keep-namespace",
        default=None,
        action="store_true",
        help="Keep the pytest namespace (do not delete after test run)",
    )

    # dummy options to satisfy abs
    parser.addoption("--cluster-type", action="store", help="Pass information about cluster type being used for tests.")
    parser.addoption("--values-file", action="store", help="Path to the values file used for testing the chart.")
    parser.addoption("--chart-path", action="store", help="The path to a helm chart under test.")
    parser.addoption("--chart-version", action="store", help="Override chart version for the chart under test.")
    parser.addoption(
        "--chart-extra-info",
        action="store",
        default="",
        help="Pass any additional info about the chart in the 'key1=val1,key2=val2' format",
    )
