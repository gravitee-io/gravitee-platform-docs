# Gravitee Gateway

## Overview

This guide will walk through how to configure your general Gravitee API Management (APIM) Gateway settings using the `gravitee.yaml` file. As described in [APIM Components](services.md), you can override these settings by using system properties or environment variables.

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

## Default `gravitee.yaml` config file

The following is a reference of the default configuration of APIM Gateway in your `gravitee.yml` file:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml" %}
