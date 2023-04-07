---
description: An overview of Helm charts and Kubernetes operators
---

# Kubernetes

Gravitee API Management (APIM) can be deployed on Kubernetes using either a Helm chart or a Kubernetes operator. Helm charts and Kubernetes operators are both tools for managing and deploying applications on Kubernetes, but they have some important differences.

## Conceptual overview

Helm is a package manager for Kubernetes that simplifies the deployment and management of applications on Kubernetes clusters. Helm packages are called "charts," which are collections of YAML templates that describe the different Kubernetes resources needed to run an application, such as deployments, services, and config maps.

Helm charts provide a convenient way to deploy, update, and manage applications on Kubernetes, making it easier to manage complex applications and configurations. With Helm, you can easily install, upgrade, rollback, and delete applications with just a few commands. However, they don't have the same level of automation and intelligence as Kubernetes operators.

Kubernetes operators allow you to automate advanced application management tasks. In Kubernetes, an operator is not an API object itself, but rather a pattern for building custom controllers that automate the management of complex, stateful applications on Kubernetes. Kubernetes' [operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) concept lets you extend the cluster's behavior without modifying the code of Kubernetes itself by linking [controllers](https://kubernetes.io/docs/concepts/architecture/controller/) to one or more custom resources.&#x20;

Operators are designed to understand the application they manage and can take actions based on that understanding. For example, an operator for a database might automatically scale the number of database instances based on the workload or perform backups and recovery operations automatically.

One key advantage of Kubernetes operators over Helm charts is that they provide a higher level of automation and intelligence for managing complex applications. They can automatically detect and respond to changes in the application or infrastructure, and can handle complex management tasks that would be difficult to do manually.

## Configuration management

Helm charts manage the configuration of an application using a set of configurable parameters that are defined in the chart's `values.yaml` file. The `values.yaml` file is a set of key-value pairs that can be modified to customize the application's behavior.&#x20;

Kubernetes operators manage the configuration of an application using custom resources. Custom resources define the desired state of the application, and the operator's controller ensures that the application's current state matches the desired state.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td>Gravitee Kubernetes Operator Install</td><td></td><td></td></tr><tr><td>Helm Chart Install</td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr></tbody></table>

