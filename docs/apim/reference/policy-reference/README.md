---
description: Discover how policies secure, transform, restrict, and monitor your APIs
---

# Policy Reference

## Overview

Gravitee policies fall into several functional categories: security, transformation, restrictions, performance, routing, and monitoring & testing. Although the implementation details of each policy are unique, they share a common installation and deployment and are compatible with subsets of phases.

## Installation and deployment

Each version of APIM includes a number of policies by default. If you would like to use a different version of the policy, you can modify the plugin.

<details>

<summary>How to modify the plugin</summary>

Please ensure the policy version you select is compatible with your version of APIM.

To modify the plugin, follow these steps:

1. Download the plugin archive (a `.zip` file) from [the plugins download page](https://download.gravitee.io/#graviteeio-apim/plugins/).
2. Add the file into the Gateway and Management API `plugins` folders. The default location is ${GRAVITEE\_HOME/plugins} but this can be modified in [the `gravitee.yaml` file.](../../getting-started/configuration/the-gravitee-api-gateway/environment-variables-system-properties-and-the-gravitee.yaml-file.md#configure-the-plugins-repository) For most installations, the Gateway and Management API `plugins` folders are at `/gravitee/apim-gateway/plugins`  and `/gravitee/apim-management-api/plugins`, respectively.
3. Remove any existing plugins of the same name.
4. Restart your APIM nodes.

</details>

{% hint style="warning" %}
Please ensure the policy version you select is compatible with your version of APIM.
{% endhint %}

## Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy has different compatibility with the available phases as described in the [Policy Studio documentation](../../guides/policy-design/).

{% tabs %}
{% tab title="v4 API definition" %}
v4 APIs have the following phases:

* `onRequest`: This phase is executed before invoking the backend services for both proxy and message APIs. Policies can act on the headers and the content for proxy APIs.
* `onMessageRequest`: This phase occurs after the `onRequest` phase and allows policies to act on each incoming message before being sent to the backend service. This only applies to message APIs.
* `onResponse`: This phase is executed after invoking the backend services for both proxy and message APIs. Policies can act on the headers and the content for proxy APIs.
* `onMessageResponse`: This phase after the `onResponse` phase and allows policies to act on each outgoing message before being sent to the client application. This only applies to message APIs.
{% endtab %}

{% tab title="v2 API definition" %}
v2 APIs have the following phases:

* `onRequest`: This phase only allows policies to work on request headers. It never accesses the request body.
* `onRequestContent`: This phase always occurs after the `onRequest` phase. It allows policies to work at the content level and access the request body.
* `onResponse`: This phase only allows policies to work on response headers. It never accesses the response body.
* `onResponseContent`: This phase always occurs after the `onResponse` phase. It allows policies to work at the content level and access the response body.
{% endtab %}
{% endtabs %}

## Related learning

For details of how policies are defined and used in APIM, see also:

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>API Exposure: Plans, Applications, &#x26; Subscriptions</strong></td><td></td><td>Learn how to configure policies for API plans in APIM Console</td><td><a href="../../guides/api-exposure-plans-applications-and-subscriptions/">api-exposure-plans-applications-and-subscriptions</a></td></tr><tr><td><strong>Gravitee Expression Language</strong></td><td></td><td>Learn more about using the Gravitee Expression Language with policies</td><td><a href="../../guides/policy-design/gravitee-expression-language.md">gravitee-expression-language.md</a></td></tr><tr><td><strong>Developer Contributions</strong></td><td></td><td>Learn how to create custom policies and deploy plugins (of which policies are one type)</td><td><a href="../../guides/developer-contributions/">developer-contributions</a></td></tr></tbody></table>
