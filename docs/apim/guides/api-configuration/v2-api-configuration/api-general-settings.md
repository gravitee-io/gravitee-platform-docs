---
description: >-
  This article walks through how to understand and edit your API's general
  settings
---

# API General settings

## Introduction

Every API in Gravitee has General settings that can be viewed and altered in the **Portal** section of your API's settings.

## Understanding and editing your API's general settings

Your API's General page is comprised of three main areas:

* **General details**
  * Name&#x20;
  * Description
  * API picture
  * API background
  * Owner and creation information
  * The ability to export your API definition, import a new API definition to update your API, duplicate your API, and promote your API
* **API Quality**: This section describes how well your API conforms to set API quality rules. For more information on the Gravitee API Quality feature, please refer to the [API Quality documentation](../../api-measurement-tracking-and-analytics/using-the-api-quality-feature.md).&#x20;
* **Danger zone:** this section includes access to mission-critical (and potentially dangerous) actions:
  * **Start the API**: this will deploy the API to all Gateways, or the Gateways specified using [Sharding tags](../../../getting-started/configuration/configure-sharding-tags-for-your-gravitee-api-gateways.md)
  * **Publish the API**: this will publish the API to the Developer Portal
  * **Make Public**: this will make the API public so that everybody can see it
  * **Delete**: this will delete the API

Any time you make a change to your API, you will need to select the **Save** icon at the bottom of the screen.
