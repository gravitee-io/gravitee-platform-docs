---
description: Step-by-step tutorial for Traffic Manager.
noIndex: true
---

# Using the Traffic Manager

Blackbird cluster (powered by Telepresence) uses a Traffic Manager to route cloud traffic to and from the user. The Traffic Manager is deployed in your cluster using [Helm](https://helm.sh), which is integrated into the `telepresence` binary. This binary includes both Helm and a Helm chart for the Traffic Manager to ensure version consistency between the binary and the deployed components.

> **Note:** If you're a former Telepresence user who's now working in Blackbird, you must install the latest Blackbird CLI and Traffic Manager. Previously installed Traffic Managers from Telepresence are incompatible. For more information, see [#getting-started-with-the-blackbird-cli](../../../technical-reference/blackbird-cli/#getting-started-with-the-blackbird-cli "mention") and [#installing-the-traffic-manager](using-the-traffic-manager.md#installing-the-traffic-manager "mention").

## Provider prerequisites

### Google Kubernetes Engine

If you're using a private Google Kubernetes Engine (GKE) cluster, the default firewall settings will block the Kubernetes API server from calling the Traffic Manager's webhook injector. To ensure Blackbird functions properly, you'll need to [add a firewall rule](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#add_firewall_rules) to allow Kubernetes masters to access TCP port 8443 in your pods.

For example, for a cluster named `tele-webhook-gke` in region `us-central1-c1`:

```bash
$ gcloud container clusters describe tele-webhook-gke --region us-central1-c | grep masterIpv4CidrBlock
  masterIpv4CidrBlock: 172.16.0.0/28 # Take note of the IP range, 172.16.0.0/28

$ gcloud compute firewall-rules list \
    --filter 'name~^gke-tele-webhook-gke' \
    --format 'table(
        name,
        network,
        direction,
        sourceRanges.list():label=SRC_RANGES,
        allowed[].map().firewall_rule().list():label=ALLOW,
        targetTags.list():label=TARGET_TAGS
    )'

NAME                                  NETWORK           DIRECTION  SRC_RANGES     ALLOW                         TARGET_TAGS
gke-tele-webhook-gke-33fa1791-all     tele-webhook-net  INGRESS    10.40.0.0/14   esp,ah,sctp,tcp,udp,icmp      gke-tele-webhook-gke-33fa1791-node
gke-tele-webhook-gke-33fa1791-master  tele-webhook-net  INGRESS    172.16.0.0/28  tcp:10250,tcp:443             gke-tele-webhook-gke-33fa1791-node
gke-tele-webhook-gke-33fa1791-vms     tele-webhook-net  INGRESS    10.128.0.0/9   icmp,tcp:1-65535,udp:1-65535  gke-tele-webhook-gke-33fa1791-node
# Take note of the TARGET_TAGS value, gke-tele-webhook-gke-33fa1791-node

$ gcloud compute firewall-rules create gke-tele-webhook-gke-webhook \
    --action ALLOW \
    --direction INGRESS \
    --source-ranges 172.16.0.0/28 \
    --rules tcp:8443 \
    --target-tags gke-tele-webhook-gke-33fa1791-node --network tele-webhook-net
Creating firewall...⠹Created [https://www.googleapis.com/compute/v1/projects/datawire-dev/global/firewalls/gke-tele-webhook-gke-webhook].
Creating firewall...done.
NAME                          NETWORK           DIRECTION  PRIORITY  ALLOW     DENY  DISABLED
gke-tele-webhook-gke-webhook  tele-webhook-net  INGRESS    1000      tcp:8443        False
```

#### GKE authentication plugin

Starting with Kubernetes version 1.26, GKE requires the use of the [gke-gcloud-auth-plugin](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke). You'll need to install this plugin to use Blackbird with Docker while using GKE.

### Amazon Elastic Kubernetes Service plugin

If you're using an Amazon Web Services (AWS) CLI version earlier than `1.16.156`, you need to install the [aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html). This plugin allows you to use Blackbird with Docker while using Amazon Elastic Kubernetes (EKS).

## Installing the Traffic Manager

You can install the Traffic Manager in one of three ways:

* [#install-the-traffic-manager-using-the-blackbird-cli](using-the-traffic-manager.md#install-the-traffic-manager-using-the-blackbird-cli "mention")
* [#install-the-traffic-manager-into-a-custom-namespace-using-the-blackbird-cli](using-the-traffic-manager.md#install-the-traffic-manager-into-a-custom-namespace-using-the-blackbird-cli "mention")
* [#install-the-traffic-manager-with-a-custom-configuration-using-the-blackbird-cli](using-the-traffic-manager.md#install-the-traffic-manager-with-a-custom-configuration-using-the-blackbird-cli "mention")

### Install the Traffic Manager using the Blackbird CLI

You can perform a basic installation of the Traffic Manager with default settings.

**To perform a basic install:**

1.  Run the following command.

    ```shell
    blackbird cluster helm install
    ```

### Install the Traffic Manager into a custom namespace using the Blackbird CLI

You can install the Traffic Manager into any namespace.

**To install into a custom namespace:**

1.  Run the `install` command with the `--namespace` flag.

    ```shell
    blackbird cluster install --namespace [namespace]
    ```

    > **Note:** If you don't want to create a namespace, you can also pass `--create-namespace=false`.
2.  Add the namespace to your kubeconfig using kubectl.

    ```yaml
    apiVersion: v1
    clusters:
    - cluster:
        server: https://127.0.0.1
        extensions:
        - name: telepresence.io
          extension:
            manager:
              namespace: [namespace]
      name: example-cluster
    ```

### Install the Traffic Manager with a custom configuration using the Blackbird CLI

You can modify the deployment settings by passing custom values to Helm during installation.

**To install with a custom configuration:**

1. Create a values.yaml file with your custom config values.
2. Run the `install` command with one of the following:
   *   Use the `--values` flag set to the path to your values file.

       ```shell
       blackbird cluster helm install --values values.yaml
       ```
   *   Use the `--set` flag to define items like logging levels.

       ```shell
       blackbird cluster helm install --set logLevel=debug
       ```
