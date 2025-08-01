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

```bash
NAME                              READY   STATUS    RESTARTS   AGE
gravitee-apim-redis-master-0      1/1     Running   0          2m
gravitee-apim-redis-replicas-0    1/1     Running   0          2m
gravitee-apim-redis-replicas-1    1/1     Running   0          2m
gravitee-apim-redis-replicas-2    1/1     Running   0          2m
```

### Prepare `values.yaml` for Helm

To prepare your Gravitee values.yaml file for Helm, complete the following steps:

1.  Copy the following Gravitee values.yaml file. This is the base configuration for your new hybrid Gateway.\


    ```yaml
    #This is the license key provided in your Gravitee Cloud account 
    license:
        key: "<license key>"

    #This section controls the Management API component deployment of Gravitee. 
    #It is disabled for a hybrid gateway installation
    api:
        enabled: false

    #This section controls the Developer Portal API component deployment of Gravitee. 
    #It is disabled for a hybrid gateway installation
    portal:
        enabled: false

    #This section controls the API Management Console component deployment of Gravitee. 
    #It is disabled for a hybrid gateway installation
    ui:
        enabled: false

    #This section controls the Alert Engine component deployment of Gravitee. 
    #It is disabled for a hybrid gateway installation
    alerts:
        enabled: false

    #This section controls the Analytics Database component deployment of Gravitee based on ElasticSearch. 
    #It is disabled for a hybrid gateway installation
    es:
        enabled: false
        
    #This section has multiple parameters to configure the API Gateway deployment  
    gateway:
        replicaCount: 1 #number of replicas of the pod
        image:
            repository: graviteeio/apim-gateway
            #The gateway version to install. 
            #It has to align with the control plane of your Gravitee Cloud
            #use it if you need to force the version of the gateway
            # tag: 4.7.6 
            pullPolicy: IfNotPresent
        autoscaling:
            enabled: false
        podAnnotations:
            prometheus.io/path: /_node/metrics/prometheus
            prometheus.io/port: "18082"
            prometheus.io/scrape: "true"
        #Sets environment variables.  
        env:
            #Gravitee Cloud Token. 
            #This is the value gathered in your Gravitee Cloud Account when you install a new Hybrid Gateway.
            - name: gravitee_cloud_token
              value: "<gravitee cloud token>"
        
        #Configure the API Gateway internal API. 
        services:
            #The following sections enables the exposure of metrics to Prometheus. 
            metrics:
                enabled: true
                prometheus:
                    enabled: true
            #This enables the Gravitee APIM Gateway internal API for monitoring and retrieving technical information about the component.
            core:
                http:
                    enabled: true
            sync:
                kubernetes:
                    enabled: false
            #disables bridge mode. unnecessary for a hybrid gateway.
            bridge:
                enabled: false

        # Uncomment and configure if you need LoadBalancer service
        # service:
        #     type: LoadBalancer
        #     externalPort: 8082
        #     annotations:
        #         service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
        #         service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"

        #ingress setup for AWS
        #This will setup the ingress rule for the gateway using AWS Load Balancer Controller
        ingress:
          enabled: true
          pathType: Prefix
          path: /
          # AWS Load Balancer Controller ingress class
          ingressClassName: "alb"
          # Used to create an Ingress record.
          # Multiple hostnames supported
          #the hosts setting should match at least one of the hosts you setup in Gravitee Cloud for the gateway you are deploying
          #example: apigw.eks.example.com
          hosts:
            - <hosts>
          annotations:
            # AWS Load Balancer Controller annotations
            alb.ingress.kubernetes.io/scheme: internet-facing
            alb.ingress.kubernetes.io/target-type: ip
            alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
            # Uncomment for SSL redirect
            # alb.ingress.kubernetes.io/ssl-redirect: '443'
            # Uncomment to specify SSL certificate ARN
            # alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/certificate-id
          # Uncomment for TLS configuration
          #tls:
          #  - hosts:
          #      - apigw.eks.example.com
          #    secretName: gravitee-tls-secret

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
        #Reporter configuration section.
        #no additional reporter enabled for the hybrid gateway outside of the default Cloud Gateway reporter
        reporters:
            file:
                enabled: false
        terminationGracePeriod: 50
        gracefulShutdown:
            delay: 20
            unit: SECONDS
        ratelimit:
            #redis setup for the rate limit database
            redis:
                host: "<redis host>"
                port: 6379
                password: "<redis password>"
                ssl: false
            
    ratelimit:
        type: redis
            
    # Auto-download the Gravitee Redis plugin
    redis:
        download: true
    ```



2. Make the following modifications to your `values.yaml` file:
   * Replace `<cloud_token>` with your Cloud Token.
   * Replace `<license_key>` with your License Key.
   * Replace `<redis_hostname>` with your extracted Redis hostname.
   * Replace `<redis_password>` with your extracted Redis password.
   * Replace `<hosts>` with the host information you entered in the Gravitee \
     Cloud Gateway setup.
   *   Set the `tag` field in the Gateway image section to the value displayed in the Overview section of your Gravitee Cloud Dashboard. \


       <figure><img src="../../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The `tag` field specifies the version of your Gravitee Gateway. Your Gateway version must match your Gravitee Cloud Control Plane version to ensure compatibility between your hybrid Gateway and the Cloud Management platform.
{% endhint %}



