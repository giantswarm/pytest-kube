<!--

    TODO:

    - Add the project to the CircleCI:
      https://circleci.com/setup-project/gh/giantswarm/REPOSITORY_NAME

    - Import RELEASE_TOKEN variable from template repository for the builds:
      https://circleci.com/gh/giantswarm/REPOSITORY_NAME/edit#env-vars

    - Change the badge (with style=shield):
      https://circleci.com/gh/giantswarm/REPOSITORY_NAME/edit#badges
      If this is a private repository token with scope `status` will be needed.

    - Run `devctl replace -i "REPOSITORY_NAME" "$(basename $(git rev-parse --show-toplevel))" *.md`
      and commit your changes.

    - If the repository is public consider adding godoc badge. This should be
      the first badge separated with a single space.
      [![GoDoc](https://godoc.org/github.com/giantswarm/REPOSITORY_NAME?status.svg)](http://godoc.org/github.com/giantswarm/REPOSITORY_NAME)

-->
[![CircleCI](https://circleci.com/gh/giantswarm/template.svg?style=shield&circle-token=cbabd7d13186f190fca813db4f0c732b026f5f6c)](https://circleci.com/gh/giantswarm/template)

# pytest-kube



```bash
docker build -t local/pytest-kube .

docker run -ti \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --network host \
  -v $PWD:/pytest \
  local/pytest-kube
```



## Hints for development

```bash
# add a python package to pyproject.toml
docker run -ti -v $PWD:$PWD -w $PWD -- local/pytest-kube \
  poetry add --dev git+https://github.com/hjacobs/pytest-kind@master

# update package versions in pyproject.toml
docker run -ti -v $PWD:$PWD -w $PWD -- local/pytest-kube \
  poetry update
```
