---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one endpoint group with a single endpoint. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Security protocols&#x20;

Gravitee Kafka APIs support **PLAINTEXT**, **SASL\_PLAINTEXT**, **SASL\_SSL**, or **SSL** as the security protocol to connect to the Kafka cluster.

### SASL mechanisms

In addition to [Kafka's](https://kafka.apache.org/documentation/#security_overview) standard mechanisms, Gravitee supports:

* **NONE**: A stub mechanism that falls back to `PLAINTEXT` protocol.
* **OAUTHBEARER\_TOKEN**: A mechanism that defines a fixed token or a dynamic token from [Gravitee Expression Language](../../../gravitee-expression-language.md).
*   **DELEGATE\_TO\_BROKER**: Authentication is delegated to the Kafka broker.

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>When using <code>DELEGATE_TO_BROKER</code>, the supported mechanisms available to the client are <code>PLAIN</code> and <code>AWS_IAM_MSK</code>. The <code>AWS_MSK_IAM</code> mechanism requires you to host the Kafka Gateway on AWS. Otherwise, authentication fails.</p></div>

## Edit the endpoint group

Gravitee assigns each Kafka API endpoint group the default name **Default Broker group.** To edit the endpoint group, complete the following steps:&#x20;

1.  Click the **Edit** button with the pencil icon to edit the endpoint group.

    <figure><img src="../../../.gitbook/assets/edit-button-endpoint-group.png" alt=""><figcaption></figcaption></figure>
2.  Select the **General** tab to change the name of your Kafka endpoint group.

    <figure><img src="../../../.gitbook/assets/image (181).png" alt=""><figcaption></figcaption></figure>
3.  Select the **Configuration** tab to edit the security settings of your Kafka endpoint group.

    <figure><img src="../../../.gitbook/assets/select-configuration-tab-endpoint-group.png" alt=""><figcaption></figcaption></figure>
4.  Select one of the security protocols from the drop-down menu, and then configure the associated settings to define your Kafka authentication flow.

    <figure><img src="../../../.gitbook/assets/supported-endpoint-security-protocol.png" alt=""><figcaption></figcaption></figure>

* **PLAINTEXT:** No further security configuration is necessary.
* **SASL\_PLAINTEXT:** Choose NON&#x45;**,** GSSAPI, OAUTHBEARER, OAUTHBEARER\_TOKEN, PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, or DELEGATE\_TO\_BROKER.
  * **NONE:** No additional security configuration required.
  * **AWS\_MSK\_IAM:** Enter the JAAS login context parameters.
  * **GSSAPI:** Enter the JAAS login context parameters.
  * **OAUTHBEARER:** Enter the OAuth token URL, client ID, client secret, and the scopes to request when issuing a new token.
  * **OAUTHBEARER\_TOKEN:** Provide your custom token value.
  * **PLAIN:** Enter the username and password to connect to the broker.
  * **SCRAM-SHA-256:** Enter the username and password to connect to the broker.
  * **SCRAM-SHA-512:** Enter the username and password to connect to the broker.
  * **DELEGATE\_TO\_BROKER:** No additional security configuration required.
* **SSL:** Choose whether to enable host name verification, and then use the drop-down menu to configure a truststore type.
  * **None**
  * **JKS with content:** Enter binary content as base64 and the truststore password.
  * **JKS with path:** Enter the truststore file path and password.
  * **PKCS#12 / PFX with content:** Enter binary content as base64 and the truststore password.
  * **PKCS#12 / PFX with path:** Enter the truststore file path and password.
  * **PEM with content:** Enter binary content as base64 and the truststore password.
  * **PEM with path:** Enter the truststore file path and password and the keystore type.
* **SASL\_SSL:** Configure both SASL authentication and SSL encryption, choose a **SASL** mechanism from the options listed under **SASL\_PLAINTEXT**, and then configure **SSL** settings as described in the **SSL** section.

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**.&#x20;

1.  Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>
2.  Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>
3.  By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>

### Endpoint groups and multiple endpoints

A Kafka Native API can be configured with multiple Endpoint Groups and multiple Endpoints per group. Endpoint Groups organize and prioritize endpoints. The gateway selects the first endpoint from the first Endpoint Group, or the first valid endpoint if tenant-based selection is configured.

#### Multiple endpoints per group

You can add, remove, rename, and reorder endpoints within a native endpoint group for a Kafka API. Endpoints are evaluated in the order they appear within each group. The first valid endpoint is selected at runtime.

#### Tenant-based endpoint selection

Tenants enable zone-aware or region-specific routing. Each endpoint can be associated with one or more tenants, or left untagged to serve as a shared fallback endpoint.

**Gateway without tenant configured**

The gateway selects the first endpoint from the first Endpoint Group. No tenant-based filtering is applied.

**Gateway with tenant configured**

The gateway selects the first valid endpoint from the first Endpoint Group according to the following criteria:

- An endpoint is valid if it has no tenant configuration (usable by all gateways), or
- An endpoint is valid if its tenant configuration matches the tenant configured on the gateway.

Endpoints whose tenant does not match the gateway are ignored. If no valid endpoint remains after filtering, the API does not run on that gateway.

#### Endpoint priority and selection order

Only the first Endpoint Group is considered for selection. Endpoints are evaluated in the order they appear within the group. The first valid endpoint is selected.

<!-- GAP: Dynamic routing policy or other future configuration options that allow selection of alternate endpoint groups are not yet documented. -->

#### Switching endpoints

Changing the active endpoint (by reordering or explicit action) triggers a deployment. The gateway gracefully closes existing connections for the affected API, and Kafka clients reconnect to the newly selected endpoint. Kafka clients handle reconnection; the gateway does not perform automatic failover or health checks.

<!-- GAP: Specific UI controls for "Set Active" action or drag-and-drop reordering are not described in the source. -->

#### Limitations

- No automatic failover or health checks.
- No load balancing (weights or round-robin) across endpoints.
- Cross-cluster data alignment, offset migration, and topic replication are customer-owned responsibilities.

<!-- GAP: Detailed UI screenshots and step-by-step instructions for configuring multiple endpoints and tenants are not provided in the source. -->

### Tenant assignment

Kafka endpoints support tenant-based routing. A Kafka endpoint can have no tenant configuration (generic endpoint) or be associated with one or more specific tenants.

Tenants are configurable in the organization settings and work similarly to tenants used for classic APIs in APIM. When a gateway is configured with a tenant identifier, it activates only the Kafka endpoints whose tenant list is empty or contains the configured tenant. Endpoints with mismatched tenants are ignored.

If no endpoint remains after tenant filtering, the gateway responds with a `503 – No endpoint available` error.

For more information about configuring multiple Kafka endpoints and tenant-based selection, see [Kafka multi-endpoint configuration](../../../kafka-gateway/create-and-configure-kafka-apis/configure-kafka-apis/kafka-multi-endpoint-configuration.md).

<!-- GAP: Link target "kafka-multi-endpoint-configuration.md" must be created or verified -->

### Multi-endpoint and tenant-based selection

Kafka APIs support multiple endpoints within a single endpoint group and tenant-based endpoint selection. The gateway automatically determines which endpoint to use based on defined rules.

For detailed configuration instructions, see [Kafka Multi-Endpoint Configuration](link-to-kafka-multi-endpoint-configuration-guide).

#### Key capabilities

- **Multiple endpoints per group**: Configure multiple Kafka endpoints within a single endpoint group to support scenarios such as disaster recovery, regional routing, or planned migrations.
- **Tenant-based selection**: Associate endpoints with specific tenants so that gateways automatically route traffic to the appropriate backend cluster based on their configured tenant.
- **Deterministic routing**: The gateway selects endpoints according to a defined priority order: tenant match, then first endpoint in the group.

#### Endpoint selection rules

The gateway applies the following logic when selecting an endpoint:

**Gateway without tenant configured**:
- Selects the first endpoint in the first endpoint group.
- No tenant-based filtering is applied.

**Gateway with tenant configured**:
- Selects the first valid endpoint from the first endpoint group.
- An endpoint is valid if:
  - It has no tenant configuration (available to all gateways), or
  - Its tenant configuration matches the gateway's configured tenant.
- Endpoints whose tenant does not match the gateway's tenant are ignored.

#### Switching endpoints

Publishers can manually switch the active endpoint by reordering endpoints within the group or using the "Set Active" action. Deploying this change gracefully closes existing connections, allowing Kafka clients to reconnect to the newly selected endpoint.

<!-- GAP: Link destination for "Kafka Multi-Endpoint Configuration" guide not provided in source -->