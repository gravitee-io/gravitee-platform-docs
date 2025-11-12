---
description: >-
  This article walks through how to understand and edit your v4 API's general
  settings
---

# General Info Settings

## Introduction

Every v4 API in Gravitee has general settings that can be viewed and altered on the **Configuration** page.

{% hint style="info" %}
The settings configuration is the same for both v2 and v4 APIs, with the exception of the API Quality section. As of Gravitee APIM 4.3, only v2 APIs support the API Quality feature.
{% endhint %}

## General settings

To access your API's general settings:

1. Log in to your APIM Console
2. Click on **APIs** in the left nav
3. Select your API
4. Click on **Configuration** in the inner left nav
5. Click on the **General** tab, which is split into two main sections:

The **Configuration** page shows two main areas under the **General** tab:

{% tabs %}
{% tab title="General details" %}
* Name
* Version
* Description
* Labels
* Categories
* API picture
* API background
* Owner, creation, and connection information
* The ability to export your API definition, import a new API definition to update your API, duplicate your API, and promote your API
{% endtab %}

{% tab title="Danger zone" %}
This section includes access to mission-critical (and potentially dangerous) actions:

* **Start the API:** Deploy the API to all Gateways, or the Gateways specified using [Sharding tags](docs/apim/4.4/using-the-product/using-the-gravitee-api-management-components/general-configuration/sharding-tags.md)
* **Publish the API:** Publish the API to the Developer Portal
* **Make Public:** Make the API public so that everybody can see it
* **Deprecate:** Unpublish the API from the Developer Portal
* **Delete:** Delete the API
{% endtab %}
{% endtabs %}

Any time you make a change to your API, click the **Save** icon at the bottom of the screen.
