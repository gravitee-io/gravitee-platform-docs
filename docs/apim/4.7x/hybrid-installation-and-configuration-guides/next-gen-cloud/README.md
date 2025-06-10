# Next-Gen Cloud

## Overview

The minimum requirements for a Next-Gen Cloud deployment are the Gravitee Gateway and Redis. For more information on Redis, see [#self-hosted-data-plane-components](../#self-hosted-data-plane-components "mention").

## Prepare your installation

The following installation steps are common to all supported deployment methods.&#x20;

1. Send your Solutions Engineer the following details:
   * The email address of each user who needs an account.&#x20;
   * The region you have selected to host your Gravitee Cloud control.
2. Log in to Gravitee Cloud with the credentials provided by your Solutions Engineer. Each user is sent a an email with a login link.
3.  Select **Dashboard** from the menu, and then click **Deploy Gateway**.\


    <figure><img src="../../.gitbook/assets/00 1 copy (1).png" alt=""><figcaption></figcaption></figure>
4.  In the **Choose Gateway Deployment Method** modal, select **Hybrid Gateway**.\


    <figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>
5.  On the **Deploy Hybrid Gateway** screen, select the Environment to which you'd like to deploy the Gateway. For example, **Development**.\


    <figure><img src="../../.gitbook/assets/00 2 copy.png" alt=""><figcaption></figcaption></figure>
6.  Under **Provide your Access Point URLs**, enter the URL of either the load balancer or the machine on which you'd like to install the Gateway.\


    <figure><img src="../../.gitbook/assets/00 3 copy.png" alt=""><figcaption></figcaption></figure>
7.  Click **Generate Installation Details** to generate your Cloud Token and License Key. Copy your Cloud Token and License Key and save them somewhere secure. \


    <figure><img src="../../.gitbook/assets/00 4 copy.png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Your have prepared your installation for deployment.
{% endhint %}

## Deployment methods

To deploy your Gravitee Gateway, choose from the following technology stacks and deployment methods.

{% hint style="warning" %}
Deployment methods that are not linked to documentation are still fully supported. For more information, contact us.
{% endhint %}

### Docker

* Docker Compose
* [Docker CLI](docker/docker-cli.md)

### Kubernetes

* Vanilla Kubernetes
* AWS EKS
* Azure AKS
* GCP GKE
* [OpenShift](kubernetes/openshift.md)

### Linux

* [RPM](rpm.md)
* [.ZIP](.zip.md)

### Windows

* [.ZIP](.zip.md)

## Architecture

Your hybrid Gateway connects to the Cloud Control Plane through API endpoints exposed by Gravitee's secured Cloud Gate. These endpoints ensure that your Gateways stays up-to-date with your configuration. It also reports analytics back to your Cloud environment to provide a single unified view of analytics in the Gravitee Cloud Control Plane.

Authentication and authorization to the Cloud Gate is secured by using your very own, Cloud-account scoped, signed Cloud Tokens (JWT).

The Cloud Gate is deployed in each Control Plane data center region, which ensures optimal connectivity and performance. Your hybrid Gateway automatically calculates which region and corresponding Cloud Gate to connect to, based on the information contained in the Cloud Token.

{% hint style="info" %}
You need to allow your Gateway to connect to the Cloud Gate in the region your control plane is deployed. The traffic is over https (port 443) and the Cloud Gate URLs are as follows:\
\
US Cloud Gate: [https://us.cloudgate.gravitee.io/](https://us.cloudgate.gravitee.io/)\
EU Cloud Gate: [https://eu.cloudgate.gravitee.io/](https://eu.cloudgate.gravitee.io/)
{% endhint %}

Analytics are reported to a dedicated Cloud Account pipeline. Data is produced to a Kafka topic, ingested in Logstash, and finally stored in a dedicated Elastisearch index that is consumed by your Cloud Account's API Management Control Plane.

All communication between the hybrid Gateway and the Cloud Gate endpoints uses TLS encryption.

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption><p>Overview of a Gravitee Cloud deployment in Azure with a hybrid gateway connecting to the Gravitee Cloud API Management Control Plane using the Cloud Gate and Cloud Tokens.</p></figcaption></figure>

### Cloud Gate Endpoints

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

### Connection Flow

1. **Generate a Cloud Token.** Before connecting your Gateway, obtain a Cloud Token from your Cloud Control Plane.
2. **Copy your Cloud license.** To start up and read your APIs, mount your license on the Gateway.
3. **Start up the Gateway.** When the Gateway starts, it reads the Cloud Token, and then connects to the targeted Cloud Gate. You can now deploy APIs to the Gateway.
