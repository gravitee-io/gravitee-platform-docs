---
description: >-
  This guide explains how to connect self-hosted hybrid gateways to your
  Gravitee Cloud Control Plane of API Management.
---

# Hybrid

A hybrid API Management setup combines the ease of operations of a cloud-hosted control plane with the power and security of self-hosted gateways. A hybrid API Management setup provides the following benefits:

* **Data Residency and Compliance**: You can keep sensitive data within your infrastructure and ensure that data remains in the location where the resource owner resides, which helps you comply with data residency regulations.
* **Reduced Latency**: By hosting the gateway within your own infrastructure, API requests are processed closer to your services, which minimizes latency and enhances performance.
* **Full Control over Traffic**: All API traffic flows through your infrastructure, which provides you with complete control over routing, monitoring, and enforcing security policies outside of the policies executed on the gateway runtime.
* **Scalability and Flexibility**: You have full control over the scaling of the gateway.
* **Customization and Integration**: Integrate with your existing infrastructure and customize the deployment to meet your organization’s needs, whether you have specific security, monitoring, or logging requirements.
* **Security**: Sensitive API traffic does not need to leave your infrastructure, reducing exposure to potential threats and vulnerabilities. Additionally, you can enforce your organization's security measures directly at the Data Plane level.

## Gravitee Cloud hybrid architecture

Your hybrid gateway connects to the Cloud Control Plane through API endpoints exposed by Gravitee's secured Cloud Gate. These endpoints ensure that your gateways stays up-to-date with your configuration and reports analytics back to your cloud environment so you have one unified view of analytics in the Gravitee Cloud control plane.

Authentication and authorization to the Cloud Gate is secured by using your very own, Cloud account scoped, signed Cloud Tokens (JWT).

The Cloud Gate is deployed in each Control Plane data center region, which ensures optimal connectivity and performance. Your hybrid gateway will automatically calculate which region and corresponding Cloud Gate to connect to, based on the information contained in the Cloud Token.

{% hint style="info" %}
You need to allow your hybrid gateway to connect to the Cloud Gate in the region your control plane is deployed. The traffic is over https (port 443) and the Cloud Gate URLs are the following:\
\
US Cloud Gate: [https://us.cloudgate.gravitee.io/](https://us.cloudgate.gravitee.io/)\
EU Cloud Gate: [https://eu.cloudgate.gravitee.io/](https://eu.cloudgate.gravitee.io/)
{% endhint %}

Analytics are reported to a Cloud Account dedicated pipeline where Cloud Gate are produced to a Kafka topics, ingested in logstash, and finally stored in dedicated Elastisearch index that your Cloud Accounts API Management Control Plane consumes.

All communication between the hybrid gateway and the Cloud Gate endpoints is encrypted using TLS.

<figure><img src="../.gitbook/assets/image (29).png" alt=""><figcaption><p>Overview of a Gravitee Cloud deployment in Azure with a hybrid gateway connecting to the Gravitee Cloud API Management Control Plane using the Cloud Gate and Cloud Tokens.</p></figcaption></figure>

### Cloud Gate Endpoints

Here are two key endpoints that your gateway interact with:

* **`/sync` Endpoint**: The Data Plane fetches the latest API definitions, policies, and configurations from your Cloud Control Plane.
* **`/reports` Endpoint**: The Data Plane sends analytics and request logs to the Cloud Control Plane for storage in a dedicated index for your account.

### Cloud Token

To connect to the Cloud Gate, your gateway uses a **Cloud Token**, a signed JSON Web Token (JWT) that contains attributes (claims) related to your Cloud Account. This token provides the necessary authentication and authorization for your gateway to connect to the Cloud Control Plane.

To issue Cloud Tokens directly on your Cloud Account, complete the steps in the Hybrid Gateway deployment setup guide.

The Cloud Token contains the following information:

* The Cloud Account ID
* Control Plane Region information
* ID of analytics index
* A signature to verify authenticity

The Cloud Token is used to establish a secure and authenticated connection with the appropriate Cloud Gate endpoint.

### Connection Flow

1. **Generate a Cloud Token**: Before connecting your gateway, obtain a Cloud Token from your Cloud Control Plane dashboard hybrid gateway setup guide.
2. **Copy your Cloud license**: To start up and read you APIs, the gateway needs a license. You need to copy the license and then mount on the hybrid gateway. You get this license through the hybrid gateway set up
3. **Start up the gateway:** When the gateway starts, it will read the Cloud Token, and then connects to the targeted Cloud Gate. You are now all set to deploy APIs to the gateway.

### Hybrid Gateway Wizard

In this section, you can follow the steps to configure a Hybrid Gateway, and connect it to your Gravitee Cloud API Management control plane environment.

{% hint style="info" %}
You can deploy, run, and connect hybrid gateways according to your preference. To configure the hybrid gateways to your preferences, ensure that you provide your Cloud Token and License key.
{% endhint %}

1. On your Gravitee Cloud Dashboard, navigate to **Gateways**, and then click **Deploy Gateway**.

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption><p>Gravitee Cloud Dashboard with no Gateways deployed.</p></figcaption></figure>

2. In the **Choose Gateway Deployment Method** pop-up window, select **Hybrid Gateway**.

<figure><img src="../.gitbook/assets/image (1) (1) (1) (1).png" alt=""><figcaption><p>Gravitee Cloud Gateway deployment selection with both Gravitee Hosted Gateways (full SaaS) and Hybrid Gateways as options.</p></figcaption></figure>

3. From the **Platform** dropdown menu, select your preferred platform. This choice changes only the link reference to documentation
4. Select the Gravitee Cloud API Management Environment that you wish to connect the Hybrid gateway to.

<figure><img src="../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption><p>Gravitee Cloud Hybrid Gateway set up guide with selection of platform and environment.</p></figcaption></figure>

5. In the **Access Point** field, type the name of your host or hosts that your Hybrid gateway will is accessible through. You configured this host in your load balancer or ingress where you run the gateway.\
   \
   In Gravitee Cloud, the full resolved URL based on your gateway host is referred to as an Access Point.\
   \
   By default, all URLs are enforcing HTTPS.
6. To retrieve your Cloud Token and License key, Click **Generate Installation Details**

<figure><img src="../.gitbook/assets/image (3) (1) (1).png" alt=""><figcaption><p>The Deploy Hybrid Gateway screen where you should enter the gateway host that you hybrid gateway will listen to.</p></figcaption></figure>

7. Copy your Cloud Token, and then add it to your gateway deployment configuration (as described in step 9).
8. Copy your License, and then add it to your gateway deployment configuration (as described in step 9).

<figure><img src="../.gitbook/assets/image (5) (1).png" alt=""><figcaption><p>Gravitee Cloud Hybrid Gateway set up with last step where you are able to copy your generated Cloud Token and your License.</p></figcaption></figure>

9. Install the Gravitee APIM Gateway. To install the APIM Gateway, complete any of the following sub-steps: &#x20;

{% tabs %}
{% tab title="Docker" %}
### Procedure

1\. Copy your Cloud Token and License Key.

2\. Run the following script:

```bash
docker run -d \
  --name gio-apim-hybrid-gateway \
  -p 8082:8082 \
  -e gravitee_ratelimit_type=none \
  -e gravitee_cloud_token=<cloud_token> \
  -e gravitee_license_key=<license_key> \
  graviteeio/apim-gateway:<CONTROL_PLANE_VERSION>
```

* Replace \<cloud\_token> and \<license\_key> with the Cloud token and License Key from steps 7 and 8.
* Replace \<CONTROL\_PLANE\_VERSION> with the current version of the Control Plane in Gravitee Cloud.

{% hint style="info" %}
**Rate Limiting**: If you want to enable rate-limiting of APIs, please consult this documentation to configure your Hybrid Gateway to use a rate-limiting repository, such as Redis: [https://documentation.gravitee.io/apim/configure-apim/apim-components/gravitee-gateway#configure-the-rate-limit-repository](https://documentation.gravitee.io/apim/configure-apim/apim-components/gravitee-gateway#configure-the-rate-limit-repository)

Example Docker Run command:

```bash
docker run -d \
  --name gio-apim-hybrid-gateway \
  -p 8082:8082 \
  -e gravitee_ratelimit_type=redis \
  -e gravitee_ratelimit_redis_host=redis \
  -e gravitee_ratelimit_redis_port=6379 \
  -e gravitee_ratelimit_redis_password=${redis_password} \
  -e gravitee_ratelimit_redis_ssl=false \
  -e gravitee_cloud_token=<cloud_token> \
  -e gravitee_license_key=<license_key> \
  graviteeio/apim-gateway:<CONTROL_PLANE_VERSION>
```
{% endhint %}
{% endtab %}

{% tab title="Kubernetes (Helm)" %}
### **Before you begin**

You must install the following command line tools:

* [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [Helm v3](https://helm.sh/docs/intro/install/)

### Procedure

1. **Set up Helm**

Add the Gravitee Helm chart repo using the following command:

<pre class="language-bash"><code class="lang-bash"><strong>helm repo add graviteeio https://helm.gravitee.io
</strong></code></pre>

2. **Configure `values.yaml` file**

On your local machine, copy the following text into a file called `values.yaml`:

```yaml
gateway:
    replicaCount: 1
    image:
        repository: graviteeio/apim-gateway
        tag: <CONTROL_PLANE_VERSION>
        pullPolicy: IfNotPresent
    autoscaling:
        enabled: false
    podAnnotations:
        prometheus.io/path: /_node/metrics/prometheus
        prometheus.io/port: "18082"
        prometheus.io/scrape: "true"
    env:
        - name: gravitee_cloud_token
          value: "<cloud_token>"
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
        type: LoadBalancer
        externalPort: 8082
        loadBalancerIP: 127.0.0.1
    ingress:
        enabled: false
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

api:
    enabled: false

ratelimit:
    type: none

portal:
    enabled: false

ui:
    enabled: false

alerts:
    enabled: false

es:
    enabled: false

license:
    key: "<license_key>"
```

* Replace \<CONTROL\_PLANE\_VERSION> with the current version of the Control Plane in Gravitee Cloud (e.g.: "4.5.4").
* Replace \<cloud\_token> with your Cloud Token.
* Replace the \<license\_key> with your License Key.

{% hint style="info" %}
**Rate Limiting**: If you want to enable rate-limiting of APIs, please consult this documentation to configure your Hybrid Gateway to use a rate-limiting repository, such as Redis: [https://documentation.gravitee.io/apim/configure-apim/apim-components/gravitee-gateway#configure-the-rate-limit-repository](https://documentation.gravitee.io/apim/configure-apim/apim-components/gravitee-gateway#configure-the-rate-limit-repository)

Example additional configuration in your `values.yaml` file:

<pre class="language-yaml"><code class="lang-yaml">gateway:
<strong>    ...
</strong>ratelimit:
    type: redis
    redis:
        host: 'redis.mycompany'
        port: 6379
        password: 'mysecretpassword'
        ssl: false
redis:
    download: true
</code></pre>
{% endhint %}

* **Run Helm Install**

Install the Helm chart with the `values.yaml` file to a dedicated namespace using the following command:

```bash
helm install graviteeio-apim4x graviteeio/apim --create-namespace --namespace gravitee-apim -f ./values.yaml
```
{% endtab %}

{% tab title="OpenShift" %}
{% hint style="info" %}
To deploy APIM with OpenShift, you must be running **OpenShift version 3.10 or later**. This is required because the Gravitee Helm Chart only supports Ingress standard objects. It does not support the specific OpenShift Routes.
{% endhint %}

When deploying APIM within OpenShift, you must:&#x20;

* Use the full host domain instead of paths for all components. Ingress paths are not sufficiently supported by OpenShift.
* Override the security context to let OpenShift automatically define the `user-id` and `group-id` with which to run containers.
* Set the `ingressClassName` to "none" for OpenShift to automatically create Routes from Ingress.

Below is a standard `values.yaml` to deploy the Gravitee APIM Gateway into OpenShift:

```yaml
gateway:
  replicaCount: 1
  image:
    repository: graviteeio/apim-gateway
    tag: 4.6.7
    pullPolicy: IfNotPresent
  autoscaling:
    enabled: false
  podAnnotations:
    prometheus.io/path: /_node/metrics/prometheus
    prometheus.io/port: "18082"
    prometheus.io/scrape: "true"
  env:
    - name: gravitee_cloud_token
      value: "${your-cloud-token}"
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
  resources:
    limits:
      cpu: 500m
      memory: 1024Mi
    requests:
      cpu: 200m
      memory: 1024Mi
  ingress:
    ingressClassName: none
    path: /
    hosts:
      - gw-graviteeio.apps.openshift-test.l8e4.p1.openshiftapps.com
    annotations:
      route.openshift.io/termination: edge
  securityContext: null
  deployment:
    securityContext:
      runAsUser: null
      runAsGroup: null
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault
  reporters:
    file:
      enabled: false
  terminationGracePeriod: 50
  gracefulShutdown:
    delay: 20
    unit: SECONDS

api:
    enabled: false

ratelimit:
    type: none

portal:
    enabled: false

ui:
    enabled: false

alerts:
    enabled: false

es:
    enabled: false

license:
    key: "${your-license-key}"
```
{% endtab %}

{% tab title="Linux/Windows" %}
Below is a sample working configuration for the Binary/RPM use case. It configures both the proxy and Redis.

```yaml
management:
  # HTTP TYPE FOR THE GRAVITEE CLOUD GATE
  type: http 
  # OPTIONAL PROXY CONFIG
  # http:
  #   proxy:
  #     useSystemProxy: false
  #     enabled: true
  #     type: HTTP
  #     host: proxy.example.com
  #     port: 8080
  #     username: proxy-username
  #     password: proxy-password

# CLOUD TOKEN TO SECURE CONNECTION TO THE CLOUD GATE
cloud:
  token: YOUR-CLOUD-TOKEN

# REDIS TO STORE AND SHARE BETWEEN GATEWAYS INSTANCES (HA)
# THE RATE LIMIT / QUOTA COUNTERS AND CACHE DATA
ratelimit:
  type: none
  # type: redis
  # redis:
  #   host: localhost
  #   port: 6379
  #   password:

# LICENCE KEY B64 ENCODED
license:
  key: YOUR-LICENCE-KEY
```
{% endtab %}
{% endtabs %}

10. Click **Return to Overview**. In the **Gateways** section of the **Overview** page, you can see your configured gateway.

<figure><img src="../.gitbook/assets/image (7) (1).png" alt=""><figcaption><p>Gravitee Cloud Dashboard, now with one hybrid gateway configuration added to Development environment.</p></figcaption></figure>

#### Verification

To verify that the gateway is running, make a GET request on the URL you have published the gateway on to make sure it is up and running.\
\
You will see a default message like:

```
No context-path matches the request URI.
```

\
You can now create and deploy APIs to your Hybrid Gateway.
