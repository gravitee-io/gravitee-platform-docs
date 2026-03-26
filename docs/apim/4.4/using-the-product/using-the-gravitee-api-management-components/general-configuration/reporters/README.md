---
description: An overview about Reporters.
---

# Reporters

## Overview

Reporters are designed to record a variety of events occurring in the Gravitee API Management (APIM) Gateway and output them to a new source in their order of occurrence. This enables you to manage your data using a solution of your choice.

The following sections detail:

* [Supported event types](README.md#event-types)
* [Available reporters](README.md#available-reporters)
* [Reporter configurations](README.md#configuring-reporters)

## Event types

The following event types are supported:

<table><thead><tr><th width="214.5">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>request</code></td><td>This event type provides common request and response metrics, such as response time, application, request ID, and more.</td></tr><tr><td><code>log</code></td><td>This event type provides more detailed request and response metrics. It is reported when logging has been enabled at the API level.</td></tr><tr><td><code>health-check</code></td><td>This event type allows for health-check events to be reported when a health-check endpoint has been configured and enabled on an API.</td></tr><tr><td><code>node</code></td><td>This event type provides some system and JVM metrics for the node Gravitee is running on.</td></tr></tbody></table>

## Available reporters

The following reporters are currently compatible with APIM:

<table><thead><tr><th width="151">Type</th><th data-type="checkbox">Bundled in Distribution</th><th data-type="checkbox">Default</th><th data-type="checkbox">Enterprise only</th></tr></thead><tbody><tr><td><a href="./#elasticsearch-reporter">Elasticsearch</a></td><td>true</td><td>true</td><td>false</td></tr><tr><td><a href="./#file-reporter">File</a></td><td>true</td><td>false</td><td>false</td></tr><tr><td><a href="./#tcp-reporter">TCP</a></td><td>true</td><td>false</td><td>true</td></tr><tr><td><a href="./#datadog-reporter">Datadog</a></td><td>false</td><td>false</td><td>true</td></tr></tbody></table>

{% hint style="warning" %}
To learn more about Gravitee Enterprise and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../../overview/gravitee-apim-enterprise-edition/README.md)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}
