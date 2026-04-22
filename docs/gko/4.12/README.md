# Introduction

## Overview

The Gravitee Kubernetes Operator (GKO) is a [Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) developed by Gravitee that lets you manage Gravitee APIs, applications, and other assets in a Kubernetes-native and declarative way.

GKO allows APIs and other resources to be treated "as-code" so you can implement GitOps workflows to manage your API platform with higher levels of automation, reliability, and collaboration.

GKO is designed to be used in combination with the Gravitee API Management Console, Developer Portal, and Gateway. APIs and applications are examples of resources that GKO can manage and synchronize with the rest of the Gravitee platform.

Resources that are managed by GKO can be synchronized with the API Management control plane but will be displayed as read-only. This is to enforce the fact that the source of truth for these resources is coming from the operator, and not from the GUI.

Choose from the guides below to get started with the Gravitee Kubernetes Operator.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>Quickstart guide</td><td></td><td><a href="getting-started/quickstart-guide.md">quickstart-guide.md</a></td></tr><tr><td></td><td>Install with Helm</td><td></td><td><a href="getting-started/installation/">installation</a></td></tr><tr><td></td><td>Custom Resource Definition introduction</td><td></td><td><a href="overview/custom-resource-definitions/">custom-resource-definitions</a></td></tr><tr><td></td><td>Reference architecture</td><td></td><td><a href="overview/example-architecture.md">example-architecture.md</a></td></tr><tr><td></td><td>API reference</td><td></td><td><a href="reference/api-reference.md">api-reference.md</a></td></tr></tbody></table>
