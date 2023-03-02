---
title: Deploying GKO on a Kubernetes cluster
tags:
  - Gravitee Kubernetes Operator
  - GKO
  - Introduced in version 3.19.0
  - BETA release
  - Deployment
  - Local cluster
  - K8s
---

# Setting up a local cluster for deployment

## Overview

If you do not have an existing APIM-ready Kubernetes cluster you can deploy the GKO on, you can create and set up a local cluster on your machine. This process is described below and involves the following stages:

1.  Set up your environment (prerequisite step).
2.  Create a local APIM-ready Kubernetes cluster.
3.  Monitor the APIM pods startup until they are ready.
4.  Check if the Console is up and running.

After the local cluster setup, the next steps are to:

1. [Deploy the GKO on the cluster](apim-kubernetes-operator-installation-cluster.md).
2. [Try out the GKO functionality](apim-kubernetes-operator-user-guide-play.md).

!!! warning

    It is strongly recommended to only use local GKO cluster deployments for testing purposes - never in production.

## Prerequisites

Before you start, you need to have the following software set up and running on your machine:

- [Docker](https://www.docker.com/).
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).
- [Helm](https://helm.sh/docs/intro/install/).
- [Node.js](https://nodejs.org/en/download/).
- [curl](https://curl.se/) in case you do not have it already - to check, type `curl -V` in your command-line tool.
- A standard command-line tool of your choice.

The GKO GitHub repository is public and available [here](https://github.com/gravitee-io/gravitee-kubernetes-operator). Cloning it is not a requirement for this installation process, so this is just for your reference.

## STEP 1: Create a local cluster

To create a local APIM-ready Kubernetes cluster, run the following command:

```
curl -s https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/master/scripts/k3d.mjs | npx zx
```

This operation may take a few minutes to complete.

!!! note

    This script has only been tested on Mac machines.

Make note of the endpoints listed at the end of the command-line output:

```
    (...)

    Available endpoints are:

        Gateway       http://localhost:9000/gateway
        Management    http://localhost:9000/management
        Console       http://localhost:9000/console/#!/login

    To update APIM components (e.g. APIM Gateway) to use a new docker image run:

    > docker tag <image> k3d-graviteeio.docker.localhost:12345/graviteeio/apim-gateway:3.19
    > docker push k3d-graviteeio.docker.localhost:12345/graviteeio/apim-gateway:3.19
    > kubectl rollout restart deployment apim-apim3-gateway
```

## STEP 2: Monitor the APIM pods startup until they are ready

The pods will take some time to start and must become ready before you can deploy the GKO (described in the next step).

To monitor from the command line, run the following command:

```
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=apim3 --timeout 360s
```

After some time, the command-line output should look similar to the example below:

```
    pod/apim-apim3-api-7b8b85d79-b7hkh condition met
    pod/apim-apim3-ui-5997c5d5c7-r9xdj condition met
    pod/apim-apim3-gateway-66cbd5c9d9-tv5jz condition met
```

You can increase the timeout if your machine is slower. If you encounter an error, you will not be able to proceed to the next steps - please contact Gravitee for assistance with this.

## STEP 3: Check if the API Console is up and running

As noted in step 1 above, you can use your Console endpoint created with the cluster to check if the Console is up and running.

To do so, open the Console endpoint URL in your browser - for example:

[http://localhost:9000/console/#!/login](http://localhost:9000/console/#!/login)

Log in the Console - the default local login credentials are `admin`/`admin`.

The Console dashboard should show one application running in the "Number of Applications" section of the Console dashboard:

![](/images/apim/3.x/kubernetes/gko-deployment-local-console-1.png)
