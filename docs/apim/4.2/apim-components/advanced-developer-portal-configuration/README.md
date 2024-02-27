---
description: The administrator's guide to the Developer Portal
---

# Configuration

## Introduction

The Developer Portal is a web application that provides a simplified, user-friendly interface tailored to the API consumption process. It acts as a centralized catalog where internal and external API consumers can find and subscribe to APIs that are developed, managed, and deployed by API publishers.

While most features in the Developer Portal are also available in the Management Console (see the [API Exposure guide](broken-reference)), the Developer Portal allows API consumers to easily discover and explore APIs, read documentation, test API endpoints, generate API keys, view API analytics, and manage their API subscriptions in a single location. Additionally, administrators have significantly more control over the look and feel of the Developer Portal to deliver an accessible and on-brand experience to external API consumers.

This documentation is intended to provide a detailed overview of the Developer Portal's features and functionality, as well as step-by-step instructions for how to use them.

## Access the Developer Portal

The Developer Portal is configured from **Settings** in the Management Console:

<figure><img src="../../.gitbook/assets/dev_portal_settings.png" alt=""><figcaption><p>Developer portal settings</p></figcaption></figure>

## Configuration file

The configuration file for APIM Portal is `assets\config.json`. The default configuration is included below:

{% code title="config.json" %}
```json
{
  "baseURL": "/portal/environments/DEFAULT",
  "homepage": {
    "featured": {
      "size": 9
    }
  },
  "loaderURL": "assets/images/gravitee-loader.gif",
  "pagination": {
    "size": {
      "default": 10,
      "values": [5, 10, 25, 50, 100]
    }
  }
}
```
{% endcode %}

The only mandatory value in `config.json` file is `baseURL`, which describes the location of the APIM API Portal endpoint. You must set this value for APIM Portal to send requests to the endpoint.
