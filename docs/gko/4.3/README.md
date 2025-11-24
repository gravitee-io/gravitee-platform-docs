---
description: Overview of GKO
---

# Introduction

## Overview

The Gravitee Kubernetes Operator (GKO) is a [Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) developed by Gravitee that provides the ability to manage Gravitee APIs, applications and other assets in a Kubernetes-native and declarative way.&#x20;

GKO allows APIs and other resources to be managed "as-code", unlocking the possibility to implement GitOps workflows that provide high levels of automation, reliability, and collaboration in the way you manage your API platform.

GKO is designed to be used in combination with the Gravitee API Management Console, Developer Portal, and Gateway. APIs and Applications are examples of resources that GKO can manage and synchronize with the rest of the Gravitee platform.

Resources that are managed by GKO can be synchronized with the API Management control plane but will be displayed as read-only. This is to enforce the fact that the source of truth for these resources is coming from the Operator, and not from the GUI.&#x20;

