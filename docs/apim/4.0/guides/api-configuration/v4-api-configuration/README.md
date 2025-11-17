---
description: This section covers concepts and how-to's for configuring v4 APIs in Gravitee.
---

# v4 API Configuration

{% hint style="info" %}
**v4 vs v2 API configuration**

This section covers v4 API configuration. If you want to learn how to configure v2 APIs, please refer to the [v2 API configuration section](../v2-api-configuration/README.md).
{% endhint %}

## Introduction

Gravitee offers several levels of configuration for v4 APIs using the Gravitee APIM Console. In this section, we'll cover:

* Portal configuration
  * **General settings**: define the general settings for your API, such as name, description, and deployment status
  * **Plans configuration**: define plans and basic access control mechanisms
* Entrypoints
  * **General entrypoint configuration**: configure how consumers access the Gateway through your Gateway API
* Endpoints
  * **Backend service configuration**: configure the backend target or resource that your Gateway API will call/subscribe to

{% hint style="info" %}
**Quality of Service**

You can also configure Quality of Service levels and settings for certain v4 APIs. However, this is NOT yet supported in Gravitee APIM Console as of Gravotee APIM 4.0. However, given the importance of QoS, we have still [included an article that walks through how to understand and configure QoS for v4 APIs using the API definition](quality-of-service.md).
{% endhint %}
