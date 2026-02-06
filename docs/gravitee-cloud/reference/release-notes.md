---
description: Release notes for Release Notes.
---

# Release Notes

This section contains an overview of the new features in Gravitee Cloud's releases. For information about the releases, see the following articles:

## February 2026&#x20;

<details>

<summary>5th February </summary>

**GCP Private Network**

You can now create a private network for SaaS Gateways deployed in the Google Cloud Platform (GCP). This service lets you connect to upstream services without exposing traffic to the public internet.

</details>

## December 2025

<details>

<summary>18 December </summary>

**Promote APIs**

You can now promote V4 APIs from one environment to another environment. For example, Staging to Production. For more information about promoting APIs, see [Promote APIs.](https://documentation.gravitee.io/apim/create-and-configure-apis/create-apis/promote-apis)

**V4 APIs are default in API Designer**&#x20;

In API Designer, V4 APIs are now the default API type when you create an API. For more information about creating an API with the API Designer, see [API Designer](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/ePLkAjjF4tUASuMeIrXC/ "mention").



</details>

## November 2025

<details>

<summary>19 November </summary>

**Delete SaaS Gateways and environments**

You can now delete SaaS Gateways and environments, including the default environments. For more information about deleting Gatways and environments, see [delete-a-gravitee-hosted-gateway.md](../guides/gravitee-hosted-gateways/delete-a-gravitee-hosted-gateway.md "mention").

</details>

## October 2025

<details>

<summary>17th October </summary>

**Deploy a SaaS Gateway in Google Cloud Platform (GCP)**

You can now deploy a SaaS Gateway in Google Cloud Platform (GCP). You can deploy the Gateway in the following regions:&#x20;

* US: `us-central1`.
* EU: `europe-west3`
* APAC: `asia-southeast1`.

For more information about Gateway providers and the available regions for each provider, see [geography-and-provider-support.md](geography-and-provider-support.md "mention").

</details>

<details>

<summary>14 October</summary>

**Deploy SaaS Gateways with multiple provides and in multiple regions**

You can now deploy your SaaS Gateways with multiple provider and in multiple regions. For more information about deploying your SaaS Gateways, see [gravitee-hosted-gateways](../guides/gravitee-hosted-gateways/ "mention").

</details>

## July 2025

<details>

<summary>28th July</summary>

**Deploy a SaaS Gateway in AWS**

You can now deploy a SaaS Gateway in AWS. You can deploy a Gateway only in `us-east-1`. For more information about Gateway providers and the available regions for each provider, see [geography-and-provider-support.md](geography-and-provider-support.md "mention").

</details>

## May 2025

<details>

<summary>21st May</summary>

**Retrieve user info from the token or userInfo endpoint**&#x20;

You can now retrieve a user's profile information from either the token or the `userInfo` endpoint. For more information about retrieving a user's profile information, see [configure-sso.md](../guides/configure-sso.md "mention").

</details>

<details>

<summary>15th May</summary>

**Adding Environments**

You can now request more environments in Gravitee Cloud to map out your specific organization. For more information about linking additional environments to your account, contact Gravitee. To learn more about how to add a new environment after it is linked, see [add-environments.md](../guides/add-environments.md "mention").

</details>

## April 2025

<details>

<summary>29th April</summary>

You can now configure Custom Domains for Gravitee-hosted Gateways and the Developer Portal. This feature lets you personalize your infrastructure URLs with your own domain names to provide a consistent branded experience across your entire API ecosystem.

To set up a Custom Domain, select the Gravitee-hosted Gateway you want to personalize from your Dashboard, and then enter your information in the Custom Domain section. You can easily reset your Custom Domain configuration if needed.

For more information, see the [Custom Domains](../guides/custom-domains.md) documentation.

</details>

## November 2024

<details>

<summary>6th November</summary>

**Cloud Hosted Gateways**

We’re thrilled to introduce **Cloud Hosted Gateways** for Gravitee Cloud API Management! With Cloud Hosted Gateways, Gravitee takes care of the setup and maintenance for your gateway environments, allowing you to focus on managing your APIs effortlessly.

**Key benefits include:**

* **Automatic Configuration & Scaling**: Gravitee automatically configures and scales gateways in high availability setups, delivering the compute power and resources needed based on your subscription tier.
* **Managed Upgrades**: Gravitee provides automatic patch upgrades, with self-serve feature upgrades available for enhanced control.
* **Dedicated Environments**: Each Cloud hosted gateway is dedicated to an API Management environment of your choice (e.g., Production, Test, Development), ensuring isolation and security across environments.

Deploying a Cloud Hosted Gateway takes just a few minutes. Simply navigate to your Gravitee Cloud Dashboard, select your environment to deploy Cloud hosted gateways for, and Gravitee will handle the rest!

[Read more about deploying Cloud Hosted Gateways here](../guides/gravitee-hosted-gateways/)

</details>

## September 2024

<details>

<summary>28th September</summary>

**Hybrid Gateways**

You can now, in a simple self-serve, manned deploy self-hosted hybrid gateways to your Gravitee Cloud API Management environments.\
\
Configuration will be synced securely from Cloud Gate components, and transactional analytics data will be sent from the gateway to your dedicated analytics index. So it can be viewed in detail in the API Management Control Plane Dashboard.\
\
Read more about the feature [here](https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/hybrid-installation-and-configuration-guides).

</details>
