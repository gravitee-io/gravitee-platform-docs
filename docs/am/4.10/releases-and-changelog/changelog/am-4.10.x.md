---
description: >-
  This page contains the changelog entries for AM 4.10.0 and any future minor or
  patch AM 4.10.x releases.
---

# AM 4.10.x

#### Gravitee Access Management 4.10 - Jan 8, 2026 <a href="#gravitee-access-management-4.8" id="gravitee-access-management-4.8"></a>

<details>

<summary>What's new</summary>

### Enhanced Kafka Reporting for Audit Logs

Access Management supports Kafka reporter, which enables seamless integration between your audit trails and Kafka topics. You can optimize data flow by selecting specific event types to send to your Kafka cluster.

### Secret References in Domain-Level Plugins

AM 4.1  extends our Secret Provider capabilities beyond the global `gravitee.yaml` configuration. Administrators can utilize secret references within specific plugin configurations defined at the Domain level.

{% hint style="info" %}
This functionality is currently exclusive to the **Certificate** **Plugin**.&#x20;
{% endhint %}

### User Authentication via Certificate

Access Management now supports Certificate-Based Authentication (CBA) as a primary authentication factor. Similar to WebAuthn, CBA uses public-key cryptography to prove identity but utilizes standard X.509 digital certificates.

### MCP Server Integration

{% hint style="warning" %}
**Tech Preview**: MCP Server support is currently in preview. Features and APIs may change in future releases. This functionality is not production-ready and you should use the feature with caution.
{% endhint %}

We are taking the first steps toward making **Model Context Protocol** (MCP) a first-class citizen within Access Management. This feature introduces a new application type designed specifically for MCP Resource Servers, enabling secure, standardized communication between AI models and your data tools.

### Authorization Engine (OpenFGA & AuthZen)

{% hint style="warning" %}
**Tech Preview:** The OpenFGA Authorization Engine is in tech preview. Features and APIs may change in future releases. This functionality is not production-ready. Contact Gravitee to get access and discover the feature.&#x20;

To get access, reach out to your Gravitee customer contact, or [book a demo](https://www.gravitee.io/demo).
{% endhint %}

In this release, we are laying the foundation for Access Management to serve as the primary Policy Decision Point (PDP) and permissions engine for Agentic AI and MCP ecosystems. This feature enables fine-grained, relationship-based access control (ReBAC) for AI tools and resources.

</details>

<details>

<summary>Breaking changes</summary>

### Optimized Audit Logging for Client Authentication

To improve Gateway performance and reduce log storage overhead, The record of client authentication in the audit logs has been optimized.&#x20;

* **Conditional Logging:** Starting in this version, successful client authentication attempts are filtered out of the audit logs by default.
* **Security Focus:** Failed authentication attempts continue to be logged in full, ensuring that potential unauthorized access or configuration issues remain visible to administrators.
* **Full Traceability (Optional):** If your compliance requirements necessitate logging every successful authentication, the previous behavior can be restored via configuration.

**Configuration Update**

To enable audit logs  again for successful client authentications, update the following property in your `gravitee.yaml`:

```yaml
reporters:
  audits:
    clientAuthentication:
      success:
        enabled: true        
```

#### Enhanced Introspection with Audience (aud) Support

We have updated the OAuth2 Introspection endpoint to include the `aud` (audience) claim in its response. This enhancement allows Resource Servers such as the new MCP Servers to verify that a token was specifically intended for them, which strengthens the security of the token validation process.

**Compatibility Toggle**

While this change improves security, we recognize it may impact existing deployments that do not expect the `aud` claim in the introspection response ([Issue #3111](https://github.com/gravitee-io/issues/issues/3111)). To ensure a smooth transition, A configuration toggle has been included to disable this behavior if necessary.

To remove the `aud` claim from the introspection response, update your `gravitee.yaml` with the following configuration:

```yaml
handlers:
  oauth2:
    introspect:
      allowAudience: false
```

</details>
