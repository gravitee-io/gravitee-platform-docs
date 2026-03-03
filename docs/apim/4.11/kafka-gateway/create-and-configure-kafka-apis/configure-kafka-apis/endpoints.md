---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Native Kafka APIs support multiple endpoint groups with multiple endpoints per group. The **Endpoints** section lets you create, modify, and reorder your Kafka endpoint groups and endpoints.

Native Kafka APIs organize Kafka broker connections through endpoint groups. Each group contains one or more endpoints representing Kafka clusters. Unlike HTTP proxy APIs, Native Kafka APIs don't require load balancer configuration—Kafka handles message distribution internally.

An API is classified as Native Kafka when its type is `NATIVE` and it includes at least one listener with type `KAFKA`. This classification determines which endpoint group types, validation rules, and UI columns are available.

{% hint style="info" %}
**Native Kafka vs HTTP Proxy Endpoint Groups**

Native Kafka endpoint groups differ from HTTP proxy endpoint groups in several ways:
- **No load balancer configuration required**: Kafka handles message distribution internally
- **Bootstrap servers instead of target URLs**: The endpoint table displays bootstrap server addresses
- **Security protocol badges**: Endpoints display security protocol badges (e.g., `SASL_SSL`, `PLAINTEXT`) indicating the authentication mechanism
- **Endpoint group type**: Automatically assigned as `native-kafka` when `apiV4.type === 'NATIVE'` and at least one listener has `listener.type === 'KAFKA'`
- **Drag-and-drop reordering**: Endpoints can be reordered within a group using drag-and-drop
{% endhint %}

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Prerequisites

Before you configure Kafka endpoint groups, ensure the following:

* The API type is `NATIVE` with at least one Kafka listener configured
* The gateway supports API definition version V4
* You have permissions to create and modify endpoint groups
* For drag-and-drop reordering, the API must not be in read-only mode

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

### Security protocol inheritance

Native Kafka endpoints display security protocol badges indicating the authentication mechanism. Endpoints inherit the security protocol from the group's shared configuration unless explicitly overridden at the endpoint level.

The badge tooltip distinguishes between inherited and overridden values:

* **Inherited:** "Security protocol inherited from group configuration"
* **Overridden:** "Security protocol override by endpoint configuration"

## Endpoint group type assignment

When creating an endpoint group for a Native Kafka API, the endpoint group type is automatically set to `native-kafka`. This type determines configuration requirements, display columns, and inheritance behavior for security settings.

| API Type | Endpoint Group Type | Load Balancer Required |
|:---------|:-------------------|:----------------------|
| `PROXY` | `http-proxy` | Yes |
| `LLM_PROXY` | `llm-proxy` | Yes |
| `NATIVE` (with Kafka listener) | `native-kafka` | No |

{% hint style="info" %}
Load balancer configuration is optional for Native Kafka APIs because Kafka handles message distribution internally. The `loadBalancerType` property may be set to `null` for Native Kafka endpoint groups.
{% endhint %}

## Default endpoint designation

The first endpoint in the first endpoint group of a Native Kafka API is automatically designated as the default endpoint. This endpoint is used by the API when no specific endpoint is selected and is marked with a **Default** badge in the UI. This designation is automatic and cannot be manually changed.

## Create an endpoint group

To create an endpoint group for a Native Kafka API:

1. Navigate to the API's endpoint configuration.
2. Click **Add Endpoint Group**.
3. Enter a name for the endpoint group.
4. Configure shared settings like security protocol if needed—load balancer configuration is not required.
5. Add at least one endpoint with bootstrap server configuration.
6. Click **Save**.

The first endpoint in the first group becomes the default endpoint automatically. The load balancer field is not displayed for Native Kafka APIs.

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

## Add an endpoint to a group

To add an endpoint to an existing group:

1. Select the target endpoint group.
2. Click **Add Endpoint**.
3. Enter the endpoint name.
4. Configure the bootstrap servers property with Kafka broker addresses.
5. (Optional) Override the group's security protocol by setting the endpoint-level security protocol and disabling configuration inheritance.
6. Click **Save**.

The endpoint displays a security protocol badge indicating whether the value is inherited or overridden.

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**.

1. Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>

2. Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>

3. By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>

## Reorder endpoints

Endpoints within a group can be reordered using drag-and-drop:

1. Click and hold the drag icon on the left side of an endpoint row.
2. Drag the row to the desired position.
3. Release to drop the endpoint in its new position.

The API is updated immediately upon drop, and a success message "Endpoint reordered successfully" is displayed.

Drag-and-drop is disabled when:

* The API is in read-only mode
* A reordering operation is in progress

Endpoints cannot be moved between groups—reordering is available only within a single endpoint group.

## Endpoint display configuration

The endpoint table displays the following columns:

| Column | Display Condition | Content |
|:-------|:-----------------|:--------|
| Drag icon | Always | Drag handle for reordering (48px fixed width) |
| Name | Always | Endpoint name with optional **Default** badge |
| Bootstrap Servers | Always | Displays bootstrap server addresses |
| Options | Only if options exist | Security protocol badge (e.g., `SASL_SSL`) |
| Weight | Hidden for Native APIs | Not applicable |
| Actions | Always | Edit and delete actions (96px fixed width, right-aligned) |

### Column visibility by API type

| API Type | Displayed Columns | Notes |
|:---------|:------------------|:------|
| `NATIVE` (Kafka) | Drag icon, Name, General, Options, Actions | Weight column excluded |
| `PROXY` | Drag icon, Name, General, Options, Weight, Actions | All columns shown |
| `MESSAGE` (Kafka) | Drag icon, Name, General, Options, Weight, Actions | All columns shown |

### General column content

| Endpoint Type | Column Label | Value Source |
|:--------------|:-------------|:-------------|
| `native-kafka` | Bootstrap Servers | `endpoint.configuration.bootstrapServers` |
| `http-proxy` | Target URL | `endpoint.configuration.target` |
| `kafka` (MESSAGE API) | Bootstrap Servers | `endpoint.configuration.bootstrapServers` |

### Security protocol badges

Security protocol badges display the authentication mechanism for each endpoint:

| Badge Text | Tooltip (Inherited) | Tooltip (Override) |
|:-----------|:-------------------|:------------------|
| `{protocol}` (e.g., `SASL_SSL`) | "Security protocol inherited from group configuration" | "Security protocol override by endpoint configuration" |

If the endpoint inherits configuration or does not override the security protocol, the protocol is inherited from the endpoint group's shared configuration. Otherwise, the endpoint-specific protocol is displayed.

### Options column badges

| Endpoint Type | Badge Content | Condition | Tooltip |
|:--------------|:--------------|:----------|:--------|
| `native-kafka` | Security protocol value | Group or endpoint security protocol configured | "Security protocol override by endpoint configuration" (endpoint-level) or "Security protocol inherited from group configuration" (group-level) |
| `http-proxy` | "Health Check" | Group or endpoint health check enabled | "Health check enabled by endpoint configuration" (endpoint-level) or "Health check enabled via inherited group configuration" (group-level) |

Load balancer badges are hidden for `native-kafka` endpoint groups.

### Default endpoint badge

The first endpoint in the first endpoint group of a Native Kafka API receives a **Default** badge with the tooltip "The default endpoint used by the API is the first one." This designation is automatic and cannot be changed.

## Gateway configuration

### Load balancer settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `loadBalancerType` | Load balancer type for endpoint group; not required for Native Kafka APIs | `null` (Native Kafka), `ROUND_ROBIN` (other types) |

For Native Kafka APIs, load balancer configuration is optional and the field may be set to `null`.

### Endpoint configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `configuration.bootstrapServers` | Kafka bootstrap server addresses for native-kafka endpoints | `localhost:9092` |
| `sharedConfiguration.security.protocol` | Security protocol inherited from endpoint group | `SASL_SSL` |
| `sharedConfigurationOverride.security.protocol` | Security protocol override at endpoint level | `PLAINTEXT` |
| `inheritConfiguration` | Whether endpoint inherits group-level shared configuration | `true` |

## Restrictions

* Native Kafka APIs do not support endpoint weighting; the weight column is hidden
* Load balancer configuration is not applicable to Native Kafka endpoint groups and is not displayed in the UI
* The **Default** badge is assigned only to the first endpoint in the first endpoint group and cannot be manually changed
* Drag-and-drop reordering is disabled when the API is in read-only mode or when a reordering operation is in progress
* Endpoint reordering is available only within a single endpoint group; endpoints cannot be moved between groups
* Native Kafka endpoints require bootstrap servers configuration to pass validation
* Endpoint table layout uses fixed column widths for drag icon, weight, and actions columns; other columns use auto width with ellipsis overflow for the Bootstrap Servers column
