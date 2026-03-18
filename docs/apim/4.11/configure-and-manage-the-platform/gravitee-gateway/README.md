---
description: An overview about gravitee gateway.
---

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

## MDC Filtering

Configure which MDC keys appear in log output and how they are formatted.

| Property | Type | Default (Gateway) | Default (REST API) | Description |
|:---------|:-----|:------------------|:-------------------|:------------|
| `node.logging.mdc.format` | String | `"{key}: {value}"` | `"{key}: {value}"` | MDC key-value format pattern |
| `node.logging.mdc.separator` | String | `" "` | `" "` | Separator between MDC entries |
| `node.logging.mdc.nullValue` | String | `"-"` | `"-"` | Value displayed when MDC entry is null |
| `node.logging.mdc.include` | List\<String> | `["nodeId", "apiId"]` | `["nodeId", "envId", "apiId", "appId"]` | MDC keys to include in log output |

## Pattern Override

Override logback.xml encoder patterns at runtime without modifying the XML file. When enabled, the infrastructure walks the appender tree and replaces console and file patterns with values from `gravitee.yml`.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.pattern.overrideLogbackXml` | Boolean | `true` | Whether to override logback.xml patterns at runtime |
| `node.logging.pattern.console` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | Console log pattern when override is enabled |
| `node.logging.pattern.file` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | File log pattern when override is enabled |


