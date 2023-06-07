---
description: >-
  This article walks through how to create APIs using the Gravitee v2API
  defintion
---

# V2 API definition creation wizard

{% @arcade/embed flowId="kApsIRtoWrfIFRzd7DQj" url="https://app.arcade.software/share/kApsIRtoWrfIFRzd7DQj" fullWidth="true" %}

## Introduction

In Gravitee, your API definition is a JSON representation of your Gateway API. Gravitee currently supports two different API definitions: v2 and v4. API definition v2 supports HTTP-based APIs and will only allow you to use the legacy version of the Policy Studio. This article walks through how to create APIs in Gravitee using the v2 API creation wizard.

## Access the API creation wizard

To create a v2 API in Gravitee, select the **APIs** tab in the left-hand nav. Then, select **+ Add API** in the top-right corner of the UI.&#x20;

Choose Create a v2 API from scratch. You'll then be brought into the API creation wizard for v2 APIs.

## Step 1: General

The first step is to define your API's general details. Give your API a:

* Name
* Version
* Description
* Context path: this is just the path where the API is exposed

Optionally, you use the Advanced mode by selecting the Advanced mode hyperlink in the top right corner of the General page. This will enable you to define whether or not to use a group as the primary owner of the API, define that primary owner group, and then also optionally define a list of groups that will have access to, but not own, that API.&#x20;

## Step 2: Gateway

Here, all you'll need to do is define your Backend, which is essentially the target backend where the request will be received.&#x20;

Optionally, you can select Advanced mode to define Tenants and/or Sharding tags for this API. These will define which Gateways to deploy this API to. For more information, please refer to the [Tenants](../../../getting-started/configuration/the-gravitee-api-gateway/tenants.md) and/or [Sharding tags](../../../getting-started/configuration/configure-sharding-tags-for-your-gravitee-api-gateways.md) documentation.&#x20;

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.35.16 PM.png" alt=""><figcaption><p>Define your APIs Gateway settings</p></figcaption></figure>

## Step 3: Plan

Step 3 is all about defining plans. Plans are an access layer around APIs that provide the API producer a method to secure, monitor, and transparently communicate details around access. Please note that this step is optional. If you do not want to implement a plan at this time, you can select Skip. Otherwise, please continue reading below.

The API creation wizard allows you to create either an **API key** or **Keyless** plan for your API. Once you choose your plan type and give it a name and description, you will have the option of adding:

* A **rate limit:** this sets a maximum number of API requests across a given amount of either seconds or minutes
* A **quota**: this sets a maximum number of API requests across a given amount of hours, days, weeks, or months.
* **Resource filtering**: this allows you to filter resources based on whitelists and blacklists.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.43.11 PM.png" alt=""><figcaption><p>v2 API creation wizard: plans</p></figcaption></figure>

Gravitee does offer more features around Plans, but further Plan configuration is not handled in the API creation wizard. For more in-depth information on Plans, please refer to the [Plans documentation. ](../../api-exposure-plans-applications-and-subscriptions/plans.md)

Once you are done defining your plan, select **Next.**

## Step 4: Documentation

{% hint style="info" %}
Currently, only the v2 API definition allows you to upload API documentation as a part of the API creation wizard.
{% endhint %}

On the **Documentation** page, you can upload your APIs documentation as a file, or, you can select **Skip** to continue without uploading API documentation.&#x20;

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.43.58 PM.png" alt=""><figcaption><p>v2 API creation wizard: documentation</p></figcaption></figure>

## Step 5: Deployment

On the Deployment page, you'll see a summary of your API, and you'll choose how you want to create it:

* **Create without deplpoying the API:** this creates the API as an artifact in Gravitee, without deploying the API to the Gateway. This will allow you to access the API via the APIs list, configure the API, and design policies for the API using the v2 Policy Design studio.
* **Create and deploy the API:** this will create the API in Gravitee _and_ deploy it to the Gateway. You can still access the API in the APIs list, configure the API, and design policies for the API using the v2 Policy Design Studio, but you will then have to redeploy that API after making changes.

{% hint style="info" %}
After you've chosen your creation method, you will have finished creating APIs using the v2 API creation wizard. From here, we recommend learning more about [API configuration](../../api-configuration/) and the Policy Design Studio.
{% endhint %}
