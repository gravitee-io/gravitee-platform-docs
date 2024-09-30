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

Analytics are reported to a Cloud Account dedicated pipeline where Cloud Gate are produced to a Kafka topics, ingested in logstash, and finally stored in dedicated Elastisearch index that your Cloud Accounts API Management Contorl Plane consumes.

All communication between the hybrid gateway and the Cloud Gate endpoints is encrypted using TLS.

<figure><img src="../.gitbook/assets/image (27).png" alt=""><figcaption><p>Overview of a Gravitee Cloud deployment in Azure US region west-us, with a hybrid gateway connecting to the Gravitee Cloud API Management Control Plane using the Cloud Gate and Cloud Tokens. </p></figcaption></figure>

### Cloud Gate Endpoints

Here are two key endpoints that your gateway interact with:

* **`/sync` Endpoint**: The Data Plane fetches the latest API definitions, policies, and configurations from your Cloud Control Plane.
* **`/reports` Endpoint**: The Data Plane sends analytics and request logs to the Cloud Control Plane for storage in a dedicated index for your account.

### Cloud Token

To connect to the Cloud Gate, your gateway uses a **Cloud Token**, a signed JSON Web Token (JWT) that contains attributes (claims) related to your Cloud Account. This token provides the necessary authentication and authorization for your gateway to connect to the Cloud Control Plane.

To issue Cloud Tokens directly on your Cloud Account, complete the steps in the Hybrid Gateway deployment setup guide.&#x20;

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

