---
description: This article walks through how to configure logging at the API Gateway level
---

# Logging

## Introduction

Gravitee enables you to capture logs at both the API and Gateway levels. This article walks through how to configure logging at the API Gateway level.

{% hint style="info" %}
**API logging**

If you want to configure logs at the API level, please refer to the [Configure and Use API Logging documentation](../../../guides/api-measurement-tracking-and-analytics/configure-and-use-api-logging.md).
{% endhint %}

## Configure logging at the Gateway level

You can configure logging permissions and settings at the Gateway level. To do this, select Settings in the far left-hand nav. Then, within the Settings menu, select **API Logging** underneath the **Gateway** section of your settings.&#x20;

<figure><img src="../../../.gitbook/assets/2023-06-28_10-39-47 (1).gif" alt=""><figcaption></figcaption></figure>

From here, you can choose to enable:

* Auditing API Logging consultation
* The display of end user information in your API logging (this is useful for when you are using OAuth2 or JWT plans)
* Generation of API logging as audit events (API\_LOGGING\_ENABLED, API\_LOGGING\_DISABLED, API\_LOGGING\_UPDATED)

You can also define the maximum duration (in ms) for the activation of logging mode by entering in a numerical value in the **Maximum duration** text field.

