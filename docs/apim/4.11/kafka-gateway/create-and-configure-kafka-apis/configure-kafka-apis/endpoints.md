---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one endpoint group with a single endpoint. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

An API is classified as Native Kafka when its `type` is `NATIVE` and it contains at least one listener with `type` set to `KAFKA`. This classification determines which endpoint group types are available and how endpoints are displayed and validated.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

Native Kafka APIs support multiple endpoint groups and endpoints. You can reorder endpoint groups and endpoints using drag-and-drop functionality. The UI displays Kafka-specific configuration properties, including bootstrap servers and security protocols.

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

## Endpoint group types

Native Kafka APIs use the `native-kafka` endpoint group type, which is automatically selected during creation. Unlike proxy APIs, Native Kafka endpoint groups do not require a load balancer type. The load balancer type is set to `null`, and the weight column is hidden from the endpoint table because Kafka clients manage broker selection internally.

### Endpoint group properties

| Property | Type | Required | Description | Example |
|:---------|:-----|:---------|:------------|:--------|
| `type` | String | Yes | Endpoint group type, automatically set to `native-kafka` for Native Kafka APIs | `native-kafka` |
| `loadBalancer.type` | String | No | Load balancer type; set to `null` for Native Kafka (not required) | `null` |
| `sharedConfiguration.security.protocol` | String | No | Security protocol inherited by all endpoints in the group unless overridden | `SASL_SSL` |

## Default endpoint behavior

The first endpoint in the first endpoint group of a Native Kafka API is automatically designated as the default endpoint. This endpoint is used when no specific endpoint is requested and is marked with a "Default" badge in the UI.

## Prerequisites

Before managing endpoint groups and endpoints for a Native Kafka API, ensure the following:

* The API is configured with `type: NATIVE` and at least one listener with `type: KAFKA`.
* Bootstrap servers are configured for each endpoint.
* Security protocol configuration is set at the group or endpoint level if required.

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
* **SASL\_PLAINTEXT:** Choose NONE, AWS\_MSK\_IAM, GSSAPI, OAUTHBEARER, OAUTHBEARER\_TOKEN, PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, or DELEGATE\_TO\_BROKER.
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

## Create an endpoint group

1. Navigate to the API's endpoint groups page.
2. Click **Add Endpoint Group**.
3. The endpoint group type is automatically set to `native-kafka` for Native Kafka APIs.
4. Enter a name for the group.
5. Configure shared settings such as security protocol if needed. Load balancer type is not required and is set to `null`.
6. Add at least one endpoint by providing bootstrap servers in the configuration step.
7. Click **Save**.

The first endpoint in the first group becomes the default endpoint automatically.

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**.

1. Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>

2. Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>

3. By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>

### Endpoint properties

| Property | Type | Required | Description | Example |
|:---------|:-----|:---------|:------------|:--------|
| `configuration.bootstrapServers` | String | Yes | Comma-separated list of Kafka broker addresses | `broker1:9092,broker2:9092` |
| `sharedConfigurationOverride.security.protocol` | String | No | Endpoint-level security protocol override | `PLAINTEXT` |
| `inheritConfiguration` | Boolean | No | When `true`, endpoint inherits group-level shared configuration | `true` |

### Configuration inheritance

Endpoints inherit configuration from their endpoint group by default. To override group-level settings:

1. Set `inheritConfiguration` to `false`.
2. Define endpoint-specific values in `sharedConfigurationOverride`.

When `inheritConfiguration` is `true`, the endpoint uses the group's `sharedConfiguration.security.protocol`. When `false`, the endpoint uses `sharedConfigurationOverride.security.protocol` if defined.

## Add additional endpoints

To add additional Kafka broker connections within an existing endpoint group:

1. Within an existing endpoint group, click **Add Endpoint**.
2. Provide a name for the endpoint.
3. Enter the bootstrap servers configuration (required).
4. To override the group's security protocol, disable **Inherit Configuration** and set endpoint-specific values.
5. Click **Save**.

The new endpoint appears in the endpoint table with a badge showing its security protocol configuration.

## Reorder endpoints

Endpoints can be reordered within an endpoint group using drag-and-drop.

1. Click and hold the drag icon on the left side of the endpoint row.
2. Drag the endpoint to the desired position.
3. Release to drop the endpoint in the new position.

The API updates automatically. A success message confirms the reordering. Drag-and-drop is disabled when the API is in read-only mode or when a reordering operation is in progress.

## Endpoint table display

The endpoint table displays the following columns for Native Kafka APIs:

* **Drag icon**: Enables drag-and-drop reordering. The cursor changes to `move` when hovering over the icon.
* **Name**: Displays the endpoint name. The first endpoint in the first group shows a **Default** badge with the tooltip "The default endpoint used by the API is the first one."
* **General**: Displays the **Bootstrap Servers** value from `endpoint.configuration.bootstrapServers`. Text truncates with ellipsis if it exceeds the column width.
* **Options**: Displays a badge showing the security protocol value. The badge tooltip indicates whether the protocol is inherited from the group configuration or overridden by the endpoint configuration.
* **Actions**: Displays **Edit** and **Delete** buttons. The **Edit** button opens the endpoint configuration. The **Delete** button removes the endpoint from the group.

The **Weight** column is hidden for Native Kafka APIs because Kafka clients manage broker selection internally.

### Security protocol badge behavior

The **Options** column displays a neutral badge showing the security protocol value when a security protocol is configured at the group or endpoint level.

* **Inherited configuration**: The badge displays the group-level security protocol value. The tooltip reads "Security protocol inherited from group configuration."
* **Overridden configuration**: The badge displays the endpoint-level security protocol value. The tooltip reads "Security protocol override by endpoint configuration."

If no security protocol is configured, the badge is not displayed.

## Restrictions

The following restrictions apply to Native Kafka endpoint configuration:

* **Load balancer type:** Not applicable to Native Kafka APIs. The load balancer type is set to `null`.
* **Bootstrap servers:** Required for each endpoint.
* **Drag-and-drop reordering:** Disabled in read-only mode.
* **Reordering operations:** Serialized. Only one reorder operation can occur at a time.
* **Weight-based load balancing:** Not supported for Native Kafka endpoints.


