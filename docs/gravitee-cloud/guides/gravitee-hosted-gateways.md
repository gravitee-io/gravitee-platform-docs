---
description: >-
  This guide explains how to deploy and run Cloud hosted gateways to your
  Gravitee Cloud Control Plane of API Management.
---

# Cloud Hosted Gateways

## Introduction

A full SaaS set up of Gravitee is a convenient way of running Gravitee. Gravitee manages operations related to your environments for both the Control Plane and all gateways. Deploying Cloud hosted gateways has the following benefits:

* **Automatic Configuration & Scaling**: Gravitee automatically configures and scales gateways in high availability setups, delivering the compute power and resources needed based on your subscription tier.
* **Managed Upgrades**: Gravitee provides automatic patch upgrades, with self-serve feature upgrades available for enhanced control.
* **Dedicated Environments**: Each Cloud hosted gateway is dedicated to an API Management environment of your choice (e.g., Production, Test, Development), ensuring isolation and security across environments.

## Deploying a Cloud hosted gateway

This section shows you how to connect a Cloud hosted gateway to your Gravitee Cloud API Management control plane environments.

You may deploy one Cloud hosted gateway for each environment. Dont worry about scaling and high availability, Gravitee will take of that.

{% hint style="info" %}
You do not have to scale your gateways. Gravitee scales your gateways and manages high-availability.
{% endhint %}

1. Navigate to your Gravitee Cloud Dashboard, and then in the Gateways section, select **Deploy Gateway** .

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption><p>Gravitee Cloud Dashboard with no gateways deployed yet.</p></figcaption></figure>

2. In the **Choose Gateway Deployment Method** pop-up window, Select **Gravitee Hosted Gateway**.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption><p>Gateway deployment screen with Cloud hosted gateways or Hybrid gateways as option.</p></figcaption></figure>

3. Select the environments that you want Cloud hosted gateways to, and then click **Deploy**.&#x20;

{% hint style="info" %}
* Environment dedicated Cloud hosted gateways are deployed even if you select more than one environment. Cloud hosted gateways are never shared between your environments.
* Deploying a Cloud hosted gateway will take around 5 minutes.
{% endhint %}

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption><p>Gateway deployment screen where you select environments that you want Cloud hosted gateways for.</p></figcaption></figure>

After you deploy a gateway, you are taken to your Gravitee Cloud Dashboard, where you see that your Cloud hosted gateways are being deployed.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>Gravitee Cloud Dashboard with a Cloud hosted gateway being deployed.</p></figcaption></figure>

## Verification

Once the gateways are deployed, you will see them as an entry in the Gateways section.

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption><p>Gravitee Cloud Dashboard with a Cloud hosted gateway deployed.</p></figcaption></figure>

## Viewing the details of a gateway

* To the view the details of a gateway, click the gateway name to see the gateway details. For example, the Gateway URL and host that has been set up for your gateways.

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption><p>Cloud hosted gateway settings screen.</p></figcaption></figure>

## Deploying APIs

Once you deploy the gateways, navigate to the API Management Console UI to create, deploy and start consuming APIs.

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption><p>API Management Developer Portal with an API deployed on a Cloud hosted Gateway. Notice the dedicated access URL for your API.</p></figcaption></figure>
