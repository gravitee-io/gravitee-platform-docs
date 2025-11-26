---
description: >-
  This article walks through how to create APIs using the Gravitee v2 API
  definition
---

# Creating APIs with the v2 API creation wizard

## Introduction

In Gravitee, your API definition is a JSON representation of your Gateway API. The v2 API definition supports HTTP-based APIs and the legacy version of the Policy Studio. This article describes how to create APIs in Gravitee using the v2 API creation wizard.

## Access the API creation wizard

To create a v2 API in Gravitee:

1. Log in to your APIM Console
2. Select **APIs** tab from the left nav
3. Click **+ Add API** in the top right corner of the UI
4. Choose **Create a v2 API from scratch** to enter the API creation wizard for v2 APIs

## Step 1: General

The first step is to define your API's general details. Give your API a:

* Name
* Version
* Description
* Context path: This is the path where the API is exposed

Optionally, you can select the **Advanced mode** hyperlink in the top right corner of the **General** page. This allows you to define:

* Whether to use a group as the primary owner of the API
* (Optional) The primary owner group
* (Optional) A list of groups that will have access to, but not own, the API

## Step 2: Gateway

Define your **Backend**, which is the target backend where the request will be received.

Optionally, you can select **Advanced mode** to define **Tenants** and/or **Sharding tags** for this API. These specify the Gateways to which the API is deployed.

{% hint style="info" %}
Refer to [Tenants](../../../using-the-gravitee-api-management-components/general-configuration/tenants.md) and/or [Sharding tags](../../../using-the-gravitee-api-management-components/general-configuration/sharding-tags.md) for more information.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.35.16 PM.png" alt=""><figcaption><p>Define your API Gateway settings</p></figcaption></figure>

## Step 3: Plan

A plans is an access layer around an API that provides the API producer with a method to secure, monitor, and transparently communicate details related to access. That this step is optional.

The API creation wizard allows you to create either an **API key** or **Keyless** plan for your API. Once you choose your plan type and give it a name and description, you will have the option of adding:

* A **rate limit:** Sets the maximum number of API requests that may occur during the specified number of seconds or minutes
* A **quota**: Sets the maximum number of API requests that may occur during the specified number of hours, days, weeks, or months
* **Resource filtering**: Allows you to filter resources based on whitelists and blacklists

<figure><img src="../../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.43.11 PM.png" alt=""><figcaption><p>v2 API creation wizard: Plans</p></figcaption></figure>

Gravitee offers additional plan features that are not configured in the API creation wizard. For more in-depth information on plans, refer to the [plans documentation](../../api-exposure-plans-applications-and-subscriptions/plans.md).

Once you have defined your plan, click **NEXT**.

## Step 4: Documentation

On the **Documentation** page you can upload your API's documentation as a file. Creating documentation is optional.

<figure><img src="../../../../.gitbook/assets/Screen Shot 2023-06-07 at 1.43.58 PM.png" alt=""><figcaption><p>v2 API creation wizard: Documentation</p></figcaption></figure>

## Step 5: Deployment

On the **Deployment** page, you will see a summary of your API and can choose how you want to create it:

* **Create without deploying the API:** Creates the API as an artifact in Gravitee, without deploying the API to the Gateway. You can access, configure, and design policies for the API.
* **Create and deploy the API:** Creates the API in Gravitee and deploys it to the Gateway. You can access, configure, and design policies for the API, but must redeploy it after making changes.
