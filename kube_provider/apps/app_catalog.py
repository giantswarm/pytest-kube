from pykube import HTTPClient
from pykube.objects import APIObject, object_factory
import pytest
from typing import Callable, Iterator

AppCatalogFactoryFunc = Callable[[str, str], APIObject]


class GiantSwarmAppPlatformCRs:
    def __init__(self, kube_client: HTTPClient):
        super().__init__()
        self.app_cr_factory = object_factory(
            kube_client, "application.giantswarm.io/v1alpha1", "App")
        self.app_catalog_cr_factory = object_factory(
            kube_client, "application.giantswarm.io/v1alpha1", "AppCatalog")


def get_app_catalog_obj(catalog_name: str, catalog_uri: str,
                        kube_client: HTTPClient) -> APIObject:
    app_catalog_cr = {
        "apiVersion": "application.giantswarm.io/v1alpha1",
        "kind": "AppCatalog",
        "metadata": {
            "labels": {
                "app-operator.giantswarm.io/version": "1.0.0",
                "application.giantswarm.io/catalog-type": "",
            },
            "name": catalog_name,
        },
        "spec": {
            "description": "Catalog for testing.",
            "storage": {
                "URL": catalog_uri,
                "type": "helm",
            },
            "title": catalog_name,
        }
    }
    crs = GiantSwarmAppPlatformCRs(kube_client)
    return crs.app_catalog_cr_factory(kube_client, app_catalog_cr)


@pytest.fixture(scope="module")
def app_catalog_factory(kube_client: HTTPClient) -> Iterator[AppCatalogFactoryFunc]:
    created_catalogs = []

    def _app_catalog_factory(name: str, url: str = "") -> APIObject:
        if url == "":
            url = "https://giantswarm.github.io/{}-catalog/".format(name)
        api_obj = get_app_catalog_obj(name, url, kube_client)
        created_catalogs.append(api_obj)
        api_obj.create()
        # TODO: check that app catalog is present
        return api_obj

    yield _app_catalog_factory
    for catalog in created_catalogs:
        catalog.delete()
        # TODO: wait until finalizer is gone and object is deleted
