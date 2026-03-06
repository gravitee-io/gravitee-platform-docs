---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one endpoint group with a single endpoint. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Multi-tenant endpoint support

Multi-tenant endpoint support enables gateway administrators to route Native Kafka API traffic to different backend endpoints based on the gateway's configured tenant identifier. This allows a single API definition to serve multiple isolated environments (e.g., internal vs. external networks) without duplicating API configurations.

### Tenant-based routing

Each gateway instance can be assigned a tenant identifier via the `tenant` configuration property. When processing a Native Kafka API request, the gateway selects the first endpoint whose tenant list includes the gateway's tenant. If no tenant is configured on the gateway, all endpoints are eligible. If no tenant list is defined on an endpoint, that endpoint matches any gateway tenant.

### Prerequisites

Before you configure tenant-based routing for Native Kafka APIs, ensure the following:

* Gravitee API Management 4.x with Native Kafka API support is installed
* Gateway instances are configured with distinct tenant identifiers (required only if tenant-based routing is needed)
* Tenant definitions are created in the Management Console (for UI display only; tenant IDs can be used directly in API definitions)

### Endpoint tenant assignment

Endpoints within a Native Kafka API can declare zero or more tenant identifiers. The gateway evaluates these lists at runtime to determine which backend to use. Multiple endpoints in the same group may share tenant assignments, but only the first matching endpoint is selected—no load balancing occurs across tenant-filtered endpoints.

Endpoints with `null` or empty tenant lists match any gateway tenant, including gateways with no tenant configured.

### Tenant resolution

The Management Console resolves tenant IDs to human-readable names when displaying endpoint configurations. If a tenant name cannot be found, the raw tenant ID is displayed. Tenant metadata (name, description) is managed separately from API definitions and is used only for UI display. The gateway uses tenant IDs directly from the API definition.

### Gateway configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `tenant` | Optional gateway tenant identifier used to filter eligible endpoints. If not set, the gateway matches all endpoints regardless of tenant assignment. | `"internal"` |

Gateways with no tenant configured match all endpoints, regardless of their tenant assignments.

### Operational restrictions

Only the first matching endpoint in a group is selected. No load balancing occurs across tenant-filtered endpoints.

If a gateway has a tenant configured and no endpoint matches, the API request fails with `KafkaNoApiEndpointFoundException`.

Tenant matching is exact and case-sensitive. Partial matches or wildcards are not supported.

### Error handling

When no endpoint matches the gateway's tenant, the error is logged at WARN level (not ERROR).

Error messages:

* `"No endpoint found for tenant: {tenantValue}"` when the gateway has a tenant configured
* `"No endpoint found for api"` when the gateway has no tenant configured

`KafkaNoApiEndpointFoundException` is handled without stack trace logging to reduce noise for expected tenant mismatch scenarios.

## Security protocols

Gravitee Kafka APIs support **PLAINTEXT**, **SASL\_PLAINTEXT**, **SASL\_SSL**, or **SSL** as the security protocol to connect to the Kafka cluster.

### SASL mechanisms

In addition to [Kafka's](https://kafka.apache.org/documentation/#security_overview) standard mechanisms, Gravitee supports:

* **NONE**: A stub mechanism that falls back to `PLAINTEXT` protocol.
* **OAUTHBEARER\_TOKEN**: A mechanism that defines a fixed token or a dynamic token from [Gravitee Expression Language](../../../../4.9/gravitee-expression-language.md).
* **DELEGATE\_TO\_BROKER**: Authentication is delegated to the Kafka broker.

{% hint style="warning" %}
When using `DELEGATE_TO_BROKER`, the supported mechanisms available to the client are `PLAIN` and `AWS_IAM_MSK`. The `AWS_MSK_IAM` mechanism requires you to host the Kafka Gateway on AWS. Otherwise, authentication fails.
{% endhint %}

## Edit the endpoint group

Gravitee assigns each Kafka API endpoint group the default name **Default Broker group.** To edit the endpoint group, complete the following steps:

1.  Click the **Edit** button with the pencil icon to edit the endpoint group.

    <figure><img src="../../../.gitbook/assets/edit-button-endpoint-group.png" alt=""><figcaption></figcaption></figure>
2.  Select the **General** tab to change the name of your Kafka endpoint group.

    <figure><img src="../../../.gitbook/assets/image (181).png" alt=""><figcaption></figcaption></figure>
3.  Select the **Configuration** tab to edit the security settings of your Kafka endpoint group.

    <figure><img src="../../../.gitbook/assets/select-configuration-tab-endpoint-group.png" alt=""><figcaption></figcaption></figure>
4.  Select one of the security protocols from the drop-down menu, and then configure the associated settings to define your Kafka authentication flow.

    <figure><img src="../../../.gitbook/assets/supported-endpoint-security-protocol.png" alt=""><figcaption></figcaption></figure>

* **PLAINTEXT:** No further security configuration is necessary.
* **SASL\_PLAINTEXT:** Choose NONE, GSSAPI, OAUTHBEARER, OAUTHBEARER\_TOKEN, PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, or DELEGATE\_TO\_BROKER.
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

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**.

1.  Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>
2.  Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>
3.  By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>
