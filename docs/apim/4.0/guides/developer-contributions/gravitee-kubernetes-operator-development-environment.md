---
description: An overview about Gravitee Kubernetes Operator Development Environment.
---

# Gravitee Kubernetes Operator Development Environment

## Overview <a href="#user-content-initialize-your-environment" id="user-content-initialize-your-environment"></a>

The Gravitee Kubernetes Operator (GKO) can define, deploy, and publish APIs to your API Developer Portal and API Gateway with custom resource definitions (CRDs). This guide is focused on how to set up your development environment. You can learn more about the functionality of the GKO in [this guide.](../gravitee-kubernetes-operator/)

## Initialize your environment <a href="#user-content-initialize-your-environment" id="user-content-initialize-your-environment"></a>

* Install [Docker](https://www.docker.com/)
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* Install [Helm](https://helm.sh/docs/intro/install/)
* Install [NodeJs](https://nodejs.org/en/download/)
* Install the operator-sdk: `brew install operator-sdk`

## Install tooling for development <a href="#user-content-install-tooling-for-development" id="user-content-install-tooling-for-development"></a>

You can install the necessary tools to run the make targets used during development with the following command:

<pre class="language-sh"><code class="lang-sh"><strong>make install-tools
</strong></code></pre>

To get more information about the available make targets, run:

```sh
make help
```

## Run the operator locally <a href="#user-content-run-the-operator-locally" id="user-content-run-the-operator-locally"></a>

To run the operator locally against an APIM-ready [k3d](https://k3d.io/) cluster, run the following commands:

```sh
# Initialize a local kubernetes cluster running APIM
$ make k3d-init

# Install the operator CRDs into the cluster
$ make install

# Run the operator controller on your local machine
$ make run
```

### Debug the operator and APIM <a href="#user-content-debug-the-operator-and-apim" id="user-content-debug-the-operator-and-apim"></a>

To be able to run the operator against a local instance of APIM Gateway and APIM Management API, you will need to:

* Attach to a local cluster context
* Create a local service account to authenticate the Gateway against the local cluster
* Create a Management Context pointing to your local APIM Management API
* Run what you need to debug in debug mode

```sh
# Create a service account token with 'cluster-admin' role in the current context and
# use this token to authenticate against the current cluster
$ make k3d-admin

$ make run # or run using a debugger if you need to debug the operator as well

# Create the debug Management Context resource for APIM
$ kubectl apply -f ./config/samples/context/debug/api-context-with-credentials.yml

# Create a basic API Definition resource
$ kubectl apply -f ./config/samples/apim/api-with-context.yml
```

## Run the operator as a deployment on the k3d cluster <a href="#user-content-run-the-operator-as-a-deployment-on-the-k3d-cluster" id="user-content-run-the-operator-as-a-deployment-on-the-k3d-cluster"></a>

Some features and behaviors of the operator can only be tested when running it as a deployment on the k3d cluster.

For example, this is the case for [webhooks](https://sdk.operatorframework.io/docs/building-operators/golang/webhook/) or when testing an operator deployed in multiple namespaces.

You can deploy the operator on your k3d cluster by running the following commands:

```sh
make k3d-build k3d-push k3d-deploy
```

## Troubleshooting <a href="#user-content-troubleshooting" id="user-content-troubleshooting"></a>

The k3d registry host used to share images between your host and your k3d cluster is defined as `k3d-graviteeio.docker.localhost`. On most linux / macos platforms, `` *.localhost` `` should resolve to 127.0.0.1. If this is not the case on your machine, you need to add the following entry to your `/etc/hosts` file:

```
127.0.0.1 k3d-graviteeio.docker.localhost
```
