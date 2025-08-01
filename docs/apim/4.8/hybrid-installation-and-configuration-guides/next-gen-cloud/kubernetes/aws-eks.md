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
* Ensure you have access to [Gravitee Cloud](https://cloud.gravitee.io/), with permissions to install new Gateways.
* Ensure you have access to the EKS cluster where you want to install the Gateway.
* Ensure the self-hosted target environment has outbound Internet connectivity to Gravitee Cloud using HTTPS/443.
* Complete the steps in [#prepare-your-installation](../#prepare-your-installation "mention").



### Install the Gateway&#x20;

To install the Gravitee Gateway, complete the following steps:

1. [#install-redis](aws-eks.md#install-redis "mention")
2. [#prepare-values.yaml-for-helm](aws-eks.md#prepare-values.yaml-for-helm "mention")
3. [#install-with-helm](aws-eks.md#install-with-helm "mention")

### Install Redis

To support caching and rate-limiting, you must install Redis into your Kubernetes cluster. For more information, see [Bitnami package for Redis®](https://artifacthub.io/packages/helm/bitnami/redis).

1.  Install Redis with Helm using the following command, which also creates a new `gravitee-apim` namespace:&#x20;

    ```bash
    helm install gravitee-apim-redis oci://registry-1.docker.io/bitnamicharts/redis --create-namespace --namespace gravitee-apim
    ```
2.  Extract the Redis hostname from the command output and save it for future use. The following sample output lists `gravitee-apim-redis-master.gravitee-apim.svc.cluster.local` as the Redis hostname:

    ```sh
    Pulled: registry-1.docker.io/bitnamicharts/redis:21.2.1
    Digest: sha256:b667ef7d2da1a073754e0499a93bb9acc6539e57ce971da39ee5fd2c222a4024
    NAME: gravitee-apim-redis
    LAST DEPLOYED: DDD MMM DD HH:MM:SS YYYY
    NAMESPACE: gravitee-apim
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    CHART NAME: redis
    CHART VERSION: 21.2.1
    APP VERSION: 8.0.2

    ** Please be patient while the chart is being deployed **

    Redis can be accessed on the following DNS names from within your cluster:

        gravitee-apim-redis-master.gravitee-apim.svc.cluster.local for read/write operations (port 6379)
        gravitee-apim-redis-replicas.gravitee-apim.svc.cluster.local for read-only operations (port 6379)

    To get your password run:
        export REDIS_PASSWORD=$(kubectl get secret --namespace gravitee-apim gravitee-apim-redis -o jsonpath="{.data.redis-password}" | base64 -d)
    ```
3.  Use the following command to output the Redis password. Save this password for future use.

    ```bash
    kubectl get secret --namespace gravitee-apim gravitee-apim-redis -o jsonpath="{.data.redis-password}" | base64 -d
    ```
4.  To verify that your Redis deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-apim-redis
    ```

&#x20;       The command generates the following output:
