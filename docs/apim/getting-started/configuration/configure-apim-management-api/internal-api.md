---
description: >-
  Configure the Gravitee APIM Management API with environment variables, system
  properties, and the gravitee.yaml file
---

# General Configuration

## Introduction

This guide will walk through how to configure your general Gravitee APIM Management API settings using the `gravitee.yaml` file. As detailed in the [Configuring APIM Components](../#configuring-apim-components), you can override these settings by using system properties or environment variables

## The `gravitee.yaml` file

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

With the  `gravitee.yaml` file, you can configure the following:
