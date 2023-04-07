# Kubernetes

Gravitee API Management (APIM) can be deployed on Kubernetes using either a Helm chart or a Kubernetes Operator. The core differences between Gravitee's Helm chart and Kubernetes Operator can be broken into four main categories:

* Installation process
* Configuration management
* Lifecycle management
* Upgradeability

At the most basic level, Gravitee's Helm chart and Kubernetes Operator both offer different approaches for deploying and managing applications on Kubernetes. The Helm chart is a package manager that simplifies the installation and management of applications, while Kubernetes Operator is a Kubernetes-native way to manage complex applications using custom resources and controllers. The choice between the two depends on the requirements of the application and the organization's operational processes.

## Installation Process

The Helm chart is a package manager for Kubernetes that simplifies the installation and management of applications on a Kubernetes cluster. It uses a set of YAML files to describe the deployment configuration and dependencies of an application. On the other hand, Kubernetes Operator is a Kubernetes-native way to manage complex applications. It uses custom resources and controllers to automate the deployment, scaling, and management of applications.

## Configuration management

Helm Chart manages the configuration of an application using a set of configurable parameters that are defined in the Chart's `values.yaml` file. The `values.yaml` file is a set of key-value pairs that can be modified to customize the application's behavior. In contrast, Kubernetes Operator manages the configuration of an application using custom resources. Custom resources define the desired state of the application, and the operator's controller ensures that the application's current state matches the desired state.

## Lifecycle management

Helm Chart manages the lifecycle of an application using a set of pre-defined Kubernetes objects such as Deployments, Services, ConfigMaps, etc. It can be used to deploy, update, and delete an application using the Helm command-line interface. Kubernetes Operator manages the lifecycle of an application using custom resources and controllers. It can be used to automate the deployment, scaling, and management of an application.

## Upgradability

Helm Chart provides an easy way to upgrade the application by modifying the Chart's values.yaml file and using the Helm command-line interface. The upgrade process is straightforward but requires manual intervention. On the other hand, Kubernetes Operator provides an automated upgrade process by managing the entire lifecycle of the application. The operator can upgrade the application automatically based on the custom resource's desired state.

