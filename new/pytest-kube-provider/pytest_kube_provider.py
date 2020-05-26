# -*- coding: utf-8 -*-

import pytest
import pykube
from pathlib import Path
import os.path


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


