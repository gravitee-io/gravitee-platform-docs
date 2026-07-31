---
description: An overview about next-gen cloud.
metaLinks:
  alternates:
    - ./
---

# Next-Gen Cloud

## Overview

The minimum requirements for a Next-Gen Cloud deployment are the Gravitee Gateway and Redis. For more information on Redis, see [#self-hosted-data-plane-components](../#self-hosted-data-plane-components "mention").

## Prepare your installation

The following installation steps are common to all supported deployment methods.

1.  Sign in to [Gravitee Cloud](https://cloud.gravitee.io/).

    <figure><img src="../../.gitbook/assets/sign-in-to-gravitee-cloud.png" alt=""><figcaption></figcaption></figure>
2.  From the **Dashboard**, click **Deploy Gateway**.

    <figure><img src="../../.gitbook/assets/5458CF8E-7FFE-4961-9EE5-761E3A3E75CB.jpeg" alt=""><figcaption></figcaption></figure>
3.  In the **Choose Gateway Deployment Method** modal, select **Hybrid Gateway**.

    <figure><img src="../../.gitbook/assets/select-hybrid-gateway.png" alt=""><figcaption></figcaption></figure>
4.  On the **Deploy Hybrid Gateway** screen, select the Environment to which you'd like to deploy the Gateway. For example, **Development**.

    <figure><img src="../../.gitbook/assets/select-environment.png" alt=""><figcaption></figcaption></figure>
5.  In **URLs & Domains**, enter the names of the HTTP domains through which you can access your Hybrid Gateway. By default, all URLs enforce HTTPS.

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>You must configure these HTTP domains/hostnames in your load balancer or ingress where you run the Gateway</p></div>

    <figure><img src="../../.gitbook/assets/deploy-your-gateway.png" alt=""><figcaption></figcaption></figure>
6.  Click **Generate Installation Details** to generate your Cloud Token and License Key. Copy your Cloud Token and License Key and save them somewhere secure.

    <figure><img src="../../.gitbook/assets/generate-installation-details.png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Your have prepared your installation for deployment.
{% endhint %}

## Deployment methods

To deploy your Gravitee Gateway, choose from the following technology stacks and deployment methods.

{% hint style="warning" %}
Deployment methods that are not linked to documentation are still fully supported. For more information, contact Gravitee.
{% endhint %}

### Docker

* [Docker Compose](docker/docker-compose.md)
* [Docker CLI](docker/docker-cli.md)

### Kubernetes

* [Vanilla Kubernetes](kubernetes/vanilla-kubernetes/README.md)
* [AWS EKS](kubernetes/aws-eks.md)
* [Azure AKS](kubernetes/azure-aks.md)
* [OpenShift](kubernetes/openshift.md)
* GCP GKE

### Linux

* [RPM](rpm.md)
* [.ZIP](.zip.md)

### Windows

* [.ZIP](.zip.md)

## Architecture

Your hybrid Gateway connects to the Cloud Control Plane through API endpoints exposed by Gravitee's secure Cloud Gate. This connection ensures that your Gateway stays up to date with your configuration. Your Gateway also reports analytics data back to your Cloud environment so that the Gravitee Cloud Control Plane can offer a single unified view of analytics.

Cloud Gate authentication and authorization are secured using your Cloud Token (JWT), which is scoped and signed for your personal Cloud account.

The Cloud Gate is deployed in each data center region of the Control Plane to ensure optimal connectivity and performance. Your hybrid Gateway uses the information contained in your Cloud Token to automatically calculate the region and corresponding Cloud Gate to which it should connect.

{% hint style="info" %}
Your Gateway needs to connect to the Cloud Gate in the region where your Control Plane is deployed. The traffic is routed over HTTPS/443 to the following Cloud Gate URLs:\
\
US Cloud Gate: `https://us.cloudgate.gravitee.io/`\
EU Cloud Gate: `https://eu.cloudgate.gravitee.io/`
{% endhint %}

Analytics are reported to a dedicated Cloud account pipeline. Data is produced to a Kafka topic, ingested in Logstash, and then stored in a dedicated Elasticsearch index that is consumed by your Cloud account's API Management Control Plane.

All communication between the hybrid Gateway and the Cloud Gate endpoints uses TLS encryption.

<figure><img src="../../.gitbook/assets/hybrid-installation-and-configuration-gu-29-1-1.png" alt=""><figcaption><p>Overview of a Gravitee Cloud deployment in Azure with a hybrid gateway connecting to the Gravitee Cloud API Management Control Plane using the Cloud Gate and Cloud Tokens.</p></figcaption></figure>

### Cloud Gate endpoints

Here are two key endpoints that your Gateway interacts with:

* **`/sync` Endpoint**: The Data Plane fetches the latest API definitions, policies, and configurations from your Cloud Control Plane.
* **`/reports` Endpoint**: The Data Plane sends analytics and request logs to the Cloud Control Plane for storage in a dedicated index for your account.

### Cloud Token

To connect to the Cloud Gate, your Gateway uses a Cloud Token, which is a signed JSON Web Token (JWT) that contains attributes (claims) related to your Cloud Account. This token provides the necessary authentication and authorization for your Gateway to connect to the Cloud Control Plane.

The Cloud Token contains the following information:

* The Cloud Account ID
* Control Plane Region information
* ID of analytics index
* A signature to verify authenticity

The Cloud Token is used to establish a secure and authenticated connection with the appropriate Cloud Gate endpoint.

### Connection flow

1. **Generate a Cloud Token.** Before connecting your Gateway, obtain a Cloud Token from your Cloud Control Plane.
2. **Copy your Cloud license.** To start up and read your APIs, mount your license on the Gateway.
3. **Start up the Gateway.** When the Gateway starts, it reads the Cloud Token, and then connects to the targeted Cloud Gate. You can now deploy APIs to the Gateway.

## Stop sending analytics to the Cloud Control Plane

Some organizations keep API traffic data inside their own infrastructure and don't want analytics or request logs leaving it. You can turn off the Cloud reporter so that the Gateway stops using the `/reports` endpoint, while the `/sync` endpoint keeps delivering API definitions, policies, and configuration from the Control Plane.

To turn off the Cloud reporter, set the following environment variable on the Gateway:

```bash
gravitee_reporters_reportercloud_enabled=false
```

For a Linux or Windows installation, set the variable in the environment of the process that runs the Gateway.

{% hint style="warning" %}
Setting `reporters.reportercloud.enabled: false` in `gravitee.yml`, or under `gateway.reporters` in your Helm values, doesn't turn off the Cloud reporter. Set it as an environment variable, as shown in the following examples.
{% endhint %}

### Kubernetes

Add the environment variable to `gateway.env` in your Helm values:

```yaml
gateway:
  env:
    - name: gravitee_reporters_reportercloud_enabled
      value: "false"
```

### Docker

Pass the environment variable alongside your Cloud Token and license key:

```yaml
services:
  gateway:
    image: graviteeio/apim-gateway:latest
    environment:
      - gravitee_cloud_token=${CLOUD_TOKEN}
      - gravitee_license_key=${LICENSE_KEY}
      - gravitee_reporters_reportercloud_enabled=false
```

Once the Gateway restarts, requests it serves no longer appear in the analytics and runtime logs of your Cloud Control Plane. The Gateway stays connected to the Cloud Gate and continues to receive configuration.

{% hint style="warning" %}
Confirm this in a non-production environment before you roll it out. Verify both halves: that new traffic stops appearing in the Control Plane analytics, and that an API change made in the Control Plane still reaches the Gateway.
{% endhint %}

{% hint style="info" %}
To keep analytics while sending them somewhere you control, configure another reporter instead of, or alongside, this setting. See [reporters](../../analyze-and-monitor-apis/reporters/README.md).
{% endhint %}

Setting `cloud.enabled` to `false` is a different action. That severs the whole Cloud Gate connection, so the Gateway stops receiving configuration as well. See [configure Cloud Gateway client](../proxy-configuration/configure-cloud-gateway-client.md).
