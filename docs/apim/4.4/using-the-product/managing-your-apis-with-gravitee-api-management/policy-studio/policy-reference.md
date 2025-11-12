---
description: Detailed documentation for all of Gravitee's policies
---

# Policy Reference

## Overview

Gravitee policies fall into the following functional categories:&#x20;

* Security
* Transformation
* Restrcitions&#x20;
* Performance&#x20;
* Routing&#x20;
* Monitoring and testing

&#x20;Although the implementation details of each policy are unique, they share a common installation and deployment, and they are compatible with subsets of phases.

{% hint style="info" %}
Policies cannot currently be applied to v4 TCP proxy APIs
{% endhint %}

## v2 APIs and v4 APIs policies support

v2 and v4 APIs support difference policies. The following table shows the differences in support for the following API types:

* v2 proxy APIs
* v4 proxy APIs
* v4 message APIs

### v2 APIs and v4 APIs support comparison for policies

{% tabs %}
{% tab title="A-C" %}
<table><thead><tr><th width="210">Policy</th><th>v2 proxy APIs</th><th>v4 proxy APis</th><th>v4 message APIs</th></tr></thead><tbody><tr><td><a href="policies-for-you-apis/a-c/api-key.md">API Key</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/a-c/assign-attributes.md">Assign Attributes</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/a-c/assign-content.md">Assign Content</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/a-c/assign-metrics.md">Assign Metrics</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/a-c/avro-to-json.md">AVRO to JSON</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/a-c/avro-to-protobuf.md">AVRO to Protobuf</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/a-c/aws-lambda.md">AWS Lambda</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td><td></td></tr><tr><td><a href="policies-for-you-apis/a-c/basic-authentication.md">Basic Authentication</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="../../../configuration/cache.md">Cache</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td><td></td></tr><tr><td><a href="policies-for-you-apis/a-c/circuit-breaker.md">Circuit Breaker</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td><td></td></tr><tr><td><a href="policies-for-you-apis/a-c/cloud-events.md">Cloud Events</a></td><td></td><td></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>Custom Query Parameters Parser</td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="D-H" %}
<table><thead><tr><th width="240">Policy</th><th>v2 proxy APIs</th><th width="137">v4 proxy APIs</th><th>v4 message APIs</th></tr></thead><tbody><tr><td><a href="policies-for-you-apis/d-h/data-logging-masking.md">Data Logging Masking</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td><td></td></tr><tr><td><a href="policies-for-you-apis/d-h/dynamic-routing.md">Dynamic Routing</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/d-h/generate-http-signature.md">Generate HTTP Signature</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/d-h/generate-jwt.md">Generate JWT</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/d-h/geoip-filtering.md">GeoIP Filtering</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/d-h/graphql-rate-limit.md">GraphQL Rate Limit</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/d-h/groovy.md">Groovy</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>HTML to JSON</td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/d-h/http-callout.md">HTTP Callout</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/d-h/http-signature.md">HTTP Signature</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="I-K" %}
<table><thead><tr><th width="221">Policy</th><th>v2 proxy APIs</th><th width="151">v4 proxy APIs</th><th>v4 message APIs</th></tr></thead><tbody><tr><td><a href="policies-for-you-apis/i-k/interrupt.md">Interrupt</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td>I<a href="policies-for-you-apis/i-k/ip-filtering.md">P Filtering</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/i-k/javascript.md">Javascript</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/i-k/json-to-xml.md">JSON to XML</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/i-k/json-threat-protection.md">JSON Threat Protection</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/i-k/json-validation.md">JSON Validation</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/i-k/json-web-signature-jws.md">JSON Web Signature</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/i-k/keyless.md">Keyless</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="L-O" %}
<table><thead><tr><th width="238">Policy</th><th>v2 proxy APIs</th><th width="138">v4 proxy APIs</th><th>v4 message APIs</th></tr></thead><tbody><tr><td><a href="policies-for-you-apis/l-p/latency.md">Latency</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/l-p/message-filtering.md">Message Filtering</a></td><td></td><td></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td>Metrics Reporter</td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td><td></td></tr><tr><td><a href="policies-for-you-apis/l-p/mock.md">Mock</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td><td></td></tr><tr><td>OAS Validation</td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/l-p/oauth2/">OAuth2</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/l-p/openid-connect-userinfo.md">OpenID Connect UserInfo</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/l-p/override-http-method.md">Override HTTP Method</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/l-p/protobuf-to-json.md">Protobuf to JSON</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr></tbody></table>
{% endtab %}

{% tab title="R-S" %}
<table><thead><tr><th width="246">Policy</th><th>v2 proxy APIs</th><th width="135">v4 proxy APIs</th><th>v4 message APIs</th></tr></thead><tbody><tr><td><a href="policies-for-you-apis/r-s/rate-limit.md">Rate Limit</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/r-s/regex-threat-protection.md">Regex Threat Protection</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/r-s/request-content-limit.md">Request Content Limit</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/r-s/request-validation.md">Request Validation</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td>Resource Validation</td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/r-s/resource-filtering.md">Resource Filtering</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/r-s/rest-to-soap.md">REST to SOAP</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/r-s/retry.md">Retry</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td><td></td></tr><tr><td><a href="policies-for-you-apis/r-s/role-based-access-control-rbac.md">Role-based Access Control</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/r-s/ssl-enforcement.md">SSL Enforcement</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="T-Z" %}
<table><thead><tr><th width="237">Policy</th><th>v2 proxy APIs</th><th width="135">v4 proxy APIs</th><th>v4 message APIs</th></tr></thead><tbody><tr><td>Transform Shadowing</td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td><td></td></tr><tr><td><a href="policies-for-you-apis/t-x/transform-headers.md">Transform Headers</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/t-x/transform-query-parameters.md">Transform Query Params</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td>URL Rewriting</td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/t-x/ws-security-authentication.md">WS Security Authentication</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/t-x/xml-to-json.md">XML to JSON</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td><a href="policies-for-you-apis/t-x/xml-threat-protection.md">XML Threat Protection</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/t-x/xml-validation.md">XML Validation</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr><tr><td><a href="policies-for-you-apis/t-x/xslt.md">XSLT</a></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td></td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Installation and deployment

Each version of Gravitee API Management (APIM) includes a number of policies in the default distribution. [Gravitee Enterprise Edition policy plugins](../../../overview/gravitee-apim-enterprise-edition/#enterprise-plugins) are available for download [here](https://download.gravitee.io/).

To use a different version of the policy or add a custom policy, you can follow the deployment instructions below.

<details>

<summary>How to deploy a plugin</summary>

Please check the policy documentation to ensure the policy version you select is compatible with your version of APIM.

To deploy the plugin, follow these steps:

1. Download the plugin archive (a `.zip` file) from [the plugins download page](https://download.gravitee.io/#graviteeio-apim/plugins/).
2. Add the file into the Gateway and Management API `plugins` folders. The default location is ${GRAVITEE\_HOME/plugins} but this can be modified in [the `gravitee.yaml` file.](../../using-the-gravitee-api-management-components/general-configuration/#configure-the-plugins-repository) For most installations, the Gateway and Management API `plugins` folders are at `/gravitee/apim-gateway/plugins` and `/gravitee/apim-management-api/plugins`, respectively.
3. Restart your APIM nodes.

</details>

## Configuration

Policies can be added to flows that are assigned to an API or to a [plan](../api-exposure-plans-applications-and-subscriptions/plans.md). Gravitee supports configuring policies [through the Policy Studio](./) in the Management Console or interacting directly with the Management API.

## Phases

Policies can be applied to the request or the response of a Gateway API transaction, which are broken up into phases that depend on the API definition version. Each policy is compatible with a subset of the available phases.

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
