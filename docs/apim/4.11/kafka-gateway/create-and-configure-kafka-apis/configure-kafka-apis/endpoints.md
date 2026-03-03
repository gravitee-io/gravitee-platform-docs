---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Native Kafka APIs support endpoint group and endpoint creation, with drag-and-drop reordering and specialized UI adaptations. This feature enables administrators to configure multiple Kafka bootstrap servers, apply security protocols, and manage endpoint priority without load balancer requirements.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

Native Kafka APIs use endpoint groups with type `native-kafka`. Unlike HTTP proxy endpoints, Native Kafka endpoint groups do not require a load balancer type. The first endpoint in the first group is automatically designated as the default endpoint used by the API.

## Prerequisites

To configure Native Kafka endpoint groups, your API must meet the following requirements:

* API definition version: `V4`
* API type: `NATIVE`
* At least one listener with type `KAFKA`

### Drag-and-drop implementation

The Angular CDK `DragDropModule` enables drag-and-drop reordering of endpoints within an endpoint group.

When an endpoint is reordered:

1. The component fetches the current API state.
2. The endpoint array order is updated using `splice()`.
3. The changes are saved.
4. A success message ("Endpoint reordered successfully") is displayed via the snackbar service.

Reordering is disabled when `isReadOnly === true` or `isReordering === true`.

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

## Native Kafka endpoint configuration

### Endpoint group type selection

When creating an endpoint group, the type is auto-selected based on API type:

| API Type | Default Endpoint Group Type |
|:---------|:---------------------------|
| `PROXY` | `http-proxy` |
| `LLM_PROXY` | `llm-proxy` |
| `NATIVE` (with Kafka listener) | `native-kafka` |

Native Kafka endpoint groups (`native-kafka`) do not use load balancer configuration and support endpoint reordering via drag-and-drop.

### Load balancer validation

Native Kafka endpoint groups do not require a load balancer type. The load balancer type field is not displayed in the endpoint group table for Native Kafka APIs.

| Property | Required For | Not Required For |
|:---------|:------------|:----------------|
| `loadBalancerType` | `PROXY`, `LLM_PROXY` APIs | `NATIVE` APIs with Kafka listeners |

### Endpoint configuration properties

| Property Path | Description | Example |
|:-------------|:-----------|:--------|
| `endpoint.configuration.bootstrapServers` | Kafka bootstrap server addresses | Displayed as "Bootstrap Servers" in endpoint table |
| `endpoint.sharedConfigurationOverride.security.protocol` | Endpoint-specific security protocol override | `SASL_SSL`, `PLAINTEXT` |
| `endpointGroup.sharedConfiguration.security.protocol` | Group-level security protocol (inherited by endpoints) | `SASL_SSL`, `PLAINTEXT` |

## Edit the endpoint group

Gravitee assigns each Kafka API endpoint group the default name **Default Broker group.**

To edit the endpoint group, complete the following steps:

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

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**. For Native Kafka APIs, the first endpoint in the first endpoint group receives a "Default" badge and serves as the API's primary endpoint.

Endpoint configuration properties:

| Property Path | Description | Example |
|:-------------|:-----------|:--------|
| `endpoint.configuration.bootstrapServers` | Kafka bootstrap server addresses | Displayed as "Bootstrap Servers" in endpoint table |
| `endpoint.sharedConfigurationOverride.security.protocol` | Endpoint-specific security protocol override | `SASL_SSL`, `PLAINTEXT` |
| `endpointGroup.sharedConfiguration.security.protocol` | Group-level security protocol (inherited by endpoints) | `SASL_SSL`, `PLAINTEXT` |

To edit the endpoint, complete the following steps:

1. Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>

2. Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>

3. By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>

### Security protocol badges

Native Kafka endpoints display security protocol information as badges in the endpoint table. Protocols can be configured at the group level (inherited by all endpoints) or overridden per endpoint. The badge tooltip indicates whether the protocol is inherited or endpoint-specific.

| Badge Text | Tooltip (Endpoint Override) | Tooltip (Inherited) |
|:-----------|:----------------------------|:--------------------|
| `{protocol}` (e.g., `SASL_SSL`) | "Security protocol override by endpoint configuration" | "Security protocol inherited from group configuration" |

## Reorder endpoints

Endpoints within a group can be reordered via drag-and-drop. The order determines priority, with the first endpoint in the first group serving as the default.

To reorder endpoints:

1. Click and hold the drag handle icon on the left side of the endpoint row.
2. Drag the endpoint to the desired position within the group.
3. Release to drop the endpoint in the new position.

A success message ("Endpoint reordered successfully") confirms the operation. Reordering is disabled when the API is in read-only mode or during an active reorder operation to prevent conflicts.

## Restrictions

Endpoint group and endpoint creation is not available for `MCP_PROXY` API types.

Drag-and-drop reordering is disabled when the API is in read-only mode or during an active reorder operation.

The `weight` column is hidden for Native APIs because endpoint weighting is not used.

Load balancer configuration is not applicable to Native Kafka endpoint groups.
