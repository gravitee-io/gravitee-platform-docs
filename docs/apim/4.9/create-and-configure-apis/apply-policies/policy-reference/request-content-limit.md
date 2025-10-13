# Request Content Limit

## Overview

You can use the `request-content-limit` policy to specify a maximum request content length allowed. This limit is compared to the content length header of the request.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
```json
"request-content-limit": {
  "limit": 1000
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `request-content-limit` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="129" data-type="checkbox">Compatible?</th><th width="196.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `request-content-limit` policy can be configured with the following options:

<table><thead><tr><th width="119">Property</th><th width="106" data-type="checkbox">Required</th><th width="237">Description</th><th>Type</th></tr></thead><tbody><tr><td>limit</td><td>true</td><td>Maximum length of request content allowed</td><td>int</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `request-content-limit` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="195.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>400</code></td><td>The limit from the configuration is not correct.</td></tr><tr><td><code>413</code></td><td>Incoming HTTP request payload exceed the size limit.</td></tr><tr><td><code>411</code></td><td>The HTTP request is not chunked and does not specify the <code>Content-Length</code> header.</td></tr></tbody></table>

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

Some possible responses are:

<table><thead><tr><th width="145.5">Error</th><th>description</th></tr></thead><tbody><tr><td>400</td><td>Content-length is not a valid integer.</td></tr><tr><td>411</td><td>The request did not specify the length of its content, which is required by the requested resource.</td></tr><tr><td>413</td><td>The request is larger than the server is willing or able to process.</td></tr></tbody></table>

The error keys sent by this policy are as follows:

<table><thead><tr><th width="424.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>REQUEST_CONTENT_LIMIT_TOO_LARGE</td><td>length - limit</td></tr><tr><td>REQUEST_CONTENT_LIMIT_LENGTH_REQUIRED</td><td>limit</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-request-content-limit/blob/master/CHANGELOG.md" %}
