---
description: This section covers concepts and how-to's for configuring v4 APIs in Gravitee.
---

# v4 API Configuration

{% hint style="info" %}
**v4 vs v2 API configuration**

This section covers v4 API configuration. If you want to learn how to configure v2 APIs, please refer to the [v2 API configuration section](../v2-api-configuration/README.md).
{% endhint %}

{% hint style="warning" %}
In Gravitee 4.2, the API Management Console cannot be used to configure a TCP proxy API. To configure TCP proxy APIs, you must use the Management API and curl commands.
{% endhint %}

## Introduction

Gravitee offers various configuration for v4 APIs via the Gravitee APIM Console. This article discusses:

* Portal configuration
  * **General settings**: Define the general settings for your API, such as name, description, and deployment status.
  * **Plan configuration**: Define plans and basic access control mechanisms.
* Entrypoints
  * **General entrypoint configuration**: Configure how consumers access the Gateway through your Gateway API.
* Endpoints
  * **Backend service configuration**: Configure the backend target or resource that your Gateway API will call / subscribe to.

{% hint style="info" %}
**Quality of Service**

Gravitee APIM Console does not yet support Quality of Service configuration. [This article](quality-of-service.md) addresses QoS configuration for v4 APIs using the API definition.
{% endhint %}
