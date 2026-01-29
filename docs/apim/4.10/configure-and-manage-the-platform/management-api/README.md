---
description: An overview about management api.
metaLinks:
  alternates:
    - ./
---

# Management API

## Overview

You can configure your general Gravitee APIM Management API settings using the `gravitee.yaml` file. As detailed in [APIM Components](./), you can override these settings by using system properties or environment variables.

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

## Default `gravitee.yaml` config file

The following is a reference of the default configuration of APIM Management API in your `gravitee.yml` file:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-rest-api/gravitee-apim-rest-api-standalone/gravitee-apim-rest-api-standalone-distribution/src/main/resources/config/gravitee.yml" %}
