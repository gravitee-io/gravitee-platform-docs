---
description: Installation guide for Access Management.
---

# Quick Install

## Overview

This tutorial assumes you are starting a clean installation and have no existing Access Management data.

## Install with RPMs

{% code overflow="wrap" %}
```sh
curl -sSL https://raw.githubusercontent.com/gravitee-io/scripts/master/am/4.x/install.sh | bash
```
{% endcode %}

For more information, see [Install on Red Hat.](install-on-red-hat.md)

## Install with Docker

{% code overflow="wrap" %}
```sh
curl -sSL https://raw.githubusercontent.com/gravitee-io/graviteeio-access-management/master/docker/launch.sh | bash
```
{% endcode %}

For more information, see [Run in Docker.](run-in-docker/)

## Install with Kubernetes

```sh
# Add Gravitee charts repository
$ helm repo add graviteeio https://helm.gravitee.io

# And install
$ helm install graviteeio-am4x graviteeio/am
```

For more information, see [Deploy in Kubernetes.](deploy-in-kubernetes.md)
