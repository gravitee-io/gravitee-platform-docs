# Cloud Tokens

## Introduction

Cloud tokens are secure, signed Json Web Tokens (JWT) that enable connection between your self-hosted services and the Gravitee Next-Gen Cloud API Management Control Plane. You can use Cloud Tokens to perform the following actions:

* Import APIs from other Gateways via Gravitee’s Federated API Management (APIM) capability.
* Manage APIs across your APIM Environments in Gravitee Cloud via the Gravitee Kubernetes Operator (GKO).

{% hint style="info" %}
Cloud Token management is available to Account Administrators only.
{% endhint %}

## Create a Cloud Token

To create a Cloud Token, complete the following steps:

1. Log in to your Cloud Console.
2.  Select **Settings > Cloud tokens** from the menu, and then click **Generate Cloud Token**.

    <figure><img src="../.gitbook/assets/image (3) (1).png" alt=""><figcaption></figcaption></figure>
3.  Give your Cloud Token a meaningful name, select the token type and environment, and then click **Confirm**.&#x20;

    <figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>
4.  Save your Cloud Token. You cannot access it once you close the dialog  box.&#x20;

    <figure><img src="../.gitbook/assets/image (4) (1).png" alt=""><figcaption></figcaption></figure>
5.  Verify that your Cloud Token is listed in the table.&#x20;

    <figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Your Cloud Token can now be used in your Federation Agent configuration file or GKO Management Context file.
{% endhint %}
