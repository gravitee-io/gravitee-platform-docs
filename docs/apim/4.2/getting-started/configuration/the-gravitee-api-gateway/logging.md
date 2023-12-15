---
description: This article describes how to configure logging at the API Gateway level
---

# Logging

## Introduction

Gravitee allows you to capture logs at both the API and Gateway levels. This article describes how to configure logging at the API Gateway level.

{% hint style="info" %}
**API logging**

If you want to configure logs at the API level, please refer to the [Configure and Use API Logging documentation](../../../guides/api-measurement-tracking-and-analytics/configure-and-use-api-logging.md).
{% endhint %}

## Configure logging at the Gateway level

To configure logging permissions and settings at the Gateway level:

1. Select **Settings** from the left sidebar of the Management Console
2. Select **API Logging** from the inner left sidebar

<figure><img src="../../../.gitbook/assets/2023-06-28_10-39-47 (1).gif" alt=""><figcaption></figcaption></figure>

You can choose to enable:

* Auditing API Logging consultation
* End user information displayed as part of API logging (this is useful if you are using an OAuth2 or JWT plan)
* Generation of API logging as audit events (API\_LOGGING\_ENABLED, API\_LOGGING\_DISABLED, API\_LOGGING\_UPDATED)

You can also define the maximum duration (in ms) of logging mode activation by entering a numeric value in the **Maximum duration** text field.
