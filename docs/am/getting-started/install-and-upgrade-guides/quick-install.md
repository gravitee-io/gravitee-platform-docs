# Quick Install

## Overview

This tutorial assumes you are starting a clean installation and have no existing Access Management data.

## Install with RPMs

```sh
curl -sSL https://bit.ly/install-am-3x | bash
```

For more information, see [Install on Red Hat](https://docs.gravitee.io/am/current/am\_installguide\_redhat\_stack.html).

## Install with Docker

```sh
curl -sSL https://bit.ly/docker-am-3x | bash
```

For more information, see [Run on Docker](https://docs.gravitee.io/am/current/am\_installguide\_docker\_compose.html).

## Install with Kubernetes

```sh
# Add Gravitee.io charts repository
$ helm repo add graviteeio https://helm.gravitee.io

# And install
$ helm install --name graviteeio-am graviteeio/am
```

For more information, see [Deploy in Kubernetes](https://docs.gravitee.io/am/current/am\_installguide\_kubernetes.html).
