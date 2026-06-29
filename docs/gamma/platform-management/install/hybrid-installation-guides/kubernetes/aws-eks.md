---
hidden: false
noIndex: false
---
# Install a hybrid Gamma Gateway on AWS EKS
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

Gravitee Gamma supports hybrid deployments, so you run the data plane in your own infrastructure while Gravitee hosts and manages the control plane. In a hybrid setup, the platform splits into two planes:

* **Control plane**: managed by Gravitee in the cloud. It runs the Management API with Gamma enabled, the Gamma console, the APIM Console, and the Developer Portal, and it handles design, publishing, configuration, analytics, and lifecycle management.
* **Data plane**: deployed and managed by you, close to your backend services. It enforces policies, applies security, and routes traffic.

This guide covers the data plane only. You deploy the Gravitee Gateway and Redis on Amazon Elastic Kubernetes Service (EKS) with Helm, and you expose the Gateway through an AWS Application Load Balancer (ALB). The Gateway connects to your Gravitee Cloud control plane with a Cloud Token and a License Key. Redis provides rate limiting at the edge.

## Prerequisites

Before you install the Gateway, complete the following steps:

* Install the [AWS CLI](https://aws.amazon.com/cli/), [eksctl](https://eksctl.io/), [helm](https://helm.sh/docs/intro/install/), and [kubectl](https://kubernetes.io/docs/tasks/tools/).
* Have a running EKS cluster with outbound Internet connectivity to Gravitee Cloud over HTTPS/443, and point `kubectl` at it:

  ```bash
  aws eks update-kubeconfig --name <cluster-name> --region <region>
  ```
* A hostname you control (for example, `gateway.example.com`) and, for HTTPS, an [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/) certificate for it.
* Obtain a Gravitee Cloud account. To register for a Gravitee Cloud account, go to the [Gravitee Cloud sign in page](https://cloud.gravitee.io), and then click **Register**.
* Ensure you have access to Gravitee Cloud, with permissions to install new Gateways.
* From your Gravitee Cloud account, obtain your **Cloud Token** and **License Key** for the hybrid Gateway.

## Configure the load balancer controller

The ALB controller turns the Gateway ingress into an ALB. How you get it depends on your cluster type.

{% hint style="info" %}
Check your cluster type with `kubectl get ingressclass`. If it returns nothing and your cluster is **EKS Auto Mode**, follow [EKS Auto Mode](#eks-auto-mode). Otherwise follow [Standard EKS](#standard-eks).
{% endhint %}

### EKS Auto Mode

On EKS Auto Mode, AWS manages the load balancer controller. You only create an `IngressClass` that points at the managed ALB controller.

1. Create a file named `alb-ingressclass.yaml` with the following content:

   ```yaml
   apiVersion: eks.amazonaws.com/v1
   kind: IngressClassParams
   metadata:
     name: alb
   spec:
     scheme: internet-facing
   ---
   apiVersion: networking.k8s.io/v1
   kind: IngressClass
   metadata:
     name: alb
   spec:
     controller: eks.amazonaws.com/alb
     parameters:
       apiGroup: eks.amazonaws.com
       kind: IngressClassParams
       name: alb
   ```
2. Apply it using the following command:

   ```bash
   kubectl apply -f alb-ingressclass.yaml
   ```

### Standard EKS

On a standard (non-Auto Mode) cluster, you install the AWS Load Balancer Controller yourself so the ingress can provision an ALB. AWS maintains the controller and its IAM policy. For more information, see the [AWS Load Balancer Controller installation guide](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/deploy/installation/).

1. Download the IAM policy the controller requires:

   ```bash
   curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
   ```
2. Create the IAM policy from that file. Replace `<region>`:

   ```bash
   aws iam create-policy \
     --policy-name AWSLoadBalancerControllerIAMPolicy \
     --policy-document file://iam_policy.json \
     --region <region>
   ```
3. Create an IAM service account bound to that policy. Replace `<cluster-name>` and `<region>`:

   ```bash
   eksctl create iamserviceaccount \
     --cluster=<cluster-name> --namespace=kube-system --name=aws-load-balancer-controller \
     --role-name AmazonEKSLoadBalancerControllerRole \
     --attach-policy-arn=arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):policy/AWSLoadBalancerControllerIAMPolicy \
     --region=<region> --approve --override-existing-serviceaccounts
   ```
4. Install the controller. Replace `<cluster-name>` and `<region>`:

   ```bash
   helm repo add eks https://aws.github.io/eks-charts
   helm repo update
   helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
     -n kube-system --set clusterName=<cluster-name> \
     --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller \
     --set region=<region>
   ```

#### Verification

* Confirm the controller pods are running using the following command:

  ```bash
  kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
  ```

## Install the Gateway

To install the Gateway, complete the following steps:

1. [#create-the-namespace](#create-the-namespace "mention")
2. [#install-redis](#install-redis "mention")
3. [#prepare-the-values-yaml-for-helm](#prepare-the-values-yaml-for-helm "mention")
4. [#install-with-helm](#install-with-helm "mention")

### Create the namespace

```bash
kubectl create namespace gravitee-gamma
```

### Install Redis

Redis is the rate-limit store for the data plane. Install it with Helm. For more information, see the [Bitnami package for Redis](https://artifacthub.io/packages/helm/bitnami/redis).

1. Install Redis using the following command:

   ```bash
   helm install gravitee-gamma-redis oci://registry-1.docker.io/bitnamicharts/redis \
     --version 19.6.4 \
     --namespace gravitee-gamma \
     --set image.repository=bitnamilegacy/redis
   ```
2. From the command output, save the Redis hostname (`gravitee-gamma-redis-master.gravitee-gamma.svc.cluster.local`).
3. Output the Redis password and save it for the next step:

   ```bash
   kubectl get secret --namespace gravitee-gamma gravitee-gamma-redis -o jsonpath="{.data.redis-password}" | base64 -d
   ```

{% hint style="info" %}
Redis requests a persistent volume. If the Redis pod stays `Pending`, ensure your cluster has a default storage class. On EKS, the [Amazon EBS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html) provides one.
{% endhint %}

### Prepare the `values.yaml` for Helm

The Helm values deploy the Gateway only. They disable the control-plane components, point the Gateway at Redis, connect it to Gravitee Cloud, and expose it through an ALB ingress.

1. Create a `values.yaml` file. Replace `gateway.example.com` with your hostname, the ACM certificate ARN with yours, and the Cloud Token, License Key, Redis hostname, and Redis password with your values:

   ```yaml
   # The License Key from your Gravitee Cloud account
   license:
     key: "<license-key>"

   # The control-plane components run in Gravitee Cloud, so they stay disabled.
   api:
     enabled: false
   portal:
     enabled: false
   ui:
     enabled: false
   gammaUi:
     enabled: false
   alerts:
     enabled: false
   es:
     enabled: false

   gateway:
     replicaCount: 1
     image:
       # We recommend running the same Gateway version as your Gamma control plane, shown in Gravitee Cloud.
       repository: graviteeio/apim-gateway
       tag: 4.12.0
       pullPolicy: IfNotPresent
     autoscaling:
       enabled: false
     # The Cloud Token registers the Gateway with your Gravitee Cloud control plane.
     env:
       - name: gravitee_cloud_token
         value: "<cloud-token>"
     services:
       metrics:
         enabled: true
         prometheus:
           enabled: true
       core:
         http:
           enabled: true
       sync:
         kubernetes:
           enabled: false
       bridge:
         enabled: false
     service:
       type: ClusterIP
       externalPort: 80
       internalPort: 8082
       internalPortName: http
     # Expose the Gateway through an AWS Application Load Balancer.
     ingress:
       enabled: true
       pathType: Prefix
       path: /
       ingressClassName: "alb"
       hosts:
         - gateway.example.com
       annotations:
         alb.ingress.kubernetes.io/scheme: internet-facing
         alb.ingress.kubernetes.io/target-type: ip
         alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
         # Uncomment to redirect HTTP to HTTPS:
         # alb.ingress.kubernetes.io/ssl-redirect: '443'
         # Uncomment and set your ACM certificate ARN for HTTPS:
         # alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/certificate-id
     resources:
       limits:
         cpu: 500m
         memory: 1024Mi
       requests:
         cpu: 200m
         memory: 512Mi
     deployment:
       revisionHistoryLimit: 1
       strategy:
         type: RollingUpdate
         rollingUpdate:
           maxUnavailable: 0
     reporters:
       file:
         enabled: false
     terminationGracePeriod: 50
     gracefulShutdown:
       delay: 20
       unit: SECONDS
     ratelimit:
       redis:
         host: "<redis-hostname>"
         port: 6379
         password: "<redis-password>"
         ssl: false

   ratelimit:
     type: redis
   ```

2. Save your `values.yaml` file in your working directory.

### Install with Helm

1. Add the Gravitee Helm repository:

   ```bash
   helm repo add graviteeio https://helm.gravitee.io
   helm repo update
   ```
2. Install the chart into the `gravitee-gamma` namespace:

   ```bash
   helm install graviteeio-gamma-gateway graviteeio/apim \
     --namespace gravitee-gamma \
     -f ./values.yaml
   ```
3. Get the ALB hostname and point your DNS record (`gateway.example.com`) at it:

   ```bash
   kubectl get ingress -n gravitee-gamma
   ```

{% hint style="info" %}
To uninstall the hybrid Gateway, use the following command:

```bash
helm uninstall graviteeio-gamma-gateway --namespace gravitee-gamma
```
{% endhint %}

## Verification

To verify that your Gateway is up and connected, complete the following steps:

1. [#ensure-the-gateway-registers-in-gravitee-cloud](#ensure-the-gateway-registers-in-gravitee-cloud "mention")
2. [#validate-the-pods](#validate-the-pods "mention")
3. [#validate-the-gateway-url](#validate-the-gateway-url "mention")

### Ensure the Gateway registers in Gravitee Cloud

* Sign in to [Gravitee Cloud](https://cloud.gravitee.io/). From the **Dashboard**, open the **Gateways** section. Your new hybrid Gateway appears here.

  
### Validate the pods

A healthy Gateway pod displays the `Running` status with `1/1` ready containers.

1. Query the pod status using the following command:

   ```bash
   kubectl get pods --namespace=gravitee-gamma -l app.kubernetes.io/instance=graviteeio-gamma-gateway
   ```
2. Verify that the Gateway pod is ready and running with no restarts:

   ```sh
   NAME                                              READY   STATUS    RESTARTS   AGE
   graviteeio-gamma-gateway-gateway-b6fd75949-rjsr4  1/1     Running   0          2m15s
   ```

### Validate the Gateway URL

1. Get the ALB address from the ingress:

   ```bash
   kubectl get ingress -n gravitee-gamma
   ```
2. Make a GET request to the Gateway using your hostname or the ALB address:

   ```bash
   curl -H "Host: gateway.example.com" http://<load-balancer-address>/

   # If DNS resolves your hostname to the ALB, you can use:
   curl http://gateway.example.com/
   ```
3. Confirm that the Gateway replies with the following message, which informs you that no API is deployed yet for this URL:

   ```sh
   No context-path matches the request URI.
   ```

{% hint style="success" %}
You can now create and deploy APIs to your hybrid Gateway from the Gamma control plane.
{% endhint %}

## Proxy configuration

To route Gateway traffic through a corporate proxy (for example, for backend API calls or JWKS retrieval from external identity providers like Microsoft Entra ID), add the following `gravitee_system_proxy_*` environment variables to the `gateway.env` section of your `values.yaml`:

```yaml
gateway:
  env:
    - name: gravitee_system_proxy_enabled
      value: "true"
    - name: gravitee_system_proxy_type
      value: "HTTP"
    - name: gravitee_system_proxy_host
      value: "<proxy-host>"
    - name: gravitee_system_proxy_port
      value: "<proxy-port>"
    - name: gravitee_system_proxy_https_host
      value: "<proxy-host>"
    - name: gravitee_system_proxy_https_port
      value: "<proxy-port>"
```

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../../agent-management/get-started/create-your-first-mcp-server.md).
* Create your first API. For more information, see [Create your first API](../../../../api-management/get-started/create-your-first-api.md).
