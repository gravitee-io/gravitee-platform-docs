---
description: An overview about ssl enforcement.
metaLinks:
  alternates:
    - ssl-enforcement.md
---

# SSL Enforcement

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../introduction/enterprise-edition.md)**.**
{% endhint %}

## Overview

You can use the `ssl-enforcement` policy to filter incoming SSL requests. It allows you to restrict or allow access only to requests with client certificate authentication or only to a subset of valid clients.

In addition to the distinguished name whitelist, the policy can validate client certificates against required certificate policy OIDs, Subject Alternative Name (SAN) patterns, and issuer Distinguished Names. This provides finer-grained control over which client certificates are accepted for mutual TLS authentication.

This policy is mainly used in plan configuration to allow access to consumers for a given set of certificates. The client is able to pass a valid certificate in one of two ways:

* In session: This is the default behavior. The client certificate is accessible through the TLS session, which must remain active during the certificate request. If the session is terminated, the certificate will not be visible. The TLS handshake has already validated the certificate chain against the listener truststore. The issuer whitelist meaningfully narrows "any trusted CA" down to a specific CA per API or plan.
* In header: A reverse proxy (e.g., NGINX, Apache) passes the client certificate using a specified header. This option requires the user to specify which header contains the certificate, which is base64-encoded. The gateway performs no chain validation and trusts the terminating proxy. The issuer whitelist is a non-cryptographic filter on the leaf certificate's issuer field and is not a substitute for trust-anchor pinning.

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

{% tab title="HTTP proxy API example with issuer whitelist" %}
Sample policy configuration with issuer whitelist:

```json
{
  "ssl-enforcement": {
    "requiresSsl": true,
    "requiresClientAuthentication": true,
    "whitelistIssuers": [
      "CN=My Intermediate CA,O=GraviteeSource,C=FR"
    ]
  }
}
```
{% endtab %}
{% endtabs %}

## Configuration

The `ssl-enforcement` policy uses Ant-style patterns when matching certificate distinguished names, issuer distinguished names, and Subject Alternative Names, with the following wildcards:

* `?` matches one character
* `*` matches zero or more characters
* `**` matches zero or more path segments

### Phases

The phases checked below are supported by the `ssl-enforcement` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="204.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `ssl-enforcement` policy can be configured with the following options:

<table><thead><tr><th width="266">Property</th><th data-type="checkbox">Required</th><th width="222">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>requiresSsl</td><td>false</td><td>Is SSL required to access this resource?</td><td>boolean</td><td>true</td></tr><tr><td>requiresClientAuthentication</td><td>false</td><td>Is client authentication required to access this resource?</td><td>boolean</td><td>false</td></tr><tr><td>whitelistClientCertificates</td><td>false</td><td>List of allowed X.500 names (from client certificate). Supports Ant-pattern matching (e.g., <code>CN=localhost,O=GraviteeSource*,C=??</code>)</td><td>array of strings</td><td>-</td></tr><tr><td>whitelistIssuers</td><td>false</td><td>List of allowed issuer Distinguished Names. Matched against the client certificate's immediate issuer using order-insensitive RDN matching with Ant-pattern support. Any listed issuer matching means pass; empty or unset means no issuer validation.</td><td>array of strings</td><td>-</td></tr><tr><td>requiredCertificatePolicies</td><td>false</td><td>List of OIDs (dotted-decimal format, e.g., <code>1.3.6.1.4.1.99999.1</code>) that must be present in the certificate's Certificate Policies extension. All listed OIDs must be present. Empty or unset means no OID validation.</td><td>array of strings</td><td>-</td></tr><tr><td>whitelistSubjectAlternativeNames</td><td>false</td><td>List of allowed Subject Alternative Name patterns. Supports Ant-pattern matching (e.g., <code>*.example.com</code>, <code>partner-*</code>). At least one SAN must match at least one pattern. Empty or unset means no SAN validation.</td><td>array of strings</td><td>-</td></tr></tbody></table>

### Issuer Whitelist

The issuer whitelist restricts access to certificates issued by specific Certificate Authorities (CAs) within the set the gateway already trusts. When configured, the policy validates that the certificate was issued by one of the specified CAs. Matching is order-insensitive across Relative Distinguished Names (RDNs) and supports Ant-style patterns (`*`, `?`) for flexible matching. An empty or unset list disables issuer validation entirely.

**Pattern Syntax:**

* Use standard DN format: `ATTRIBUTE=value,ATTRIBUTE=value,...`
* Attribute names must be uppercase alphanumeric or OIDs (dotted-decimal)
* Values support Ant-style patterns: `*` (matches any characters), `?` (matches single character)
* Example: `CN=My Intermediate CA,O=GraviteeSource*,C=??`

**Validation Behavior:**

* Malformed issuer DNs in **Whitelist Issuers** are rejected when the configuration is validated
* Empty or unset list disables issuer validation
* Matching is order-insensitive across RDNs

**Known Limitations:**

* **Fail-closed RDN matching**: Matching is exact on the number of RDNs. A partial entry such as `CN=My Intermediate CA` will NOT match a full issuer DN `CN=My Intermediate CA,O=GraviteeSource,C=FR`. Provide the complete issuer DN; use Ant patterns for the values (e.g., `O=GraviteeSource*`), not to omit RDNs.
* **Unknown attribute types render as OIDs**: Attribute types outside the standard DN name set render as their numeric OID. For example, `organizationIdentifier` (OID `2.5.4.97`) appears as `2.5.4.97=#<hex>`, so a friendly-name whitelist entry will not match. CA issuer DNs are conventionally limited to `CN`/`O`/`C`, but keep this in mind for eIDAS/PSD2 certificates.
* **HEADER mode trust delegation**: In HEADER mode, the gateway performs no chain validation and trusts the terminating proxy. The issuer whitelist is a non-cryptographic filter on the leaf certificate's issuer field — not a substitute for trust-anchor pinning.
* **Immediate issuer only**: The check validates the client certificate's immediate issuer, not the entire chain or root CA.

### Certificate Policy OID Validation

The policy can enforce that client certificates contain specific Object Identifiers (OIDs) in their Certificate Policies X.509 extension. OIDs are specified in dotted-decimal format (e.g., `1.3.6.1.4.1.99999.1`). All listed OIDs must be present in the certificate for validation to succeed. If the Certificate Policies extension is absent or malformed, validation fails. An empty or unset list disables OID validation.

OID values in **Required Certificate Policies** must match the regex `^\d+(\.\d+)+$` (dotted-decimal format). Invalid formats are rejected at configuration validation time.

### Subject Alternative Name Whitelist

The policy can restrict client certificates to those containing Subject Alternative Names (SANs) that match at least one Ant-style pattern (e.g., `*.example.com`, `partner.example.com`). The policy checks all SAN types (DNS, email, URI, IP); if any SAN matches any pattern, validation succeeds. Matching is case-insensitive. An empty or unset list disables SAN validation.

### Validation Execution Order

The policy enforces checks in the following sequence: SSL requirement, client authentication requirement, DN whitelist, issuer whitelist, required OIDs, and SAN whitelist. Each check runs only if its prerequisite conditions are met. For example, issuer, OID, and SAN validation occur only when **Requires Client Authentication** is enabled and the respective configuration properties are non-empty.

The **Whitelist Issuers**, **Required Certificate Policies**, and **Whitelist Subject Alternative Names** properties are skipped entirely when **Requires Client Authentication** is `false`.

## Compatibility matrix

The following is the compatibility matrix for APIM and the `ssl-enforcement` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.x            | All                     |

{% hint style="info" %}
The **Whitelist Issuers** property was introduced in plugin version 1.7.0. Existing configurations that omit this property continue to work unchanged — the issuer validation check is skipped entirely when the property is empty or unset. The feature is optional and additive, preserving backward compatibility with previous policy versions.
{% endhint %}

## Errors

<table><thead><tr><th width="209.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>401</code></td><td>Access to the resource is unauthorized according to policy rules</td></tr><tr><td><code>403</code></td><td>Access to the resource is forbidden according to policy rules</td></tr></tbody></table>

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="442.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>SSL_ENFORCEMENT_SSL_REQUIRED</td><td>-</td></tr><tr><td>SSL_ENFORCEMENT_AUTHENTICATION_REQUIRED</td><td>-</td></tr><tr><td>SSL_ENFORCEMENT_CLIENT_FORBIDDEN</td><td>name (X.500 name from client certificate)</td></tr><tr><td>SSL_ENFORCEMENT_ISSUER_MISMATCH</td><td>issuer (observed leaf issuer DN)</td></tr><tr><td>SSL_ENFORCEMENT_OID_MISMATCH</td><td>required (list of OIDs configured in <code>requiredCertificatePolicies</code>)</td></tr><tr><td>SSL_ENFORCEMENT_SAN_MISMATCH</td><td>whitelist (list of patterns configured in <code>whitelistSubjectAlternativeNames</code>)</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-ssl-enforcement/blob/master/CHANGELOG.md" %}
