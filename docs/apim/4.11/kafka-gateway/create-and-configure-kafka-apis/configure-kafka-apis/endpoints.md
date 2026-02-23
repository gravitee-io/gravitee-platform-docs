---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one endpoint group with a single endpoint. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Managing multiple endpoint groups and endpoints

Native Kafka APIs can create, configure, and reorder Kafka endpoints through the Gravitee APIM Console UI. This capability removes previous restrictions that prevented Native Kafka APIs from managing multiple endpoint groups and endpoints. For detailed instructions on managing Native Kafka endpoints, see [Managing Native Kafka Endpoints](../managing-native-kafka-endpoints.md).

<!-- NEED CLARIFICATION: Confirm the relative path to the new 'Managing Native Kafka Endpoints' guide. The path '../managing-native-kafka-endpoints.md' assumes the new guide is a sibling file in the same directory as endpoints.md. -->

### Native Kafka API detection

The system identifies a Native Kafka API when both conditions are met:

* The API type is `NATIVE`
* At least one listener has type `KAFKA`

This detection drives conditional UI behavior and validation rules throughout the endpoint management workflow.

### Default endpoint semantics

For Native Kafka APIs, the first endpoint in the first endpoint group is always designated as the default endpoint. This default assignment is automatic and cannot be changed through load balancer configuration. The UI displays a "Default" badge on this endpoint with the tooltip "The default endpoint used by the API is the first one."

### Endpoint group type assignment

The system automatically assigns endpoint group types based on API classification:

* `http-proxy` for PROXY APIs
* `llm-proxy` for LLM_PROXY APIs
* `native-kafka` for NATIVE APIs with Kafka listeners

This type determines which configuration fields are required and how endpoints are displayed in the management table.

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

## Prerequisites

* Gravitee APIM Console access with API management permissions
* Native Kafka API already created with at least one Kafka listener configured
* Bootstrap server addresses available for endpoint configuration

## Gateway configuration

### Load balancer validation

The `loadBalancerType` form control applies conditional validation based on API type. For all API types except Native Kafka, this field is required. For Native Kafka APIs, the validator is removed and the field is hidden in the UI.

| Property | Type | Validation Rule |
|:---------|:-----|:----------------|
| `loadBalancerType` | FormControl | Required for PROXY, LLM_PROXY, MESSAGE types; not required for NATIVE Kafka |

### Endpoint configuration properties

Native Kafka endpoints require bootstrap server addresses in place of target URLs. Security protocol configuration can be set at the endpoint group level and optionally overridden per endpoint.

| Property | Description | Example |
|:---------|:------------|:--------|
| Bootstrap Servers | Comma-separated list of Kafka broker addresses | `kafka-1.example.com:9092,kafka-2.example.com:9092` |
| Security Protocol | Authentication mechanism (group-level or endpoint override) | `SASL_SSL`, `PLAINTEXT` |

## Creating an endpoint group

To create an additional endpoint group:

1. Navigate to the API's endpoint configuration.
2. Select **Add Endpoint Group**.
3. The system automatically assigns the `native-kafka` type for Native Kafka APIs.
4. Configure the bootstrap servers and optional security protocol at the group level. These settings apply to all endpoints in the group unless overridden.
5. Click **Save** to create the group.

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

## Adding endpoints to a group

To add endpoints within an endpoint group:

1. Within an endpoint group, click **Add Endpoint**.
2. Provide a unique name and bootstrap server addresses.
3. Optionally override the group's security protocol if this endpoint requires different authentication.
4. Click **Save** to create the endpoint.

The endpoint inherits group-level settings by default, indicated by "inherited from group configuration" tooltips in the UI.

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**.

1. Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>

2. Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>

3. By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>

## Reordering endpoints

To reorder endpoints within a group:

1. Click and hold the drag icon (⋮⋮) next to an endpoint name.
2. Drag to the desired position.
3. Release to apply the new order.

The system validates that `previousIndex` differs from `currentIndex` before triggering an API update. Reordering does not change the default endpoint designation for Native Kafka APIs—the first endpoint in the first group remains default regardless of subsequent reordering.

## Architecture notes

### Dynamic table columns

The endpoint management table adapts its columns based on API and endpoint types. Base columns include drag icon, name, general (Target URL or Bootstrap Servers), options, weight, and actions. For Native Kafka APIs, the weight column is removed since load balancing does not apply. The options column displays security protocol badges with inheritance indicators. The general column label changes from "Target URL" to "Bootstrap Servers" for Kafka endpoints.

### Endpoint options badges

The UI displays type-specific badges in the options column. For HTTP proxy endpoints, a "Health Check" badge appears when health checking is enabled, with tooltips distinguishing inherited vs. endpoint-specific configuration. For Native Kafka endpoints, the security protocol (e.g., `SASL_SSL`) displays as a badge, with tooltips indicating whether the protocol is inherited from the group or overridden at the endpoint level.

## Restrictions

* MCP_PROXY APIs cannot create endpoint groups or add endpoints through this interface
* Load balancer configuration is not applicable to Native Kafka APIs and is hidden in the UI
* The default endpoint for Native Kafka APIs is always the first endpoint in the first group and cannot be changed
* Drag-and-drop reordering is limited to endpoints within the same group
* Endpoint group type is automatically assigned and cannot be manually changed after creation
* Bootstrap server addresses must be provided for all Native Kafka endpoints (no default value)

## Related changes

The Angular CDK drag-drop module was added as a dependency to enable endpoint reordering functionality. The endpoint management table now dynamically adjusts displayed columns based on API type, removing the weight column for Native Kafka APIs and hiding the options column when no badges are present. Form validation logic was updated to conditionally apply the load balancer type requirement, removing the validator for Native Kafka APIs during component initialization. The adapter layer now generates type-specific column names and endpoint badges based on API classification and endpoint configuration inheritance.

## Troubleshooting

### Bootstrap servers required for Native Kafka endpoints

**Symptom**: Endpoint creation or update fails with a validation error indicating missing bootstrap servers.

**Cause**: Native Kafka endpoints do not have a default value for bootstrap server addresses. The system requires explicit configuration of at least one Kafka broker address.

**Resolution**: Provide a comma-separated list of bootstrap server addresses in the format `host:port`. For example:

```
kafka-1.example.com:9092,kafka-2.example.com:9092
```

Bootstrap servers can be configured at the endpoint group level (inherited by all endpoints) or overridden per endpoint in the endpoint's **General** tab.

### Load balancer validation skipped for Native Kafka APIs

**Symptom**: The load balancer type field is not visible or required when configuring Native Kafka API endpoints.

**Cause**: Load balancer configuration does not apply to Native Kafka APIs. The system automatically removes the `loadBalancerType` validator and hides the field in the UI when a Native Kafka API is detected.

**Resolution**: This is expected behavior. Native Kafka APIs use the first endpoint in the first endpoint group as the default endpoint, regardless of load balancer settings. No action is required.

### Drag-and-drop reordering does not trigger API update

**Symptom**: Dragging an endpoint to a new position does not save the reordering or update the API configuration.

**Cause**: The system validates that `previousIndex` differs from `currentIndex` before triggering an API update. If the endpoint is dropped in its original position, no update occurs.

**Resolution**: Ensure the endpoint is dragged to a different position within the same endpoint group. The new order is saved automatically when the drop completes at a valid target position.

<!-- GAP: Authentication flow details for SASL_SSL and other security protocols -->
<!-- GAP: Error handling behavior when drag-and-drop fails or API update returns an error -->
<!-- GAP: Version or edition requirements for Native Kafka API support -->
<!-- GAP: Migration path for existing Native Kafka APIs created before this feature -->
<!-- GAP: Error messages or UI feedback when drag-and-drop validation fails -->
<!-- GAP: Behavior when API update request fails during reordering -->