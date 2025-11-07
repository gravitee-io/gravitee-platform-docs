# AWS EKS

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview&#x20;

This guide explains how to deploy a complete self-hosted Gravitee APIM platform on Amazon Elastic Kubernetes Service (EKS) using Helm charts.

## Prerequisites

Before you install the Gravitee APIM, complete the following steps:

* Install [AWS CLI](https://aws.amazon.com/cli/) and configure it with your credentials
* Install [eksctl](https://eksctl.io/) for EKS cluster management
* Install [helm](https://helm.sh/docs/intro/install/)&#x20;
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/)
* Have a [valid AWS account](https://signin.aws.amazon.com/signup?request_type=register)
* (Optional) License key for Enterprise features
* (Optional) Register a domain name in Route53 or have access to DNS management

## Components Overview&#x20;

This self-hosted APIM deployment includes several components that work together to provide a complete API management platform:

* Management API: Handles API configuration, policies, and administrative operations
* Gateway: Processes API requests, applies policies, and routes traffic to backend services
* Management Console UI: Web interface for API administrators to configure and monitor APIs
* Developer Portal UI: Self-service portal for developers to discover and consume APIs

## Configure AWS Infrastructure Components

To prepare your EKS cluster for Gravitee APIM deployment, configure the following AWS infrastructure components:

1. [#install-ebs-csi-driver](aws-eks.md#install-ebs-csi-driver "mention")
2. [#create-default-storage-class](aws-eks.md#create-default-storage-class "mention")
3. [#install-aws-load-balancer-controller](aws-eks.md#install-aws-load-balancer-controller "mention")

### Install EBS CSI Driver&#x20;

{% hint style="info" %}
The EBS CSI driver is required for persistent volumes.&#x20;
{% endhint %}

1.  Install the EBS driver with the following  `kubectl` command:

    ```bash
    kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.35"
    ```
2. Create an IAM service account for the EBS CSI driver using the following command:

```bash
eksctl create iamserviceaccount \
  --name ebs-csi-controller-sa \
  --namespace kube-system \
  --cluster <cluster-name> \
  --region <region> \
  --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --approve \
  --override-existing-serviceaccounts

```

3.  Restart the EBS CSI controller to apply permissions using the following command:

    ```sh
    kubectl rollout restart deployment ebs-csi-controller -n kube-system
    ```

#### Verification&#x20;

To verify that your EBS CSI driver installation succeeded, check pod status using the following command:

```bash
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-ebs-csi-driver
```

The output should show the EBS CSI controller pods in Running status with 2/2 or more ready:

```bash
NAME                                  READY   STATUS    RESTARTS   AGE
ebs-csi-controller-<replicaset-id>-<pod-id>   6/6     Running   0          2m
ebs-csi-controller-<replicaset-id>-<pod-id>   6/6     Running   0          2m
ebs-csi-node-<node-id>                        3/3     Running   0          2m
ebs-csi-node-<node-id>                        3/3     Running   0          2m
```

### Create Default Storage Class

{% hint style="warning" %}
Without a default storage class, Kubernetes cannot dynamically provision persistent volumes.
{% endhint %}

1.  Create a file named `storageclass.yaml` with the following configuration:

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
2.  Apply the storage class using the following command:

    ```bash
    kubectl apply -f storageclass.yaml
    ```

#### Verification&#x20;

To verify that your storage class was created successfully, use the following command:

```bash
kubectl get storageclass
```

The output should show the `gp3` storage class as the default, indicated by `(default)` next to the name:

```bash
NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
gp3 (default)   ebs.csi.aws.com        Delete          Immediate           true                   30s
```

### Install AWS Load Balancer Controller

1.  Create a file named `iam_policy.json` and then copy and paste the following JSON content into the file:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "iam:CreateServiceLinkedRole"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "iam:AWSServiceName": "elasticloadbalancing.amazonaws.com"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:DescribeAccountAttributes",
                    "ec2:DescribeAddresses",
                    "ec2:DescribeAvailabilityZones",
                    "ec2:DescribeInternetGateways",
                    "ec2:DescribeVpcs",
                    "ec2:DescribeVpcPeeringConnections",
                    "ec2:DescribeSubnets",
                    "ec2:DescribeSecurityGroups",
                    "ec2:DescribeInstances",
                    "ec2:DescribeNetworkInterfaces",
                    "ec2:DescribeTags",
                    "ec2:GetCoipPoolUsage",
                    "ec2:DescribeCoipPools",
                    "elasticloadbalancing:DescribeLoadBalancers",
                    "elasticloadbalancing:DescribeLoadBalancerAttributes",
                    "elasticloadbalancing:DescribeListeners",
                    "elasticloadbalancing:DescribeListenerAttributes",
                    "elasticloadbalancing:DescribeListenerCertificates",
                    "elasticloadbalancing:DescribeSSLPolicies",
                    "elasticloadbalancing:DescribeRules",
                    "elasticloadbalancing:DescribeTargetGroups",
                    "elasticloadbalancing:DescribeTargetGroupAttributes",
                    "elasticloadbalancing:DescribeTargetHealth",
                    "elasticloadbalancing:DescribeTags",
                    "elasticloadbalancing:DescribeTrustStores"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "cognito-idp:DescribeUserPoolClient",
                    "acm:ListCertificates",
                    "acm:DescribeCertificate",
                    "iam:ListServerCertificates",
                    "iam:GetServerCertificate",
                    "waf-regional:GetWebACL",
                    "waf-regional:GetWebACLForResource",
                    "waf-regional:AssociateWebACL",
                    "waf-regional:DisassociateWebACL",
                    "wafv2:GetWebACL",
                    "wafv2:GetWebACLForResource",
                    "wafv2:AssociateWebACL",
                    "wafv2:DisassociateWebACL",
                    "shield:GetSubscriptionState",
                    "shield:DescribeProtection",
                    "shield:CreateProtection",
                    "shield:DeleteProtection"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:AuthorizeSecurityGroupIngress",
                    "ec2:RevokeSecurityGroupIngress",
                    "ec2:CreateSecurityGroup"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:CreateTags"
                ],
                "Resource": "arn:aws:ec2:*:*:security-group/*",
                "Condition": {
                    "StringEquals": {
                        "ec2:CreateAction": "CreateSecurityGroup"
                    },
                    "Null": {
                        "aws:RequestTag/elbv2.k8s.aws/cluster": "false"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:CreateTags",
                    "ec2:DeleteTags"
                ],
                "Resource": "arn:aws:ec2:*:*:security-group/*",
                "Condition": {
                    "Null": {
                        "aws:RequestTag/elbv2.k8s.aws/cluster": "true",
                        "aws:ResourceTag/elbv2.k8s.aws/cluster": "false"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:AuthorizeSecurityGroupIngress",
                    "ec2:RevokeSecurityGroupIngress",
                    "ec2:DeleteSecurityGroup"
                ],
                "Resource": "*",
                "Condition": {
                    "Null": {
                        "aws:ResourceTag/elbv2.k8s.aws/cluster": "false"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": [
                    "elasticloadbalancing:CreateLoadBalancer",
                    "elasticloadbalancing:CreateTargetGroup"
                ],
                "Resource": "*",
                "Condition": {
                    "Null": {
                        "aws:RequestTag/elbv2.k8s.aws/cluster": "false"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": [
                    "elasticloadbalancing:CreateListener",
                    "elasticloadbalancing:DeleteListener",
                    "elasticloadbalancing:CreateRule",
                    "elasticloadbalancing:DeleteRule",
                    "elasticloadbalancing:ModifyListener",
                    "elasticloadbalancing:AddListenerCertificates",
                    "elasticloadbalancing:RemoveListenerCertificates",
                    "elasticloadbalancing:ModifyRule"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "elasticloadbalancing:AddTags",
                    "elasticloadbalancing:RemoveTags"
                ],
                "Resource": [
                    "arn:aws:elasticloadbalancing:*:*:targetgroup/*/*",
                    "arn:aws:elasticloadbalancing:*:*:loadbalancer/net/*/*",
                    "arn:aws:elasticloadbalancing:*:*:loadbalancer/app/*/*",
                    "arn:aws:elasticloadbalancing:*:*:listener/net/*/*/*",
                    "arn:aws:elasticloadbalancing:*:*:listener/app/*/*/*",
                    "arn:aws:elasticloadbalancing:*:*:listener-rule/net/*/*/*",
                    "arn:aws:elasticloadbalancing:*:*:listener-rule/app/*/*/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "elasticloadbalancing:ModifyLoadBalancerAttributes",
                    "elasticloadbalancing:SetIpAddressType",
                    "elasticloadbalancing:SetSecurityGroups",
                    "elasticloadbalancing:SetSubnets",
                    "elasticloadbalancing:DeleteLoadBalancer",
                    "elasticloadbalancing:ModifyTargetGroup",
                    "elasticloadbalancing:ModifyTargetGroupAttributes",
                    "elasticloadbalancing:DeleteTargetGroup",
                    "elasticloadbalancing:RegisterTargets",
                    "elasticloadbalancing:DeregisterTargets",
                    "elasticloadbalancing:SetWebAcl"
                ],
                "Resource": "*"
            }
        ]
    }

    ```
2.  Apply the IAM Policy to AWS using the following command:

    ```bash
    # Replace <region> with your AWS region (e.g., "eu-west-2", "us-east-1")
    # Note: If you get "AccessDenied" error, ask your AWS admin to run this command

    aws iam create-policy \
        --policy-name AWSLoadBalancerControllerIAMPolicy \
        --policy-document file://iam_policy.json \
        --region <region>
    ```
3.  Create IAM Service Account using the following command:&#x20;

    ```bash
    # Replace these values:
    # <cluster-name>: Your EKS cluster name (same as created above)
    # <region>: Your AWS region (same as above)

    eksctl create iamserviceaccount \
      --cluster=<cluster-name> \
      --namespace=kube-system \
      --name=aws-load-balancer-controller \
      --role-name AmazonEKSLoadBalancerControllerRole \
      --attach-policy-arn=arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):policy/AWSLoadBalancerControllerIAMPolicy \
      --region=<region> \
      --approve \
      --override-existing-serviceaccounts
    ```
4.  Install the Controller using the following Helm command:

    ```bash
    # Add the EKS Helm repository
    helm repo add eks https://aws.github.io/eks-charts

    helm repo update

    # Install the controller
    # Replace these values:
    # <cluster-name>: Your EKS cluster name
    # <region>: Your AWS region

    helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
      -n kube-system \
      --set clusterName=<cluster-name> \
      --set serviceAccount.create=false \
      --set serviceAccount.name=aws-load-balancer-controller \
      --set region=<region>
    ```

#### Verification&#x20;

Verify the installation using the following command:

```bash
# Check if pods are running

kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
```

The output shows two pods in `Running` status with `1/1` ready.

```bash
NAME                                                    READY   STATUS    RESTARTS   AGE
aws-load-balancer-controller-<replicaset-id>-<pod-id>  1/1     Running   0          33s
aws-load-balancer-controller-<replicaset-id>-<pod-id>  1/1     Running   0          33s
```

## Install the Gravitee APIM

To install the Gravitee APIM, complete the following steps:

1. [#create-namespace](aws-eks.md#create-namespace "mention")
2. [#install-mongodb](aws-eks.md#install-mongodb "mention")
3. [#install-elasticsearch](aws-eks.md#install-elasticsearch "mention")
4. [#optional-install-redis](aws-eks.md#optional-install-redis "mention")
5. [#optional-install-postgresql](aws-eks.md#optional-install-postgresql "mention")
6. [#enterprise-edition-only-create-secret](aws-eks.md#enterprise-edition-only-create-secret "mention")
7. [#prepare-the-values.yaml-for-helm](aws-eks.md#prepare-the-values.yaml-for-helm "mention")
8. [#install-using-helm](aws-eks.md#install-using-helm "mention")

### Create Namespace&#x20;

Kubernetes namespaces provide logical isolation and organization within a cluster. Creating a dedicated namespace for Gravitee APIM:

* Isolates resources: Separates APIM components from other applications
* Simplifies management: Groups related services, pods, and configurations together

Create the namespace using the following command:&#x20;

```bash
kubectl create namespace gravitee-apim
```

{% hint style="danger" %}
This guide requires MongoDB and Elasticsearch to be installed for the complete APIM platform to function.
{% endhint %}

### Install MongoDB

To support API definitions and configuration, you must install MongoDB into your Kubernetes cluster. For more information about installing MongoDB, see the [official chart documentation](https://artifacthub.io/packages/helm/bitnami/mongodb)

1.  Install MongoDB with Helm using the following command:&#x20;

    ```bash
    helm install gravitee-mongodb oci://registry-1.docker.io/cloudpirates/mongodb \
      -n gravitee-apim \
      --set auth.enabled=false \
      --set persistence.enabled=false \
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```

#### Verification

1.  To verify that your MongoDB deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-mongodb
    ```

    \
    The command generates the following output:&#x20;

    ```bash
    NAME                  READY   STATUS    RESTARTS   AGE
    gravitee-mongodb-0    1/1     Running   0          2m
    ```



### Install Elasticsearch&#x20;

To support analytics and logging, you must install Elasticsearch into your Kubernetes cluster. For more information on installing Elasticsearch, see the [official chart documentation.](https://artifacthub.io/packages/helm/bitnami/elasticsearch)&#x20;

1.  Install Elasticsearch with Helm using the following command:

    ```bash
    helm repo add elastic https://helm.elastic.co

    helm repo update

    helm -n gravitee-apim install elasticsearch elastic/elasticsearch \
      --set persistence.enabled=false \
      --set replicas=1 \
      --set minimumMasterNodes=1
    ```
2.  Follow the instructions that appear in your terminal, and retrieve the Elastic user's password.

    ```bash
    NAME: elasticsearch                                                                                                                                                                                                                                            
    LAST DEPLOYED: Fri Oct 24 12:13:02 2025                                                                                                                                                                                                                        
    NAMESPACE: gravitee-apim                                                                                                                                                                                                                                             
    STATUS: deployed                                                                                                                                                                                                                                               
    REVISION: 1                                                                                                                                                                                                                                                    
    NOTES:                                                                                                                                                                                                                                                         
    1. Watch all cluster members come up.                                                                                                                                                                                                                          
      $ kubectl get pods --namespace=gravitee-apim -l app=elasticsearch-master -w                                                                                                                                                                                        
    2. Retrieve elastic user's password.                                                                                                                                                                                                                           
      $ kubectl get secrets --namespace=gravitee-apim elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d                                                                                                                                         
    3. Test cluster health using Helm test.
      $ helm --namespace=gravitee-apim test elasticsearch
    ```

#### Verification

1.  To verify that your Elasticsearch deployment succeeded, check pod status using the following command:\


    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-elasticsearch
    ```

    \
    The command generates the following output:\


    ```bash
    NAME                     READY   STATUS    RESTARTS   AGE
    elasticsearch-master-0   1/1     Running   0          55m
    ```

    \


### (Optional) Install Redis

To support caching and rate-limiting, you must install Redis into your Kubernetes cluster. For more information about installing Redis, see the [official chart documentation. ](https://artifacthub.io/packages/helm/bitnami/redis)

1.  Install Redis with Helm using the following command: &#x20;

    ```bash
    helm install gravitee-redis oci://registry-1.docker.io/cloudpirates/redis \
      -n gravitee-apim \
      --set auth.enabled=true \
      --set auth.password=redis-password
    ```

#### Verification

1.  To verify that your Redis deployment succeeded, check pod status using the following command:\


    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-redis
    ```

    \
    The command generates the following output:&#x20;

    ```bash
    NAME                      READY   STATUS    RESTARTS   AGE
    gravitee-redis-master-0   1/1     Running   0          2m
    ```

### (Optional) Install PostgreSQL&#x20;

To support management data, you can install PostgreSQL into your Kubernetes cluster. For more information on installing PostgreSQL, see the [official chart documentation.](https://artifacthub.io/packages/helm/bitnami/postgresql)&#x20;

1.  Install PostgreSQL with Helm using the following command:\


    ```bash
    helm install gravitee-postgresql oci://registry-1.docker.io/cloudpirates/postgres \
      -n gravitee-apim \
      --set auth.database=gravitee \
      --set auth.username=gravitee \
      --set auth.password=changeme \
      --set persistence.enabled=true \
      --set persistence.size=8Gi \
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```

#### Verification&#x20;

1.  To verify that your PostgreSQL deployment succeeded, retrieve the password using the following command:

    ```bash
    kubectl -n gravitee-apim get secret gravitee-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d
    ```


2.  Check pod status using the following command:

    ```bash
    kubectl -n gravitee-apim get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-postgresql
    ```

    \
    The command generates the following output:&#x20;

    ```bash
    NAME                    READY   STATUS    RESTARTS   AGE
    gravitee-postgresql-0   1/1     Running   0          2m
    ```



### (Enterprise Edition Only) Create Secret&#x20;

Before installing Gravitee APIM for [enterprise edition](https://documentation.gravitee.io/apim/readme/enterprise-edition), you need to create a Kubernetes secret for your license key.

1.  Create the secret using the following command:

    ```bash
    kubectl create secret generic gravitee-license \
      --from-file=license.key=./license.key \
      --namespace gravitee-apim
    ```

{% hint style="info" %}
* Ensure your license key file is named `license.key` and located in your current directory.
* The secret will be named `gravitee-license` and referenced in your Helm configuration.
* If you don't have a license key, you can still proceed with community features.
{% endhint %}

### Prepare the `values.yaml` for Helm&#x20;

1.  Create a `values.yaml` file in your working directory and copy the following Gravitee configuration into it. This is the base configuration for your self-hosted APIM platform:\


    ```yaml
    # MongoDB Configuration
    mongo:
      uri: mongodb://gravitee-mongodb.gravitee-apim.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000

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

    # Repository types
    management:
      type: mongodb

    ratelimit:
      type: mongodb

    analytics:
      type: elasticsearch

    # Management API Configuration
    api:
      enabled: true
      replicaCount: 1
      image:
        repository: graviteeio/apim-management-api
        tag: latest
        pullPolicy: Always

      env:
        # CORS Configuration
        - name: gravitee_http_cors_enabled
          value: "true"
        - name: gravitee_http_cors_allow-origin
          value: "*"
        - name: gravitee_http_cors_allow-headers
          value: "Authorization,Content-Type,X-Requested-With,Accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,Cookie"
        - name: gravitee_http_cors_allow-methods
          value: "GET,POST,PUT,DELETE,OPTIONS,PATCH"
        - name: gravitee_http_cors_exposed-headers
          value: "X-Total-Count,Set-Cookie"
        - name: gravitee_http_cors_allow-credentials
          value: "true"

        # Cookie Configuration for HTTPS
        - name: gravitee_http_cookie_sameSite
          value: "None"
        - name: gravitee_http_cookie_secure
          value: "true"

        # Security exclusions for public endpoints
        - name: gravitee_management_security_providers_0_type
          value: "memory"
        - name: gravitee_management_security_exclude_0
          value: "/auth/**"
        - name: gravitee_management_security_exclude_1
          value: "/organizations/*/environments/*/configuration"
        - name: gravitee_management_security_exclude_2
          value: "/_health"
        - name: gravitee_management_security_exclude_3
          value: "/info"
        - name: gravitee_management_security_exclude_4
          value: "/portal/**"

        # Make portal public by default
        - name: gravitee_portal_authentication_forceLogin_enabled
          value: "false"

      service:
        type: ClusterIP
        externalPort: 83
        internalPort: 8083

      ingress:
        management:
          enabled: true
          ingressClassName: alb
          scheme: https
          pathType: Prefix
          path: /management
          hosts:
            - api.yourdomain.com
          annotations:
            alb.ingress.kubernetes.io/scheme: internet-facing
            alb.ingress.kubernetes.io/target-type: ip
            alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}, {"HTTP": 80}]'
            alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/certificate-id
            alb.ingress.kubernetes.io/ssl-redirect: '443'
            alb.ingress.kubernetes.io/healthcheck-path: /management/_health
            alb.ingress.kubernetes.io/healthcheck-interval-seconds: '30'
            alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
            alb.ingress.kubernetes.io/healthy-threshold-count: '2'
            alb.ingress.kubernetes.io/unhealthy-threshold-count: '3'
            alb.ingress.kubernetes.io/enable-cors: "true"
            alb.ingress.kubernetes.io/cors-allow-origin: "*"
            alb.ingress.kubernetes.io/cors-allow-methods: "GET,POST,PUT,DELETE,OPTIONS,PATCH"
            alb.ingress.kubernetes.io/cors-allow-headers: "Authorization,Content-Type,X-Requested-With,Accept,Origin,Cookie"
            alb.ingress.kubernetes.io/cors-expose-headers: "Content-Length,Content-Range,Set-Cookie"
            alb.ingress.kubernetes.io/cors-allow-credentials: "true"

        portal:
          enabled: true
          ingressClassName: alb
          scheme: https
          pathType: Prefix
          path: /portal
          hosts:
            - api.yourdomain.com
          annotations:
            alb.ingress.kubernetes.io/scheme: internet-facing
            alb.ingress.kubernetes.io/target-type: ip
            alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}, {"HTTP": 80}]'
            alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/certificate-id
            alb.ingress.kubernetes.io/ssl-redirect: '443'
            alb.ingress.kubernetes.io/healthcheck-path: /portal/_health
            alb.ingress.kubernetes.io/enable-cors: "true"
            alb.ingress.kubernetes.io/cors-allow-origin: "https://portal.yourdomain.com"
            alb.ingress.kubernetes.io/cors-allow-methods: "GET,POST,PUT,DELETE,OPTIONS,PATCH"
            alb.ingress.kubernetes.io/cors-allow-headers: "DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,Accept,Origin,Cookie"
            alb.ingress.kubernetes.io/cors-expose-headers: "Content-Length,Content-Range,Set-Cookie"
            alb.ingress.kubernetes.io/cors-allow-credentials: "true"

      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1"

      autoscaling:
        enabled: true
        minReplicas: 2
        maxReplicas: 5
        targetAverageUtilization: 70
        targetMemoryAverageUtilization: 80

      # License volume configuration for Management API (uncomment for enterprise edition using license key)
      # extraVolumes: |
      #   - name: gravitee-license
      #     secret:
      #       secretName: gravitee-license
      # extraVolumeMounts: |
      #   - name: gravitee-license
      #     mountPath: "/opt/graviteeio-management-api/license/license.key"
      #     subPath: license.key
      #     readOnly: true

    # Gateway Configuration
    gateway:
      enabled: true
      replicaCount: 1
      image:
        repository: graviteeio/apim-gateway
        tag: latest
        pullPolicy: Always

      service:
        type: ClusterIP
        externalPort: 82
        internalPort: 8082

      ingress:
        enabled: true
        ingressClassName: alb
        pathType: Prefix
        path: /
        hosts:
          - gateway.yourdomain.com
        annotations:
          alb.ingress.kubernetes.io/scheme: internet-facing
          alb.ingress.kubernetes.io/target-type: ip
          alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}, {"HTTP": 80}]'
          alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/certificate-id
          alb.ingress.kubernetes.io/ssl-redirect: '443'
          alb.ingress.kubernetes.io/healthcheck-path: /_health
          alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
          alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
          alb.ingress.kubernetes.io/healthy-threshold-count: '2'
          alb.ingress.kubernetes.io/unhealthy-threshold-count: '3'

      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1"

      autoscaling:
        enabled: true
        minReplicas: 2
        maxReplicas: 10
        targetAverageUtilization: 70
        targetMemoryAverageUtilization: 80

    # Management Console UI
    ui:
      enabled: true
      replicaCount: 1
      image:
        repository: graviteeio/apim-management-ui
        tag: latest
        pullPolicy: Always

      env:
        - name: MGMT_API_URL
          value: "https://api.yourdomain.com/management/organizations/DEFAULT/environments/DEFAULT/"

      service:
        type: ClusterIP
        externalPort: 8002
        internalPort: 8080

      ingress:
        enabled: true
        ingressClassName: alb
        pathType: ImplementationSpecific
        path: /console(/.*)?
        hosts:
          - console.yourdomain.com
        annotations:
          alb.ingress.kubernetes.io/scheme: internet-facing
          alb.ingress.kubernetes.io/target-type: ip
          alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}, {"HTTP": 80}]'
          alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/certificate-id
          alb.ingress.kubernetes.io/ssl-redirect: '443'
          alb.ingress.kubernetes.io/healthcheck-path: /
          alb.ingress.kubernetes.io/healthcheck-interval-seconds: '30'

      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "250m"

      autoscaling:
        enabled: true
        minReplicas: 1
        maxReplicas: 3
        targetAverageUtilization: 70
        targetMemoryAverageUtilization: 80

    # Developer Portal UI
    portal:
      enabled: true
      replicaCount: 1
      image:
        repository: graviteeio/apim-portal-ui
        tag: latest
        pullPolicy: Always

      env:
        - name: PORTAL_API_URL
          value: "https://api.yourdomain.com/portal/environments/DEFAULT"

      service:
        type: ClusterIP
        externalPort: 8003
        internalPort: 8080

      ingress:
        enabled: true
        ingressClassName: alb
        pathType: Prefix
        path: /
        hosts:
          - portal.yourdomain.com
        annotations:
          alb.ingress.kubernetes.io/scheme: internet-facing
          alb.ingress.kubernetes.io/target-type: ip
          alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}, {"HTTP": 80}]'
          alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/certificate-id
          alb.ingress.kubernetes.io/ssl-redirect: '443'
          alb.ingress.kubernetes.io/healthcheck-path: /
          alb.ingress.kubernetes.io/healthcheck-interval-seconds: '30'

      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "250m"

      autoscaling:
        enabled: true
        minReplicas: 1
        maxReplicas: 3
        targetAverageUtilization: 70
        targetMemoryAverageUtilization: 80

    # External dependencies
    elasticsearch:
      enabled: false

    mongodb:
      enabled: false

    postgresql:
      enabled: false

    redis:
      enabled: false

    # Alert Engine
    alerts:
      enabled: false

    # Global configuration
    apim:
      name: apim

    # Main ingress disabled
    ingress:
      enabled: false
    ```

a. Replace `[ELASTIC PASSWORD FROM ES INSTALLATION]` with your Elasticsearch password.

b. If your Kubernetes cluster does not support IPV6 networking, both the UI and Portal deployments must set the `IPV4_ONLY` environment variable to `true`.

2. **(Enterprise Edition only)** Navigate to the following section, and then uncomment the following configuration:&#x20;

```yaml
 # License volume configuration for Management API (uncomment for enterprise edition)
  # extraVolumes: |
  #   - name: gravitee-license
  #     secret:
  #       secretName: gravitee-license
  # extraVolumeMounts: |
  #   - name: gravitee-license
  #     mountPath: "/opt/graviteeio-management-api/license/license.key"
  #     subPath: license.key
  #     readOnly: true
```

3. Save your Gravitee `values.yaml` file in your working directory.

<details>

<summary>Explanations of key predefined <code>values.yaml</code> parameter settings</summary>

**Service Configuration** The self-hosted setup uses `ClusterIP` services with AWS ALB ingress controllers for external access:

* **ClusterIP**: Internal cluster communication only - no direct external exposure
* **Ingress**: Routes external traffic through AWS Application Load Balancer to internal services
* **Domain-based routing**: Uses separate domains for Gateway, Management API, Console UI, and Portal UI
* **HTTPS enforcement**: All traffic redirected to HTTPS with SSL certificates from AWS ACM

**Resource Allocation** The configured resource limits ensure optimal performance while preventing resource exhaustion:

* **Management API/Gateway**: 1-2Gi memory, 500m-1 CPU (handles API processing, gateway routing, and management operations)
* **UI Components (Console/Portal)**: 256-512Mi memory, 100-250m CPU (lightweight frontend serving)

**Ingress Strategy** The ingress configuration enables external access with advanced AWS ALB features:

* **Multi-domain setup**: Separate domains for each component (gateway.yourdomain.com, api.yourdomain.com, console.yourdomain.com, portal.yourdomain.com)
* **Path-based routing**: Management API uses `/management` and `/portal` paths on the same domain
* **CORS enabled**: Comprehensive CORS headers configured at both application and ALB level for cross-origin requests
* **SSL/TLS**: ACM certificates with automatic HTTP to HTTPS redirection
* **Health checks**: Custom health check paths for each service (`/_health`, `/management/_health`)

**Autoscaling Configuration** Horizontal Pod Autoscaling is enabled for all components to handle variable load:

* **Management API/Gateway**: Scales 1-5 replicas based on 70% CPU and 80% memory utilization
* **UI Components**: Scales 1-3 replicas based on 70% CPU and 80% memory utilization
* **Dynamic scaling**: Automatically adjusts pod count based on actual resource consumption

**Security Configuration** Multiple security layers protect the deployment:

* **CORS policies**: Configured for all public-facing endpoints with specific allowed origins, methods, and headers
* **Security exclusions**: Public endpoints like `/auth/**`, `/_health`, and `/info`

</details>

### Install using Helm&#x20;

To install your Gravitee APIM with Helm, complete the following steps:

1.  Add the Gravitee Helm chart repository to your Kubernetes environment using the following command:

    ```bash
    helm repo add gravitee https://helm.gravitee.io
    ```
2.  Update the Helm repository with the following command:

    ```bash
    helm repo update
    ```
3.  Install the Helm chart with the Gravitee `values.yaml` file into the namespace using the following command:

    ```bash
    helm install gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./gravitee-eks-values.yaml \
      --wait \
      --timeout 10m
    ```

#### Verification&#x20;

Verify the installation was successful. The command output should be similar to the following:

```bash
NAME: gravitee-apim
LAST DEPLOYED: [DATE]
NAMESPACE: gravitee-apim
STATUS: deployed
REVISION: 1
```

To uninstall Gravitee APIM, use the following command:&#x20;

```bash
helm uninstall gravitee-apim --namespace gravitee-apim
```

## Verification&#x20;

To verify that your Gravitee APIM platform is up and running on EKS, complete the following steps:

1. [#access-gravitee-apim-web-interface](aws-eks.md#access-gravitee-apim-web-interface "mention")
2. [#validate-the-pods](#validate-the-pods-1)
3. [#validate-the-pods-2](#validate-the-pods-1)
4. [#validate-the-gateway-logs](aws-eks.md#validate-the-gateway-logs "mention")
5. [#validate-ingress](aws-eks.md#validate-ingress "mention")
6. [#validate-the-gateway-url](aws-eks.md#validate-the-gateway-url "mention")

### Access Gravitee APIM Web Interface

Access the Gravitee APIM web interface using the following steps:

#### Management Console&#x20;

Open your browser and navigate to: `https://console.yourdomain.com/console`  The interface allows you to configure APIs, policies, and monitor your API platform.&#x20;

#### Developer Portal&#x20;

Open your browser and navigate to: `https://portal.yourdomain.com/`  The self-service portal allows developers to discover and consume APIs.&#x20;

### Validate the Pods&#x20;

A healthy deployment displays all pods with the `Running` status, `1/1` ready containers, and zero or minimal restart counts.

To validate the pods, complete the following steps:&#x20;

1.  Use the following command to query the pod status:\


    ```bash
    kubectl get pods --namespace=gravitee-apim
    ```

#### 2. Verify that the deployment was successful. The output should show all Gravitee components ready and running: <a href="#validate-the-pods" id="validate-the-pods"></a>

```bash
NAME                                    READY   STATUS    RESTARTS   AGE
gravitee-apim-api-xxx-xxx               1/1     Running   0          23m
gravitee-apim-gateway-xxx-xxx           1/1     Running   0          23m
gravitee-apim-portal-xxx-xxx            1/1     Running   0          23m
gravitee-apim-ui-xxx-xxx                1/1     Running   0          23m
gravitee-elasticsearch-master-0         1/1     Running   0          23m
gravitee-mongodb-xxx-xxx                1/1     Running   0          23m
gravitee-postgresql-0                   1/1     Running   0          23m
gravitee-redis-master-0                 1/1     Running   0          23m
```

### Validate the Services  <a href="#validate-the-pods" id="validate-the-pods"></a>

1.  To verify service configuration, run the following command:\


    ```bash
    kubectl get services -n gravitee-apim
    ```


2.  Verify that all services are properly configured. The output should show all required services:\


    ```bash
    NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
    gravitee-apim-api                 ClusterIP   10.x.x.x        <none>        83/TCP
    gravitee-apim-gateway             ClusterIP   10.x.x.x        <none>        82/TCP
    gravitee-apim-ui                  ClusterIP   10.x.x.x        <none>        8002/TCP
    gravitee-apim-portal              ClusterIP   10.x.x.x        <none>        8003/TCP
    gravitee-mongodb                  ClusterIP   10.x.x.x        <none>        27017/TCP
    gravitee-elasticsearch            ClusterIP   10.x.x.x        <none>        9200/TCP,9300/TCP
    gravitee-postgresql               ClusterIP   10.x.x.x        <none>        5432/TCP
    gravitee-redis-master             ClusterIP   10.x.x.x        <none>        6379/TCP
    ```

    \


### Validate the Gateway logs&#x20;

To validate the Gateway logs, complete the following steps:

1.  List the Gateway pod using the following command:\


    ```bash
    kubectl get pods -n gravitee-apim | grep gateway
    ```



2.  Verify that the Gateway is running properly. The output should show the Gateway ready and running:\


    ```bash
    gravitee-apim-gateway-xxxxxxxxxx  1/1     Running   0          23m
    ```


3.  View the Gateway logs using the following command: \


    ```bash
    kubectl logs -f gravitee-apim-gateway-xxxxxxxxxxxx -n gravitee-apim
    ```



### Validate Ingress&#x20;

1.  Verify ingress is working with the following command:\


    ```bash
    kubectl get ingress -n gravitee-apim
    ```



2.  The output should show the hosts and ALB addresses: \


    ```bash
    NAME                           CLASS   HOSTS                      ADDRESS                                                                  PORTS     AGE
    gravitee-apim-api-management   alb     api.yourdomain.com         k8s-gravitee-gravitee-a1b2c3d4-1234567890.region.elb.amazonaws.com      80, 443   1h
    gravitee-apim-api-portal       alb     api.yourdomain.com         k8s-gravitee-gravitee-a1b2c3d4-1234567890.region.elb.amazonaws.com      80, 443   1h
    gravitee-apim-gateway          alb     gateway.yourdomain.com     k8s-gravitee-gravitee-e5f6g7h8-9876543210.region.elb.amazonaws.com      80, 443   1h
    gravitee-apim-portal           alb     portal.yourdomain.com      k8s-gravitee-gravitee-i9j0k1l2-5678901234.region.elb.amazonaws.com      80, 443   1h
    gravitee-apim-ui               alb     console.yourdomain.com     k8s-gravitee-gravitee-m3n4o5p6-3456789012.region.elb.amazonaws.com      80, 443   1h
    ```



### Validate the Gateway URL&#x20;

Validate your Gateway URL using the following steps:

1. [Validate Gateway URL using Ingress ](aws-eks.md#validate-gateway-url-using-ingress)
2. [Validate Gateway URL using Port Forwarding](aws-eks.md#validate-gateway-url-using-port-forwarding)

The Gateway URL is determined by the ingress configuration in your `values.yaml` file and AWS Route53 DNS settings pointing to the ALB endpoints.

#### Validate Gateway URL using Ingress&#x20;

To validate the Gateway URL, complete the following steps:

1.  Get the ALB DNS names from ingress:

    ```bash
    kubectl get ingress -n gravitee-apim -o wide
    ```
2.  Verify the Gateway endpoint directly, and then replace with your ALB DNS:

    ```bash
    # Test Gateway
    curl -H "Host: gateway.yourdomain.com" http://k8s-gravitee-gateway-xxxxxxxxxx-xxxxxxxxxx.region.elb.amazonaws.com/

    # Or if DNS is configured and SSL certificate is set up:
    curl https://gateway.yourdomain.com/
    ```
3.  Verify that the Gateway is responding correctly. The output should show the following message, which confirms that no API is deployed yet for this URL:

    ```bash
    No context-path matches the request URI.
    ```

#### Validate Gateway URL using Port Forwarding&#x20;

1.  Set up port forwarding for the Gateway using the following command:&#x20;

    ```bash
    kubectl port-forward svc/gravitee-apim-gateway 8082:82 -n gravitee-apim
    ```
2.  Verify via port forwarding using the following command:&#x20;

    ```bash
    curl http://localhost:8082/
    ```
3.  Verify that the Gateway is responding correctly. The output should show the following message, which confirms that no API is deployed yet for this URL.

    ```bash
    No context-path matches the request URI.
    ```

## Next steps <a href="#next-steps" id="next-steps"></a>

* Create your first API. For more information about creating your first API, see [Create & Publish Your First API](https://documentation.gravitee.io/apim/how-to-guides/create-and-publish-your-first-api).
* Add native Kafka capabilities. For more information about adding native Kafka capabilities, see [Configure the Kafka Client & Gateway](https://documentation.gravitee.io/apim/kafka-gateway/configure-the-kafka-client-and-gateway).

