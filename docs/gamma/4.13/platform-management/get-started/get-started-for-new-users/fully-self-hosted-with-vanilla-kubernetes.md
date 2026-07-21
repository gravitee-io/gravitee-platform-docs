---
hidden: false
noIndex: false
---
# Fully self-hosted installation with Vanilla Kubernetes

Gravitee Gamma is Gravitee's next-generation unified control plane. It brings API Management, Event Management, Agent Management, Authorization Management, and Platform Management together in a single console, so you manage your APIs, Kafka streams, AI agents and MCP servers, and authorization policies from one place.

To run a full Gamma platform yourself on Kubernetes, install the Helm chart with the guide for your cluster. Each guide uses the same chart and turns on Gamma, with ingress tailored to the platform.

## Choose a Kubernetes guide

* [Install Gamma on Vanilla Kubernetes](../../install/self-hosted-installation-guides/kubernetes/vanilla-kubernetes.md): the standard Helm install for Docker Desktop, minikube, or any vanilla cluster.
* [Install Gamma on AWS EKS](../../install/self-hosted-installation-guides/kubernetes/aws-eks.md): a managed cluster on Amazon, fronted by an AWS load balancer.
* [Install Gamma on Azure AKS](../../install/self-hosted-installation-guides/kubernetes/azure-aks.md): a managed cluster on Azure, fronted by an NGINX ingress.
* [Install Gamma on OpenShift](../../install/self-hosted-installation-guides/kubernetes/openshift.md): an OpenShift cluster, served through edge-terminated Routes.
* **Hybrid on Kubernetes:** run a self-hosted Helm Gateway against a Gravitee Cloud (Next-Gen Cloud) control plane. See the hybrid Kubernetes guides for [Vanilla Kubernetes](../../install/hybrid-installation-guides/kubernetes/vanilla-kubernetes.md), [AWS EKS](../../install/hybrid-installation-guides/kubernetes/aws-eks.md), [Azure AKS](../../install/hybrid-installation-guides/kubernetes/azure-aks.md), or [OpenShift](../../install/hybrid-installation-guides/kubernetes/openshift.md).

## What to expect

Every guide serves the Gamma console and the Management API on a single host so the console can sign in. The default username and password for the consoles are both `admin`.

## Next steps

* Once Gamma is running, create your first MCP server. For more information, see [Create your first MCP server](../../../agent-management/get-started/create-your-first-mcp-server.md).
