---
description: An overview about ssl enforcement.
metaLinks:
  alternates:
    - ssl-enforcement.md
---

# SSL Enforcement

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../readme/enterprise-edition.md)**.**
{% endhint %}

## Overview

You can use the `ssl-enforcement` policy to filter incoming SSL requests. It allows you to restrict or allow access only to requests with client certificate authentication or only to a subset of valid clients.

In addition to the distinguished name whitelist, the policy can validate client certificates against required certificate policy OIDs and against Subject Alternative Name (SAN) patterns.

This policy is mainly used in plan configuration to allow access to consumers for a given set of certificates. The client is able to pass a valid certificate in one of two ways:

* In session: This is the default behavior. The client certificate is accessible through the TLS session, which must remain active during the certificate request. If the session is terminated, the certificate will not be visible.
* In header: A reverse proxy (e.g., NGINX, Apache) passes the client certificate using a specified header. This option requires the user to specify which header contains the certificate, which is base64-encoded.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 TCP proxy APIs or v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
"ssl-enforcement" : {
    "requiresSsl": true,
    "requiresClientAuthentication": true,
    "whitelistClientCertificates": [
        "CN=localhost,O=GraviteeSource,C=FR"
    ]
}
```
{% endtab %}
{% endtabs %}

## Configuration

The `ssl-enforcement` policy uses Ant-style patterns when matching certificate distinguished names and Subject Alternative Names, with the following wildcards:

* `?` matches one character
* `*` matches zero or more characters
* `**` matches zero or more path segments

### Phases

The phases checked below are supported by the `ssl-enforcement` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="204.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `ssl-enforcement` policy can be configured with the following options:

<table><thead><tr><th width="266">Property</th><th data-type="checkbox">Required</th><th width="222">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>requiresSsl</td><td>false</td><td>Is SSL required to access this resource?</td><td>boolean</td><td>true</td></tr><tr><td>requiresClientAuthentication</td><td>false</td><td>Is client authentication required to access this resource?</td><td>boolean</td><td>false</td></tr><tr><td>whitelistClientCertificates</td><td>false</td><td>List of allowed X.500 names (from client certificate). Supports Ant-pattern matching (e.g., <code>CN=localhost,O=GraviteeSource*,C=??</code>)</td><td>array of strings</td><td>-</td></tr><tr><td>requiredCertificatePolicies</td><td>false</td><td>List of OIDs (dotted-decimal format, e.g., <code>1.3.6.1.4.1.99999.1</code>) that must be present in the certificate's Certificate Policies extension. All listed OIDs must be present. Empty or unset means no OID validation.</td><td>array of strings</td><td>-</td></tr><tr><td>whitelistSubjectAlternativeNames</td><td>false</td><td>List of allowed Subject Alternative Name patterns. Supports Ant-pattern matching (e.g., <code>*.example.com</code>, <code>partner-*</code>). At least one SAN must match at least one pattern. Empty or unset means no SAN validation.</td><td>array of strings</td><td>-</td></tr></tbody></table>

### Certificate Policy OID Validation

The policy can enforce that client certificates contain specific Object Identifiers (OIDs) in their Certificate Policies X.509 extension. OIDs are specified in dotted-decimal format (e.g., `1.3.6.1.4.1.99999.1`). All listed OIDs must be present in the certificate for validation to succeed. If the Certificate Policies extension is absent or malformed, validation fails. An empty or unset list disables OID validation.

OID values in **Required Certificate Policies** must match the regex `^\d+(\.\d+)+$` (dotted-decimal format). Invalid formats are rejected at configuration validation time.

### Subject Alternative Name Whitelist

The policy can restrict client certificates to those containing Subject Alternative Names (SANs) that match at least one Ant-style pattern (e.g., `*.example.com`, `partner.example.com`). The policy checks all SAN types (DNS, email, URI, IP); if any SAN matches any pattern, validation succeeds. Matching is case-insensitive. An empty or unset list disables SAN validation.

### Validation Execution Order

The policy enforces checks in the following sequence: SSL requirement, client authentication requirement, DN whitelist, required OIDs, and SAN whitelist. Each check runs only if its prerequisite conditions are met. For example, OID and SAN validation occur only when **Requires Client Authentication** is enabled and the respective configuration properties are non-empty.

Both **Required Certificate Policies** and **Whitelist Subject Alternative Names** are skipped entirely when **Requires Client Authentication** is `false`.

## Compatibility matrix

The following is the compatibility matrix for APIM and the `ssl-enforcement` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.x            | All                     |

## Errors

<table><thead><tr><th width="209.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>401</code></td><td>Access to the resource is unauthorized according to policy rules</td></tr><tr><td><code>403</code></td><td>Access to the resource is forbidden according to policy rules</td></tr></tbody></table>

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="442.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>SSL_ENFORCEMENT_SSL_REQUIRED</td><td>-</td></tr><tr><td>SSL_ENFORCEMENT_AUTHENTICATION_REQUIRED</td><td>-</td></tr><tr><td>SSL_ENFORCEMENT_CLIENT_FORBIDDEN</td><td>name (X.500 name from client certificate)</td></tr><tr><td>SSL_ENFORCEMENT_OID_MISMATCH</td><td>required (list of OIDs configured in <code>requiredCertificatePolicies</code>)</td></tr><tr><td>SSL_ENFORCEMENT_SAN_MISMATCH</td><td>whitelist (list of patterns configured in <code>whitelistSubjectAlternativeNames</code>)</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-ssl-enforcement/blob/master/CHANGELOG.md" %}
