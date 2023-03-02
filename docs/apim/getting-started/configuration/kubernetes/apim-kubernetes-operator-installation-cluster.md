---
title: Deploying GKO on a Kubernetes cluster
tags:
  - Gravitee Kubernetes Operator
  - GKO
  - Introduced in version 3.19.0
  - BETA release
  - Deployment
  - Cluster
  - K8s
---

# Deploying GKO on a Kubernetes cluster

## Overview

This section provides steps on how to deploy the Gravitee Kubernetes
Operator (GKO) on an existing APIM-ready Kubernetes cluster.

!!! info "Cluster availability"
    If you do not have an existing cluster you can deploy to, you can set up a new local cluster - see the [local cluster installation section](apim-kubernetes-operator-installation-local.md) for details. Once you have the local cluster set up and running, return to this section to deploy the GKO.

!!! info "Multiple clusters"
    If your architecture requires the management of multiple Kubernetes clusters with a different set of APIs for each cluster, you should deploy the GKO separately on each cluster. Follow the deployment process described below for each cluster deployment.

## Prerequisites

Before you start the deployment process, ensure that you have access to an APIM-ready Kubernetes cluster.

By default the Kubernetes synchronizer is configured to look for API definitions in the API Gateway namespace. To watch all namespaces you must set the property `services.sync.kubernetes.namespaces` to `all` in the Gateway configuration. You can also provide a specific list of namespaces to watch.

It is also recommended to check the current Kubernetes context to ensure that it is set to the correct cluster. To do this, run the following command:

```
kubectl config current-context
```

See the [Kubernetes documentation](https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-context-and-configuration) for more information on displaying a list of contexts and setting your current context.

## Deploying the GKO on the cluster

### STEP 1: Run the deployment script

Run the following command in your command-line tool (the working directory does not matter) to deploy the GKO on the cluster of your current Kubernetes context:

```
kubectl apply -f https://github.com/gravitee-io/gravitee-kubernetes-operator/releases/latest/download/bundle.yml
```

The operation is quick and the successful command-line output should be similar to one in the example below:

```
namespace/gko-system created
customresourcedefinition.apiextensions.k8s.io/apidefinitions.gravitee.io created
customresourcedefinition.apiextensions.k8s.io/managementcontexts.gravitee.io created
serviceaccount/gko-controller-manager created
role.rbac.authorization.k8s.io/gko-leader-election-role created
clusterrole.rbac.authorization.k8s.io/gko-manager-role created
clusterrole.rbac.authorization.k8s.io/gko-metrics-reader created
clusterrole.rbac.authorization.k8s.io/gko-proxy-role created
rolebinding.rbac.authorization.k8s.io/gko-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/gko-manager-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/gko-proxy-rolebinding created
configmap/gko-manager-config created
service/gko-controller-manager-metrics-service created
deployment.apps/gko-controller-manager created
```

The GKO has now been deployed on your cluster.

### STEP 2: Check if the Gravitee CRDs are available on your cluster

Run the following command:

```
kubectl get crd
```

The command-line output should include `apidefinitions.gravitee.io` and `managementcontexts.gravitee.io`, as shown in the example below:

```
NAME                              CREATED AT
addons.k3s.cattle.io              2022-09-28T10:25:02Z
helmcharts.helm.cattle.io         2022-09-28T10:25:02Z
helmchartconfigs.helm.cattle.io   2022-09-28T10:25:02Z
apidefinitions.gravitee.io        2022-09-28T10:34:38Z
managementcontexts.gravitee.io    2022-09-28T10:34:38Z
```
