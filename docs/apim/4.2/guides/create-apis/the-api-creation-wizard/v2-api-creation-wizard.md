---
description: >-
  This article walks through how to create APIs using the Gravitee v2 API
  definition
---

# v2 API creation wizard

## Introduction

In Gravitee, your API definition is a JSON representation of your Gateway API. API definition v2 supports HTTP-based APIs and the legacy version of the Policy Studio. This article walks through how to create APIs in Gravitee using the v2 API creation wizard.

## Access the API creation wizard

To create a v2 API in Gravitee, select the **APIs** tab in the lefthand nav. Then, select **+ Add API** in the top right corner of the UI.

Choose Create a v2 API from scratch to enter the API creation wizard for v2 APIs.

## Step 1: General

The first step is to define your API's general details. Give your API a:

* Name
* Version
* Description
* Context path: this is the path where the API is exposed

Optionally, you can use the Advanced mode by selecting the Advanced mode hyperlink in the top right corner of the General page. This allows you to define:

* Whether to use a group as the primary owner of the API
* (Optional) the primary owner group
* (Optional) A list of groups that will have access to, but not own, the API

## Step 2: Gateway

In this step you will define your Backend, which is the target backend where the request will be received.

Optionally, you can select Advanced mode to define Tenants and/or Sharding tags for this API. These define the Gateways to which the API is deployed. For more information, please refer to the [Tenants](../../../getting-started/configuration/the-gravitee-api-gateway/tenants.md) and/or [Sharding tags](../../../getting-started/configuration/the-gravitee-api-gateway/sharding-tags.md) documentation.

<figure><img src="../../../../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.35.16 PM (1).png" alt=""><figcaption><p>Define your APIs Gateway settings</p></figcaption></figure>

## Step 3: Plan

Step 3 is all about defining plans. Plans are an access layer around APIs that provide the API producer with a method to secure, monitor, and transparently communicate details surrounding access. Please note that this step is optional. If you do not want to implement a plan at this time, you can select Skip. Otherwise, please continue reading below.

The API creation wizard allows you to create either an **API key** or **Keyless** plan for your API. Once you choose your plan type and give it a name and description, you will have the option of adding:

* A **rate limit:** this sets the maximum number of API requests that may occur during the specified number of seconds or minutes.
* A **quota**: this sets the maximum number of API requests that may occur during the specified number of hours, days, weeks, or months.
* **Resource filtering**: this allows you to filter resources based on whitelists and blacklists.

<figure><img src="../../../../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.43.11 PM (1).png" alt=""><figcaption><p>v2 API creation wizard: plans</p></figcaption></figure>

Gravitee offers additional plan features, but these are not configured in the API creation wizard. For more in-depth information on plans, please refer to the [plans documentation](../../api-exposure-plans-applications-and-subscriptions/plans.md).

Once you have defined your plan, select Next\*\*.\*\*

## Step 4: Documentation

{% hint style="info" %}
Currently, only the v2 API definition allows you to upload API documentation as a part of the API creation wizard.
{% endhint %}

On the Documentation page, you can either upload your API's documentation as a file or select Skip to continue without uploading API documentation.

<figure><img src="../../../../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.43.58 PM (1).png" alt=""><figcaption><p>v2 API creation wizard: documentation</p></figcaption></figure>

## Step 5: Deployment

On the Deployment page, you will see a summary of your API and can choose how you want to create it:

* **Create without deploying the API:** this creates the API as an artifact in Gravitee, without deploying the API to the Gateway. It allows you to access the API via the APIs list, configure the API, and design policies for the API using the v2 Policy Studio.
* **Create and deploy the API:** this creates the API in Gravitee _and_ deploys it to the Gateway. You can still access the API in the APIs list, configure the API, and design policies for the API using the v2 Policy Studio, but you will then have to redeploy that API after making changes.

{% hint style="info" %}
After you've chosen your creation method, you will have finished creating APIs using the v2 API creation wizard. From here, we recommend learning more about [API configuration](../../api-configuration/README.md) and the Policy Studio.
{% endhint %}
