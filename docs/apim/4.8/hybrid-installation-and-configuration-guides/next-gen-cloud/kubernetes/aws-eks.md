---
hidden: true
noIndex: true
---

# AWS EKS

This is a step-by-step guide to install a self-hosted gateway on your EKS cluster connecting to Gravitee Cloud (Next-Gen).

### Overview&#x20;

This guide explains how to install and connect a Hybrid Gateway to Gravitee Cloud using Amazon Elastic Kubernetes Service (EKS).

### Prerequisites&#x20;

* Install [helm](https://helm.sh/docs/intro/install/).
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
* Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* Configure AWS CLI with appropriate credentials: `aws configure`
* Ensure you have access to Gravitee Cloud, with permissions to install new Gateways.
* Ensure you have access to the EKS cluster where you want to install the Gateway.
* Ensure the self-hosted target environment has outbound Internet connectivity to Gravitee Cloud using HTTPS/443.
* Complete the steps in **Prepare your installation**.
