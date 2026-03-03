---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one endpoint group with a single endpoint. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

Native Kafka APIs now support full endpoint group and endpoint management, including creation, editing, and drag-and-drop reordering. Previously, Native Kafka APIs were restricted to a single default endpoint group. Administrators can now define multiple endpoint groups and endpoints to support complex routing and failover scenarios.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Prerequisites

Before configuring Native Kafka API endpoints, ensure the following:

* API must be defined with `type: NATIVE` and at least one `KAFKA` listener
* User must have permissions to edit API endpoint configuration
* Gateway must support Native Kafka API definitions (V4 definition version)

## Security protocols

Gravitee Kafka APIs support **PLAINTEXT**, **SASL\_PLAINTEXT**, **SASL\_SSL**, or **SSL** as the security protocol to connect to the Kafka cluster.

### SASL mechanisms

In addition to [Kafka's](https://kafka.apache.org/documentation/#security_overview) standard mechanisms, Gravitee supports:

* **NONE**: A stub mechanism that falls back to `PLAINTEXT` protocol.
* **OAUTHBEARER\_TOKEN**: A mechanism that defines a fixed token or a dynamic token from [Gravitee Expression Language](../../../gravitee-expression-language.md).
* **DELEGATE\_TO\_BROKER**: Authentication is delegated to the Kafka broker.

{% hint style="warning" %}
When using `DELEGATE_TO_BROKER`, the supported mechanisms available to the client are `PLAIN` and `AWS_IAM_MSK`. The `AWS_MSK_IAM` mechanism requires you to host the Kafka Gateway on AWS. Otherwise, authentication fails.
{% endhint %}

## Endpoint group properties

Endpoint groups define shared configuration settings that apply to all endpoints within the group. Native Kafka APIs support the following endpoint group properties:

| Property | Required | Description | Example |
|:---------|:---------|:------------|:--------|
| `name` | Yes | Unique identifier for the endpoint group | `"primary-cluster"` |
| `type` | Yes | Endpoint group type, automatically set to `native-kafka` for Native Kafka APIs | `"native-kafka"` |
| `loadBalancer.type` | No | Load balancer configuration. Not required for Native Kafka APIs | `null` |
| `sharedConfiguration.security.protocol` | No | Security protocol inherited by all endpoints in the group unless overridden | `"SASL_SSL"` |

{% hint style="info" %}
The `loadBalancer.type` property is optional for Native Kafka APIs. Leave this field empty unless specific load balancing behavior is required. Other API types (e.g., HTTP Proxy) continue to require load balancer selection.
{% endhint %}

## Endpoint properties

Endpoints define the connection details for individual Kafka brokers. Native Kafka APIs support the following endpoint properties:

| Property | Required | Description | Example |
|:---------|:---------|:------------|:--------|
| `name` | Yes | Descriptive name for the endpoint | `"broker-1"` |
| `configuration.bootstrapServers` | Yes | Comma-separated list of Kafka broker addresses | `"localhost:9092,localhost:9093"` |
| `sharedConfigurationOverride.security.protocol` | No | Endpoint-specific security protocol that overrides the group's shared configuration | `"PLAINTEXT"` |
| `weight` | N/A | Routing weight. Not applicable to Native Kafka APIs | N/A |

{% hint style="info" %}
The `weight` property is not applicable to Native Kafka APIs and is hidden in the UI.
{% endhint %}

### Configuration inheritance

Endpoints inherit configuration settings from their endpoint group by default. To override inherited settings, configure the `sharedConfigurationOverride` property at the endpoint level.

**Inheritance behavior:**
- If an endpoint does not define `sharedConfigurationOverride.security.protocol`, it inherits the value from `sharedConfiguration.security.protocol` in the endpoint group.
- If an endpoint defines `sharedConfigurationOverride.security.protocol`, the endpoint-specific value takes precedence over the group configuration.

**Example:**

An endpoint group defines `sharedConfiguration.security.protocol: "SASL_SSL"`. Endpoints in this group inherit `SASL_SSL` as the security protocol unless they explicitly override it with `sharedConfigurationOverride.security.protocol: "PLAINTEXT"`.

### Default endpoint badge

The first endpoint in the first endpoint group of a Native Kafka API receives a "Default" badge in the Console UI. This endpoint serves as the primary connection target when no other routing rules apply. The badge displays the tooltip "The default endpoint used by the API is the first one."

## Create an endpoint group

1. Navigate to the API's endpoint configuration page and select **Add Endpoint Group**.
2. Enter a unique name for the group.
3. For Native Kafka APIs, the type is automatically set to `native-kafka` and the load balancer field is optional. Leave it empty unless specific load balancing behavior is required.
4. Configure shared security settings (e.g., `security.protocol`) that will apply to all endpoints in the group unless overridden.
5. Save the group to make it available for endpoint creation.

## Edit the endpoint group

Gravitee assigns each Kafka API endpoint group the default name **Default Broker group.** To edit the endpoint group, complete the following steps:

1. Click the **Edit** button with the pencil icon to edit the endpoint group.

    <figure><img src="../../../.gitbook/assets/edit-button-endpoint-group.png" alt=""><figcaption></figcaption></figure>

2. Select the **General** tab to change the name of your Kafka endpoint group.

    <figure><img src="../../../.gitbook/assets/image (181).png" alt=""><figcaption></figcaption></figure>

3. Select the **Configuration** tab to edit the security settings of your Kafka endpoint group.

    <figure><img src="../../../.gitbook/assets/select-configuration-tab-endpoint-group.png" alt=""><figcaption></figcaption></figure>

4. Select one of the security protocols from the drop-down menu, and then configure the associated settings to define your Kafka authentication flow.

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

## Add endpoints to a group

1. Within an endpoint group, select **Add Endpoint**.
2. Provide a descriptive name for the endpoint.
3. Enter the `bootstrapServers` value as a comma-separated list of broker addresses (e.g., `localhost:9092`).
4. Optionally override the group's shared security protocol by setting `sharedConfigurationOverride.security.protocol`.
5. Save the endpoint. The endpoint will appear in the group's endpoint table with a badge indicating its security protocol (either inherited or overridden).

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**.

1. Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>

2. Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>

3. By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>

## Reorder endpoints

Endpoints within a group can be reordered using drag-and-drop functionality. To reorder endpoints:

1. Drag an endpoint row to a new position within the table.
2. Drop the endpoint at the desired location.
3. The system updates the endpoint order and displays a success message: "Endpoint reordered successfully."

Reordering is disabled in read-only mode and during active reordering operations.

## Restrictions

MCP Proxy APIs cannot create endpoint groups or add endpoints. This restriction remains unchanged.
