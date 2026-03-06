---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Native Kafka APIs support full endpoint group and endpoint lifecycle management, including creation, editing, deletion, and drag-and-drop reordering. This feature enables administrators to configure multiple Kafka bootstrap servers and manage endpoint priority without load balancer constraints.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Native Kafka API detection

An API is classified as Native Kafka when `api.type === 'NATIVE'` and at least one listener has `type === 'KAFKA'`. This classification determines which endpoint group types are available and which validation rules apply.

## Default endpoint designation

The first endpoint in the first endpoint group of a Native Kafka API is automatically designated as the "Default" endpoint. This endpoint receives a visual badge in the UI with the tooltip "The default endpoint used by the API is the first one."

## Endpoint group type auto-selection

When creating a new endpoint group, the system automatically selects the appropriate type based on the API configuration:

| API Type | Auto-Selected Endpoint Group Type |
|:---------|:----------------------------------|
| `PROXY` | `http-proxy` |
| `LLM_PROXY` | `llm-proxy` |
| `NATIVE` (with Kafka listener) | `native-kafka` |

## Prerequisites

Before configuring Native Kafka API endpoints, ensure the following:

* API must be configured with `type: NATIVE`
* At least one listener with `type: KAFKA` must exist
* User must have permissions to modify API endpoint configuration

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

## Endpoint group properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Endpoint group identifier (required) | `"primary-kafka-cluster"` |
| `type` | Must be `native-kafka` for Native Kafka APIs | `"native-kafka"` |
| `loadBalancer.type` | Optional for Native Kafka endpoint groups | `null` |
| `sharedConfiguration` | Group-level Kafka security settings | `{}` |

## Endpoint properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Endpoint identifier (required) | `"primary-broker"` |
| `configuration.bootstrapServers` | Kafka broker addresses (required) | `"kafka-1.example.com:9092,kafka-2.example.com:9092"` |
| `configuration.securityProtocol` | Optional endpoint-level security override | `"SASL_SSL"` |

## Create an endpoint group

1. Navigate to the API's endpoint configuration and select **Add Endpoint Group**.
2. The system auto-selects `native-kafka` as the endpoint group type.
3. Provide a group name and configure at least one endpoint with `bootstrapServers`.
4. The load balancer type field is optional and may be left empty.
5. Save the endpoint group to make it available for API traffic routing.

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

1. Click and hold the drag handle icon next to the endpoint name.
2. Drag the endpoint to the desired position within the group.
3. Release to apply the new order.

The system updates the API configuration automatically. A success message confirms the reorder operation.

