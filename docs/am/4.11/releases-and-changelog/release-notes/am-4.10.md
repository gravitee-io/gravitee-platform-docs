---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.10.
---

# AM 4.10

### Enhanced Kafka Reporting for Audit Logs

Access Management supports [Kafka reporter](../../getting-started/configuration/configure-reporters.md#kafka-reporter), which enables seamless integration between your audit trails and Kafka topics. You can optimize data flow by selecting specific event types to send to your Kafka cluster.

### Secret References in Domain-Level Plugins

{% hint style="info" %}
This functionality is currently exclusive to the **Certificate** **Plugin**.&#x20;
{% endhint %}

AM 4.10 extends our Secret Provider capabilities beyond the global `gravitee.yaml` configuration. Administrators can utilize [secret references](../../getting-started/configuration/domain-secrets/) within specific plugin configurations defined at the Domain level.

### User Authentication via Certificate

Access Management supports [Certificate-Based Authentication](../../guides/login/certificate-based-authentication.md) (CBA) as a primary authentication factor. Similar to WebAuthn, CBA uses public-key cryptography to prove identity but utilizes standard X.509 digital certificates.

### MCP Server Integration

{% hint style="warning" %}
**Tech Preview:** MCP Server support is currently in tech preview. Features and APIs might change in future releases. This functionality is not production-ready and you should use this feature with caution.
{% endhint %}

Access Management is now taking its first steps toward becoming a first-class citizen in the MCP ecosystem. This feature allows for secure and standardized communication between AI models and your internal tools.

* **Dedicated MCP App Type**: A new "[MCP Resource Server](../../guides/mcp-servers/)" application type is available in the creation wizard.
* **RFC 8707 Compliance**: AM now validates the `resource` parameter, ensuring tokens are scoped correctly for specific MCP servers and tools.

### Authorization Engine (OpenFGA & AuthZen)

{% hint style="warning" %}
**Tech Preview:** The OpenFGA Authorization Engine is currently in tech preview. Features and APIs may change in future releases. This functionality is not production-ready. Contact Gravitee to get access and discover the feature.&#x20;

To get access, reach out to your Gravitee customer contact, or [book a demo](https://www.gravitee.io/demo).
{% endhint %}

In 4.10, we are laying the foundation for Access Management to serve as the primary[ Policy Decision Point](am-4.10.md#authorization-engine-openfga-and-authzen) (PDP) and permissions engine for Agentic AI and MCP ecosystems. This feature enables fine-grained, relationship-based access control (ReBAC) for AI tools and resources.

* **OpenFGA Integration**: Connect an OpenFGA server to manage "tuples" that define relationships between users and AI tools. For example,  `user:johndoe` can `invoke` `tool:get_weather`.
* **AuthZen Interface**: An MVP interface aligned with the AuthZen specification allows MCP Gateways to request real-time "Permit/Deny" decisions.
* **Auditability**: A new `PERMISSION_EVALUATED` audit entry captures full request/response payloads for every AI authorization decision.
