
---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Native Kafka APIs support endpoint group and endpoint creation, with drag-and-drop reordering and enhanced table displays. This feature enables administrators to configure multiple Kafka bootstrap servers, apply security protocol overrides, and manage endpoint priority through visual reordering.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Load balancer configuration is optional for Native Kafka APIs.
{% endhint %}


## Prerequisites

Before you configure Kafka endpoint groups, ensure the following requirements are met:

* **API type:** The API must be of type `NATIVE` with a Kafka listener configured.
* **User permissions:** You must have write permissions to modify endpoint groups and endpoints.
* **Drag-and-drop reordering:** The API must not be in read-only mode.

## Native Kafka API detection

The platform identifies Native Kafka APIs by checking for `type === 'NATIVE'` and the presence of a Kafka listener. When detected, the UI automatically selects the `native-kafka` endpoint group type and removes load balancer validation requirements.

| API Type | Auto-Selected Endpoint Group Type |
|:---------|:----------------------------------|
| `PROXY` | `http-proxy` |
| `LLM_PROXY` | `llm-proxy` |
| `NATIVE` (with Kafka listener) | `native-kafka` |

**Detection logic:**

```typescript
this.isNativeKafka = apiV4.type === 'NATIVE' && apiV4.listeners.some((listener) => listener.type === 'KAFKA');
```

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

Native Kafka endpoints display security protocol badges when configured. Protocols can be set at the endpoint level via `sharedConfigurationOverride.security.protocol` or inherited from the endpoint group's `sharedConfiguration.security.protocol`.

| Badge Text | Tooltip | Condition |
|:-----------|:--------|:----------|
| `{protocol}` (e.g., `SASL_SSL`) | "Security protocol override by endpoint configuration" | Native Kafka endpoint with `sharedConfigurationOverride.security.protocol` set |
| `{protocol}` | "Security protocol inherited from group configuration" | Native Kafka endpoint inheriting `sharedConfiguration.security.protocol` |

## Create an endpoint group

To create an endpoint group for a Native Kafka API:

1. Navigate to the API's endpoint groups configuration.
2. Click **Add Endpoint Group**.
3. The endpoint group type is pre-selected as `native-kafka`.
4. Configure the group name and optional shared security protocol settings.
5. Save the endpoint group.

Load balancer configuration is optional and can be left blank.

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

## Add an endpoint

To add an endpoint to a Native Kafka endpoint group:

1. Select the target endpoint group.
2. Click **Add Endpoint**.
3. Enter the endpoint name and bootstrap servers. Bootstrap servers are displayed in the **Bootstrap Servers** column.
4. (Optional) Configure security protocol overrides via `sharedConfigurationOverride.security.protocol`.
5. Save the endpoint.

The first endpoint in the first group is automatically designated as the default endpoint and receives a **Default** badge.

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**.

1. Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>

2. Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>

3. By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>

## Reorder endpoints

You can reorder endpoints within an endpoint group using drag-and-drop:

1. Click and hold the drag icon in the leftmost column of the endpoint table.
2. Drag the endpoint row to the desired position.
3. Release to drop.

The platform updates the API configuration and displays "Endpoint reordered successfully." Endpoint order determines priority, with the first endpoint serving as the default.

Endpoint reordering is disabled when:

* The API is in read-only mode.
* Another reordering operation is in progress.

If reordering fails, the platform displays an error message from the API response.

## Default endpoint designation

For Native Kafka APIs, the first endpoint in the first endpoint group is designated as the default endpoint. This endpoint receives a "Default" badge with the tooltip "The default endpoint used by the API is the first one." Endpoint order determines priority, making drag-and-drop reordering a critical configuration tool.

## Endpoint table display

The endpoint table displays the following columns:

| Column | Width | Visibility | Content |
|:-------|:------|:----------|:--------|
| Drag icon | 48px | Always visible | Drag handle for reordering endpoints |
| Name | — | Always visible | Endpoint name with optional **Default** badge for the first endpoint in the first group |
| Bootstrap Servers | — | Visible for Native Kafka APIs | Displays `endpoint.configuration.bootstrapServers` (renamed from "general" column) |
| Options | — | Visible when endpoints have options | Security protocol badges (e.g., `SASL_SSL`) with tooltips indicating override or inheritance |
| Weight | — | Hidden for Native Kafka APIs | Not applicable to Native APIs |
| Actions | 96px (right-aligned) | Always visible | Edit and delete actions |

The endpoint table uses `@angular/cdk/drag-drop` for drag-and-drop functionality. Column visibility is dynamically adjusted based on API type and endpoint configuration. Success messages ("Endpoint reordered successfully," "Endpoint group reordered successfully") are displayed after reordering operations. Error messages from the API are displayed if reordering fails. The general column header changes to "Bootstrap Servers" for Native Kafka and Message APIs, and "Target URL" for Proxy APIs.

## Load balancer validation

For Native Kafka APIs, load balancer configuration is optional. The platform automatically removes load balancer validation requirements when it detects a Native Kafka API. Native Kafka APIs do not require load balancer configuration.

| Property | Type | Requirement | Description |
|:---------|:-----|:-----------|:------------|
| `loadBalancerType` | FormControl | Optional for Native Kafka; required for all other API types | Load balancer type is not required for Native Kafka APIs; validation is removed automatically when `isNativeKafka === true` |

**Before:**

```typescript
loadBalancerType: new UntypedFormControl('', [Validators.required])
```

**After (Native Kafka):**

```typescript
loadBalancerType: new UntypedFormControl({ value: null, disabled: false }, [])
```

## Restrictions

* Endpoint reordering is disabled when the API is in read-only mode.
* Endpoint reordering is disabled while another reordering operation is in progress.
* `MCP_PROXY` APIs can't add endpoint groups or endpoints.
* The `weight` column is hidden for Native Kafka APIs (weighting is not supported).
* Load balancer badges are hidden for `native-kafka` endpoint groups.
* The **Default** badge is only displayed for the first endpoint in the first endpoint group of Native Kafka APIs.
