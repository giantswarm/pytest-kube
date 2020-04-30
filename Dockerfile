FROM python:3.8-slim

RUN apt update && apt install -y curl docker.io \
  && curl -L https://kind.sigs.k8s.io/dl/v0.7.0/kind-Linux-amd64 \
    -o /usr/local/bin/kind && chmod +x /usr/local/bin/kind \
  && curl -L https://storage.googleapis.com/kubernetes-release/release/v1.18.2/bin/linux/amd64/kubectl \
    -o /usr/local/bin/kubectl && chmod +x /usr/local/bin/kubectl \
  && curl -L https://get.helm.sh/helm-v3.2.0-linux-amd64.tar.gz \
    | tar -zx --strip-components=1 --directory=/usr/local/bin linux-amd64/helm \
  && curl -L https://github.com/giantswarm/gsctl/releases/download/0.20.1/gsctl-0.20.1-linux-amd64.tar.gz \
    | tar -zx --strip-components=1 --directory=/usr/local/bin gsctl-0.20.1-linux-amd64/gsctl 

RUN pip install poetry
ENV POETRY_VIRTUALENVS_CREATE false
WORKDIR /pytest
COPY pyproject.toml poetry.lock ./
RUN poetry install

CMD ["python", "-m", "pytest"]
