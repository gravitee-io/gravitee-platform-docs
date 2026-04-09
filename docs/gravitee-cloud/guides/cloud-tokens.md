---
description: Overview of Cloud Tokens.
---

# Cloud Tokens

## Introduction

Cloud tokens are secure, signed Json Web Tokens (JWT) that enable connection between your self-hosted services and the Gravitee Next-Gen Cloud API Management Control Plane. You can use Cloud Tokens to perform the following actions:

* Import APIs from other Gateways via Gravitee’s Federated API Management (APIM) capability.
* Manage APIs across your APIM Environments in Gravitee Cloud via the Gravitee Kubernetes Operator (GKO).

### Where Cloud Tokens are used&#x20;

Cloud Tokens authenticate the following self-hosted components to Gravitee Next-Gen Cloud. In every case, you only need to provide the token: the endpoint, organization, and environment are read from the token's JWT claims.

* **Federation Agent.** A Cloud Token authenticates a Federation Agent that imports APIs from a third-party gateway such as Apigee, AWS API Gateway, Azure API Management, Confluent Platform, IBM API Connect, Mulesoft Anypoint, or Solace. For details, see [Federation Agent Service Account.](https://documentation.gravitee.io/apim/govern-apis/federation/federation-agent-service-account)
* **Gravitee Kubernetes Operator (GKO).** A Cloud Token in a `ManagementContext` resource lets GKO manage APIs across your Cloud environments. For details, see the [GKO quickstart guide.](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/getting-started/quickstart-guide)
* **Terraform provider.** A Cloud Token authenticates the Gravitee APIM Terraform provider so it can manage Cloud resources as Infrastructure as Code. For details, see the Terraform [quick start guide.](https://documentation.gravitee.io/apim/terraform/quick-start-guide)
* **Hybrid Gateway.** A Cloud Token links a self-hosted hybrid Gateway to the Cloud Control Plane. For details, see [Generate a new Cloud Token.](https://documentation.gravitee.io/apim/hybrid-installation-and-configuration-guides/next-gen-cloud/generate-a-new-cloud-token)



{% hint style="info" %}
Cloud Token management is available to Account Administrators only.
{% endhint %}

## Create a Cloud Token

To create a Cloud Token, complete the following steps:

1. Log in to your Cloud Console.
2.  Select **Settings > Cloud tokens** from the menu, and then click **Generate Cloud Token**.

    <figure><img src="../.gitbook/assets/image (3) (1).png" alt=""><figcaption></figcaption></figure>
3.  Give your Cloud Token a meaningful name, select the token type and environment, and then click **Confirm**.

    <figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>
4.  Save your Cloud Token. You cannot access it once you close the dialog box.

    <figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>
5.  Verify that your Cloud Token is listed in the table.

    <figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Your Cloud Token can now be used in your Federation Agent configuration file or GKO Management Context file.
{% endhint %}

### Verification

To verify your Cloud Token was created successfully, follow these steps:

1. In the Cloud Console, select **Settings > Cloud tokens**. The new Cloud Token appears in the table with its name, type, environment, and creation date.
