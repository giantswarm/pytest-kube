from typing import Iterable, Callable, Dict, List, NamedTuple, Any

import yaml
import pytest
from pykube import HTTPClient, ConfigMap

from .app_catalog import AppCR, AppCatalogFactoryFunc
from kube_provider.apps.app_catalog import GiantSwarmAppPlatformCRs

AppFactoryFunc = Callable[[str, str, str,
                           str, int, str, Dict[str, Any]], AppCR]

class AppState(NamedTuple):
    app: AppCR
    app_cm: ConfigMap


def app_factory_func(kube_client: HTTPClient,
                app_catalog_factory: AppCatalogFactoryFunc,
                created_apps: List[AppState]) -> AppFactoryFunc:
    def _app_factory(app_name: str, app_version: str, catalog_name: str,
                     catalog_url: str, replicas: int = 1, namespace: str = "default",
                     config_values: Dict[str, Any] = {}) -> AppCR:
        # TODO: include proper regexp validation
        assert app_name is not ""
        assert app_version is not ""
        assert catalog_name is not ""
        assert catalog_url is not ""

        api_version = "application.giantswarm.io/v1alpha1"
        app_cm_name = "{}-testing-user-config".format(app_name)
        catalog = app_catalog_factory(catalog_name, catalog_url)
        kind = "App"

        app = {
            "apiVersion": api_version,
            "kind": kind,
            "metadata": {
                "name": app_name,
                "namespace": namespace,
                "labels": {
                    "app": app_name,
                    "app-operator.giantswarm.io/version": "1.0.0"
                },
            },
            "spec": {
                "catalog": catalog.metadata["name"],
                "version": app_version,
                "kubeConfig": {
                    "inCluster": True
                },
                "name": app_name,
                "namespace": namespace,
            }
        }

        app_cm_obj: ConfigMap = None
        if config_values:
            app["spec"]["config"] = {
                "configMap": {
                    "name": app_cm_name,
                    "namespace": namespace,
                }
            }
            app_cm = {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {
                    "name": app_cm_name,
                    "namespace": namespace,
                },
                "data": {
                    "values": yaml.dump(config_values)
                }
            }
            app_cm_obj = ConfigMap(kube_client, app_cm)
            app_cm_obj.create()

        app_obj = GiantSwarmAppPlatformCRs(
            kube_client).app_cr_factory(kube_client, app)
        app_obj.create()
        created_apps.append(AppState(app_obj, app_cm_obj))
        # TODO: wait until deployment is all ready
        return app_obj
    return _app_factory