---
description: >-
  This article describes how to configure sharding tags when customizing
  deployments via your API proxy settings
---

# Sharding Tags

## Introduction

Sharding tags allow you to “tag” Gateways with a keyword and deploy an API to a Gateway with a certain tag. Gateways can be tagged with one or more sharding tags. Additionally, the `!` symbol can be placed before the tag name to specify exclusion rules.

To learn more about how to deploy APIs to specific Gateways based on sharding tags, refer to [Configure Deployments](docs/apim/4.6/configure-v2-apis/proxy-settings.md).

The sections below discuss:

* [Tagged Gateway/API behavior](sharding-tags.md#tagged-gateway-api-behavior)
* [Configuring sharding tags for Gravitee API Gateways](sharding-tags.md#configure-sharding-tags-for-your-gravitee-api-gateways)
* [Defining sharding tags for an organization](sharding-tags.md#define-sharding-tags-for-an-organization)
* [Adding sharding tags to an API](sharding-tags.md#add-sharding-tags-to-an-api)
* [Mapping entrypoints to sharding tags](sharding-tags.md#map-entrypoints-to-sharding-tags)

## Tagged Gateway/API behavior

API deployment is impacted by how tags are applied to APIs and Gateways.

### Rules

* Tagged Gateway instances will never deploy tagless APIs.
* Tagless Gateway instances will deploy every API, regardless of how the APIs are tagged.
* An API defined with a specific tag will only be deployed on a Gateway that has been assigned that tag.

### Examples

* A tagless API will not be deployed on a Gateway tagged with `x`.
* An API tagged with `x` will be deployed on a tagless Gateway.
* A tagless API will be deployed on a tagless Gateway.
* An API defined with tag `x` will be deployed on a Gateway that has been assigned tag `x`.
* An API defined with tag `x` will be deployed on a Gateway that has been assigned tag `!y`. The tag `!y` means that the Gateway has been assigned every tag but `y`.

## Configure sharding tags for your Gravitee API Gateways

Our discussion of sharding tag configuration assumes an architecture that includes both DMZ Gateways and internal, corporate Gateways. We want to tag these Gateways as external-only and internal-only, respectively, per the diagram below:

<figure><img src="../../4.0/.gitbook/assets/Example architecture (1).png" alt=""><figcaption></figcaption></figure>

Before sharding tags can be defined in the Gravitee API Management Console, the API Gateway `gravitee.yaml` file must be modified to assign a Gravitee API Gateway to a specific sharding tag:

```
DMZ Gateways: 
tags: ‘external’
```

```
Internal Network Gateways:
tags: ‘internal’
```

For example, if Gateways can be tagged as “external” and “partner," the below sharding tag definition configures a Gateway to host external APIs that are not dedicated to partners:

```
tags: ‘product,store,!partner’
```

Once Gateways have been tagged, these sharding tags must be defined within API Manager.

## Define sharding tags for an organization

Follow the steps below to add sharding tags to your organization.

1.  Log in to your API Management Console:

    <figure><img src="../../../../.gitbook/assets/v2 sharding tags_step 1.png" alt=""><figcaption></figcaption></figure>
2.  In the left-hand nav, select **Organization**:

    <figure><img src="../../../../.gitbook/assets/v2 sharding tags_step 2.png" alt=""><figcaption></figcaption></figure>
3.  On the **Organization** page, select **Sharding tags**:

    <figure><img src="../../../../.gitbook/assets/v2 sharding tags_step 3.png" alt=""><figcaption></figcaption></figure>
4.  Click **+ Add a tag**:

    <figure><img src="../../../../.gitbook/assets/v2 sharding tags_step 4.png" alt=""><figcaption></figcaption></figure>
5.  Create the same tags that you created in the `gravitee.yaml` file, ensuring the names are an exact match. For this example, let's first create the "internal" tag using the **Name** field:

    <figure><img src="../../../../.gitbook/assets/v2 sharding tags_step 5.png" alt=""><figcaption></figcaption></figure>
6.  (Optional) You can choose to restrict the usage of the tag to certain groups, as defined in Gravitee user administration

    <figure><img src="../../../../.gitbook/assets/v2 sharding tags_step 6.png" alt=""><figcaption></figcaption></figure>
7.  Click **Ok**:

    <figure><img src="../../../../.gitbook/assets/v2 sharding tags_step 7.png" alt=""><figcaption></figcaption></figure>
8.  Let's add the "external" tag, following the same steps:

    <figure><img src="../../../../.gitbook/assets/v2 sharding tags_step 8.png" alt=""><figcaption></figcaption></figure>

## Add sharding tags to an API

Follow the instructions below to add a sharding tag to a v2 API or a v4 API.

1. Log in to your API Management Console
2. Select **APIs** from the left nav
3. Choose the API you want to tag
4.  Select **Deployment** from the inner left nav:

    <figure><img src="../../../../.gitbook/assets/deployment_sharding tag.png" alt=""><figcaption></figcaption></figure>
5.  Select one or more tags from the **Sharding tags** drop-down menu, then click **Save**:

    <figure><img src="../../../../.gitbook/assets/deployment_sharding tag select.png" alt=""><figcaption></figcaption></figure>
6.  Click **Deploy API** to sync your API:

    <figure><img src="../../../../.gitbook/assets/deployment_sharding tag deploy.png" alt=""><figcaption></figcaption></figure>

## Map entrypoints to sharding tags

If you are using the Developer Portal, Gravitee also provides a way to map different entrypoint URLs to specific sharding tags. The Portal will display available entrypoints based on an API's tag(s).

{% hint style="info" %}
The following process applies to both v2 and v4 APIs.
{% endhint %}

To demonstrate, let's instruct Gravitee API Manager to apply the “internal test” tag to all APIs tagged with this entrypoint:

1. In your APIM console, select **Organization** from the left nav
2. Select **Sharding tags** from the new left nav
3.  Select **+ Add a mapping**:

    <figure><img src="../../../../.gitbook/assets/sharding tags map_step 3.png" alt=""><figcaption></figcaption></figure>
4.  In the **Entrypoint url** field, enter your Entrypoint URL:

    <figure><img src="../../../../.gitbook/assets/sharding tags map_step 4.png" alt=""><figcaption></figcaption></figure>
5.  In the **Sharding tags** drop-down menu, select the tag that you want mapped to your entrypoint. For this example, let's choose the "internal test" tag.

    <figure><img src="../../../../.gitbook/assets/sharding tags map_step 5.png" alt=""><figcaption></figcaption></figure>
6.  Click **Ok**:

    <figure><img src="../../../../.gitbook/assets/sharding tags map_step 6.png" alt=""><figcaption></figcaption></figure>
7.  You can view your entrypoint mapping in the **Entrypoint mappings** section:

    <figure><img src="../../4.0/.gitbook/assets/image (48) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
You've just learned how to configure sharding tags for your Gravitee API Gateways. To apply sharding tags to APIs in order to control where those APIs are deployed, refer to [this documentation](docs/apim/4.6/configure-v2-apis/proxy-settings.md).
{% endhint %}
