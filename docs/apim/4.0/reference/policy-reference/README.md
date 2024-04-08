---
description: Detailed documentation for all of Gravitee's policies
---

# Policy Reference

## Overview

Gravitee policies fall into several functional categories: security, transformation, restrictions, performance, routing, and monitoring & testing. Although the implementation details of each policy are unique, they share a common installation and deployment and are compatible with subsets of phases.

## Installation and deployment

Each version of Gravitee API Management (APIM) includes a number of policies in the default distribution. [Gravitee Enterprise Edition](../../overview/ee-vs-oss/) policy plugins are available for download [here](https://download.gravitee.io/).

EE plugins are installed from their respective repositories in GitHub. Gravitee’s EE plugin repositories are private and their names are prefixed as `gravitee-io/gravitee-policy-<plugin-name>`. For example, the Data Logging Masking Policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`. If you have not been granted access to private EE plugin repositories as part of your EE license request process, email [contact@graviteesource.com](mailto:contact@graviteesource.com).

If you would like to use a different version of the policy or add a custom policy, you can follow the deployment instructions below.

<details>

<summary>How to deploy a plugin</summary>

Please check the policy documentation to ensure the policy version you select is compatible with your version of APIM.

To deploy the plugin, follow these steps:

1. Download the plugin archive (a `.zip` file) from [the plugins download page](https://download.gravitee.io/#graviteeio-apim/plugins/).
2. Add the file into the Gateway and Management API `plugins` folders. The default location is ${GRAVITEE\_HOME/plugins} but this can be modified in [the `gravitee.yaml` file.](../../getting-started/configuration/configure-apim-gateway/general-configuration.md#configure-the-plugins-repository) For most installations, the Gateway and Management API `plugins` folders are at `/gravitee/apim-gateway/plugins` and `/gravitee/apim-management-api/plugins`, respectively.
3. Restart your APIM nodes.

</details>

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-studio/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference.md)

## Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines/). Each policy is compatible with a subset of the available phases. Refer to an individual policy's documentation for phase support information.

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

## Compatibility matrices

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The documentation for each policy includes the compatibility matrix for APIM and that particular policy.

## Related learning

For details of how policies are defined and used in APIM, see also:

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>API Exposure: Plans, Applications, &#x26; Subscriptions</strong></td><td></td><td>Learn how to configure policies for API plans in APIM Console</td><td><a href="../../guides/api-exposure-plans-applications-and-subscriptions/">api-exposure-plans-applications-and-subscriptions</a></td></tr><tr><td><strong>Gravitee Expression Language</strong></td><td></td><td>Learn more about using the Gravitee Expression Language with policies</td><td><a href="../../guides/gravitee-expression-language.md">gravitee-expression-language.md</a></td></tr><tr><td><strong>Developer Contributions</strong></td><td></td><td>Learn how to create custom policies and deploy plugins (of which policies are one type)</td><td><a href="../../guides/developer-contributions/">developer-contributions</a></td></tr></tbody></table>
