---
hidden: false
noIndex: true
---
# Install Gamma on AWS EKS
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

This guide explains how to deploy a self-hosted Gravitee Gamma platform on Amazon Elastic Kubernetes Service (EKS) with Helm, fronted by a single AWS Application Load Balancer (ALB).

You deploy the standard `graviteeio/apim` Helm chart, turn on Gamma with `gamma.enabled`, and add the Gamma console (`gammaUi`). This guide uses the `4.12.0` images, which include the Agent Management module.

Every component is served on **one hostname** through one ALB: the Gamma console at `/`, and the Management API at `/management`, `/portal`, and `/gamma`. Keeping everything on a single host makes the browser requests same-origin, so the login session cookie is sent and the consoles log in. The whole platform, including the ALB ingress, is defined in a single `values.yaml`.

## Prerequisites

Before you install Gamma, complete the following steps:

* Install the [AWS CLI](https://aws.amazon.com/cli/), [eksctl](https://eksctl.io/), [helm](https://helm.sh/docs/intro/install/), and [kubectl](https://kubernetes.io/docs/tasks/tools/).
* Have a running EKS cluster, and point `kubectl` at it:

  ```bash
  aws eks update-kubeconfig --name <cluster-name> --region <region>
  ```
* A hostname you control (for example, `gamma.example.com`) and, for HTTPS, an [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/) certificate for it.
* **(Enterprise Edition only)** To enable Agent Management, you need an enterprise license that includes the `agent-management` pack. To get one, contact your Technical Account Manager. For more information, see [Add your license key](#enterprise-edition-only-add-your-license-key).
* For Gravitee Enterprise Edition deployments, ensure that you have your license key. For more information about license keys, see [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

## Configure the load balancer controller

The ALB controller turns the ingress into an ALB. How you get it depends on your cluster type.

{% hint style="info" %}
Check your cluster type with `kubectl get ingressclass`. If it returns nothing and your cluster is **EKS Auto Mode**, follow [EKS Auto Mode](#eks-auto-mode). Otherwise follow [Standard EKS](#standard-eks).
{% endhint %}

### EKS Auto Mode

On EKS Auto Mode, AWS manages the EBS CSI driver and the load balancer controller. You don't install them. You only create an `IngressClass` that points at the managed ALB controller.

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

1. Download the IAM policy the controller requires using the following command:

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

  \
  The output shows two controller pods in `Running` status:

  ```bash
  NAME                                            READY   STATUS    RESTARTS   AGE
  aws-load-balancer-controller-xxxxxxxxx-xxxxx    1/1     Running   0          33s
  aws-load-balancer-controller-xxxxxxxxx-xxxxx    1/1     Running   0          33s
  ```

#### Optional: persistent storage

{% hint style="info" %}
**You don't need this section for the quick-start.** This guide installs MongoDB and Elasticsearch with `persistence.enabled=false`, so they use ephemeral pod storage and create no persistent volumes. The platform comes up and you can sign in without any storage setup.
{% endhint %}

Set up persistent storage only when you want MongoDB and Elasticsearch **data to survive pod restarts and rescheduling**, for example a longer-lived demo, a shared environment, or anything closer to production. With the ephemeral default, restarting a datastore pod loses its data. To enable it, switch the datastore installs to `persistence.enabled=true`, then give the cluster a way to provision volumes by installing the EBS CSI driver and a default storage class.

1. Install the EBS CSI driver using the following command:

   ```bash
   kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.35"
   ```
2. Create an IAM service account for the driver. Replace `<cluster-name>` and `<region>`:

   ```bash
   eksctl create iamserviceaccount \
     --name ebs-csi-controller-sa --namespace kube-system \
     --cluster <cluster-name> --region <region> \
     --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
     --approve --override-existing-serviceaccounts
   ```
3. Restart the EBS CSI controller to pick up the permissions using the following command:

   ```bash
   kubectl rollout restart deployment ebs-csi-controller -n kube-system
   ```
4. Create a file named `storageclass.yaml` with the following content:

   ```yaml
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: gp3
     annotations:
       storageclass.kubernetes.io/is-default-class: "true"
   provisioner: ebs.csi.aws.com
   parameters:
     type: gp3
     fsType: ext4
   volumeBindingMode: Immediate
   allowVolumeExpansion: true
   ```
5. Apply the storage class using the following command:

   ```bash
   kubectl apply -f storageclass.yaml
   ```

   \
   With a default storage class in place, set `persistence.enabled=true` on the MongoDB and Elasticsearch installs in [Deploy MongoDB and Elasticsearch](#deploy-mongodb-and-elasticsearch) so they request persistent volumes.

## Install Gamma

To install Gamma, complete the following steps:

1. [#create-the-namespace](#create-the-namespace "mention")
2. [#deploy-mongodb-and-elasticsearch](#deploy-mongodb-and-elasticsearch "mention")
3. [#enterprise-edition-only-add-your-license-key](#enterprise-edition-only-add-your-license-key "mention")
4. [#prepare-the-values-yaml-for-helm](#prepare-the-values-yaml-for-helm "mention")
5. [#install-with-helm](#install-with-helm "mention")

### Create the namespace

```bash
kubectl create namespace gravitee-gamma
```

### Deploy MongoDB and Elasticsearch

1. Install MongoDB:

   ```bash
   helm install gravitee-mongodb oci://registry-1.docker.io/cloudpirates/mongodb \
     --namespace gravitee-gamma --set auth.enabled=false --set persistence.enabled=false \
     --set resources.requests.memory=512Mi --set resources.requests.cpu=250m
   ```
2. Install Elasticsearch:

   ```bash
   helm repo add elastic https://helm.elastic.co
   helm repo update
   helm install elasticsearch elastic/elasticsearch \
     --namespace gravitee-gamma --set persistence.enabled=false --set replicas=1 --set minimumMasterNodes=1
   ```
3. Retrieve the `elastic` user password:

   ```bash
   kubectl get secrets --namespace gravitee-gamma elasticsearch-master-credentials -o jsonpath='{.data.password}' | base64 -d
   ```

### (Enterprise Edition only) Add your license key

Agent Management is an enterprise feature. It only activates with an enterprise license that includes the `agent-management` pack. To get one, contact your Technical Account Manager. Your account manager sends you the license as a `license.key` file. The other modules work without a license.

{% hint style="info" %}
If your license is a base64-encoded text file (for example, `license.base64.txt`), decode it into `license.key` first:

```bash
base64 -d < license.base64.txt > license.key
```

On macOS, use `base64 -D` (capital `D`) if `base64 -d` returns an error.
{% endhint %}

1. Save the `license.key` file your account manager sent you.
2. Create the secret:

   ```bash
   kubectl create secret generic gravitee-license --from-file=license.key=./license.key --namespace gravitee-gamma
   ```
3. Uncomment the license lines under the `api` service in `values.yaml` (in the next step).

### Prepare the `values.yaml` for Helm

The Gamma components run as `ClusterIP` services, and the single ALB ingress is defined in the chart's `extraObjects`, so the whole platform ships from one `values.yaml`.

1. Create a `values.yaml` file. Replace `gamma.example.com` with your hostname, the ACM certificate ARN with yours, and the Elasticsearch password:

   ```yaml
   # MongoDB Configuration
   mongo:
     uri: mongodb://gravitee-mongodb.gravitee-gamma.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000

   # Elasticsearch Configuration
   es:
     enabled: true
     endpoints:
       - https://elasticsearch-master:9200
     security:
       enabled: true
       username: elastic
       password: [ELASTIC PASSWORD FROM ES INSTALLATION]
     ssl:
       verifyHostname: false
       trustAll: true

   management:
     type: mongodb
   ratelimit:
     type: mongodb
   analytics:
     type: elasticsearch

   elasticsearch:
     enabled: false
   mongodb:
     enabled: false

   # Single host for all components
   installation:
     type: standalone
     api:
       url: https://gamma.example.com/management
     standalone:
       gamma-console:
         urls:
           - orgId: DEFAULT
             url: https://gamma.example.com/

   gamma:
     enabled: true

   api:
     enabled: true
     image:
       repository: graviteeio/apim-management-api
       tag: 4.12.0
       pullPolicy: IfNotPresent
     env:
       - name: gravitee_installation_api_url
         value: "https://gamma.example.com/management"
       # CORS - single origin, credentials allowed
       - name: gravitee_http_cors_enabled
         value: "true"
       - name: gravitee_http_cors_allow-origin
         value: "https://gamma.example.com"
       - name: gravitee_http_cors_allow-credentials
         value: "true"
       # Cookie - same-origin over HTTPS
       - name: gravitee_http_cookie_sameSite
         value: "Lax"
       - name: gravitee_http_cookie_secure
         value: "true"
     # ALB health check for the API target group: the Management API doesn't
     # return 200 on /, so health-check it on a path that does.
     service:
       annotations:
         alb.ingress.kubernetes.io/healthcheck-path: /management/v2/ui/bootstrap
         alb.ingress.kubernetes.io/success-codes: "200"
     ingress:
       management:
         enabled: false
       portal:
         enabled: false
       gamma:
         enabled: false
     resources:
       requests:
         memory: "1Gi"
         cpu: "500m"
       limits:
         memory: "2Gi"
         cpu: "1"
     # (Enterprise Edition) Mount the license secret for Agent Management.
     # Create the gravitee-license secret (see "Add your license key"), then uncomment:
     # extraVolumes: |
     #   - name: gravitee-license
     #     secret:
     #       secretName: gravitee-license
     # extraVolumeMounts: |
     #   - name: gravitee-license
     #     mountPath: "/opt/graviteeio-management-api/license/license.key"
     #     subPath: license.key
     #     readOnly: true

   gateway:
     enabled: true
     image:
       repository: graviteeio/apim-gateway
       tag: 4.12.0
       pullPolicy: IfNotPresent
     ingress:
       enabled: false

   ui:
     enabled: true
     image:
       repository: graviteeio/apim-management-ui
       tag: 4.12.0
       pullPolicy: IfNotPresent
     ingress:
       enabled: false

   portal:
     enabled: true
     defaultPortal: "classic"
     image:
       repository: graviteeio/apim-portal-ui
       tag: 4.12.0
       pullPolicy: IfNotPresent
     env:
       - name: PORTAL_BASE_HREF
         value: /dev/
     ingress:
       enabled: false

   gammaUi:
     enabled: true
     image:
       repository: graviteeio/gamma-ui
       tag: 4.12.0
       pullPolicy: IfNotPresent
     app:
       gammaBaseURL: "https://gamma.example.com/gamma"
     env:
       - name: GAMMA_CONSOLE_BASE_HREF
         value: /
     ingress:
       enabled: false

   ingress:
     enabled: false

   # One ALB ingress for all paths on the single host, shipped with the release.
   # The longer, specific API paths are matched ahead of the / catch-all (the console).
   extraObjects:
     - apiVersion: networking.k8s.io/v1
       kind: Ingress
       metadata:
         name: gamma
         namespace: gravitee-gamma
         annotations:
           alb.ingress.kubernetes.io/scheme: internet-facing
           alb.ingress.kubernetes.io/target-type: ip
           alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}, {"HTTP": 80}]'
           alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/certificate-id
           alb.ingress.kubernetes.io/ssl-redirect: '443'
       spec:
         ingressClassName: alb
         rules:
           - host: gamma.example.com
             http:
               paths:
                 - path: /gamma
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-api
                       port:
                         number: 83
                 - path: /management
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-api
                       port:
                         number: 83
                 - path: /portal
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-api
                       port:
                         number: 83
                 - path: /console
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-ui
                       port:
                         number: 8002
                 - path: /dev
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-portal
                       port:
                         number: 8003
                 - path: /
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-gamma
                       port:
                         number: 8005
   ```
2. Replace `[ELASTIC PASSWORD FROM ES INSTALLATION]` with the password you retrieved.

{% hint style="warning" %}
**Gamma uses two Helm flags**

* `gamma.enabled` is the global master switch (default `false`). It turns Gamma on in the Management API and unlocks the Gamma ingress and the Gamma console deployment.
* `gammaUi.enabled` is the per-component switch for the Gamma console (default `false`). It deploys the `graviteeio/gamma-ui` console.

When `gamma.enabled` is `true`, you choose which components to deploy:

* `gamma.enabled: true` with `gammaUi.enabled: true` enables Gamma on the API and deploys the Gamma console.
* `gamma.enabled: true` with `gammaUi.enabled: false` enables Gamma on the API without the console.

If `gamma.enabled` is `false`, Gamma stays off everywhere, and the Gamma console doesn't deploy even when `gammaUi.enabled` is `true`.
{% endhint %}

### Install with Helm

1. Add the Gravitee Helm repository:

   ```bash
   helm repo add graviteeio https://helm.gravitee.io
   helm repo update
   ```
2. Install the chart with the release name `gamma`. This creates the components and the ALB ingress together:

   ```bash
   helm install gamma graviteeio/apim \
     --version 4.12.0 --devel \
     --namespace gravitee-gamma \
     -f values.yaml \
     --wait --timeout 10m
   ```
3. Get the ALB hostname and point your DNS record (`gamma.example.com`) at it:

   ```bash
   kubectl get ingress gamma -n gravitee-gamma
   ```

{% hint style="info" %}
The Management API doesn't return `200` on `/`, so its ALB target group is health-checked on `/management/v2/ui/bootstrap` (the `api.service.annotations` in `values.yaml`). Without that, `/management` and `/gamma` return `503` while the console still serves.
{% endhint %}

## Access the consoles

After DNS resolves to the ALB, open the consoles. The default username and password for the Gamma console, the APIM Console, and the Developer Portal are both `admin`.

| Component | URL | Default credentials |
| --- | --- | --- |
| Gamma console | `https://gamma.example.com/` | `admin` / `admin` |
| APIM Console | `https://gamma.example.com/console` | `admin` / `admin` |
| Developer Portal | `https://gamma.example.com/dev/` | `admin` / `admin` |

## Verification

* Confirm the pods are running and the ALB serves the platform:

  ```bash
  kubectl get pods -n gravitee-gamma
  curl -s -o /dev/null -w "%{http_code}\n" https://gamma.example.com/management/v2/ui/bootstrap
  ```

  \
  The bootstrap call returns `200` once the platform is up.

## Why one hostname

The Gamma console (`/`) and the API (`/gamma`, `/management`) are on the same host, so the browser requests are same-origin and the login session cookie is sent with each call. If you instead put the console and the API on separate subdomains, the cookie becomes cross-site and you'd need `SameSite=None; Secure` cookies and per-origin CORS. Keeping everything on one host behind one ALB is simpler and is the layout verified on EKS.

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../agent-management/get-started/create-your-first-mcp-server.md).
