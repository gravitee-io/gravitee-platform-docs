# Quick Install

## Overview

This tutorial assumes you are starting a clean installation and have no existing Access Management data.

## Install with RPMs

```sh
curl -sSL https://bit.ly/install-am-3x | bash
```

For more information, see [Install on Red Hat.](install-on-red-hat.md)

## Install with Docker

```sh
curl -sSL https://bit.ly/docker-am-3x | bash
```

For more information, see [Run in Docker.](run-in-docker/)

## Install with Kubernetes

```sh
# Add Gravitee charts repository
$ helm repo add graviteeio https://helm.gravitee.io

# And install
$ helm install --name graviteeio-am graviteeio/am
```

For more information, see [Deploy in Kubernetes.](deploy-in-kubernetes.md)
