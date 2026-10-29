---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/getting-started/install-and-upgrade-guides/quick-install
description: Install Access Management 4.14 quickly on a clean environment. Compare installing with RPMs, Docker, or Kubernetes and follow your chosen path.
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

For more information, see [Run in Docker.](run-in-docker/README.md)

## Install with Kubernetes

The chart doesn't deploy a database. Before you install it, prepare MongoDB or a relational database that AM supports, and configure it in your Helm values file, as described in [Configure backend](deploy-in-kubernetes.md#configure-backend).

```sh
# Add Gravitee charts repository
$ helm repo add graviteeio https://helm.gravitee.io

# And install, with the values file that configures your database
$ helm install graviteeio-am4x graviteeio/am -f values.yaml
```

For more information, see [Deploy in Kubernetes.](deploy-in-kubernetes.md)
