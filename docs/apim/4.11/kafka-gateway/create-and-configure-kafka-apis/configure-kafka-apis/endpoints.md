---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one endpoint group with a single endpoint. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Multi-tenant endpoint support

Multi-tenant endpoint support enables a single Kafka API definition to route traffic to different backend clusters based on the gateway's configured tenant identifier. This eliminates the need to duplicate API definitions across deployment zones (VPN, DMZ, cloud regions) while maintaining governance, analytics, and lifecycle operations in a single artifact. Platform administrators assign a tenant to each gateway node; the runtime automatically filters and activates only the endpoints tagged with that tenant.

### Tenant-based endpoint filtering

Each Kafka endpoint can be tagged with one or more tenant identifiers. At startup and during hot-reload, the gateway loads only endpoints whose tenant list is empty (shared) or contains the gateway's configured tenant. Endpoints that do not match are skipped entirely. If no endpoint remains after filtering, requests fail with a 503 error. There is no automatic fallback to untagged endpoints — fallback is achieved by explicitly defining at least one shared (untagged) endpoint in the group.

| Gateway Tenant | Endpoint Tenants | Match Result |
|:--------------|:-----------------|:-------------|
| Not configured | Any value or empty | ✅ Match (gateway participates in all endpoints) |
| Configured (for example, `"tenant-a"`) | `null` or `[]` | ✅ Match (shared endpoint) |
| Configured (for example, `"tenant-b"`) | Contains `"tenant-b"` | ✅ Match |
| Configured (for example, `"tenant-c"`) | Does not contain `"tenant-c"` | ❌ No Match |

### Endpoint selection

Within an endpoint group, the first endpoint matching the tenant filter is selected. If multiple endpoints match, only the first is used — there is no load balancing across tenant-filtered endpoints. This behavior aligns with the single-endpoint-per-group model for Kafka APIs.

### Shared endpoints

An endpoint with an empty or null tenant list is considered shared and matches any gateway, regardless of the gateway's tenant configuration. Shared endpoints serve as a safety net during gradual rollout or when legacy gateways haven't yet been assigned a tenant.

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

Before configuring Kafka API endpoints with multi-tenant support, ensure the following:

* Gravitee API Management platform with Kafka gateway support
* Tenant objects created via the Management API or Console (organization-scoped)
* Gateway nodes configured with a tenant identifier (or left unconfigured to participate in all endpoints)
* At least one Kafka endpoint defined in the API's endpoint group

## Gateway configuration

### Tenant identifier

| Property | Description | Example |
|:---------|:------------|:--------|
| `tenant` | Gateway tenant identifier used to filter endpoints. Omit to participate in all endpoints. | `"internal"`, `"external"`, `"eu-west"` |

The tenant value can be set via environment variable, system property, or `gravitee.yml`. Changing the tenant identifier refreshes the gateway's active endpoint set without requiring API redefinition.

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

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**. The Console endpoint table includes a **Tenants** column displaying comma-separated tenant names for each endpoint. The column is hidden if no endpoint in the group has tenants configured.

1. Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>

2. Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>

3. By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>

4. To assign tenant tags to the endpoint, select one or more tenants from the **Tenants** multi-select dropdown. The endpoint configuration form exposes a multi-select **Tenants** field populated from the organization's tenant list, with tenant descriptions shown as tooltips. Leave the tenant list empty to create a shared endpoint that matches any gateway.

## Example endpoint group configuration

The following example demonstrates a Kafka API endpoint group with tenant-specific endpoints and a shared fallback:

```json
{
  "endpointGroups": [
    {
      "name": "outbound-kafka",
      "type": "native-kafka",
      "endpoints": [
        {
          "name": "internal-cluster",
          "type": "native-kafka",
          "tenants": ["internal"],
          "configuration": {
            "bootstrapServers": "kafka-internal.local:9092"
          }
        },
        {
          "name": "external-cluster",
          "type": "native-kafka",
          "tenants": ["external"],
          "configuration": {
            "bootstrapServers": "kafka-external.cloud:9092"
          }
        },
        {
          "name": "shared-fallback",
          "type": "native-kafka",
          "tenants": [],
          "configuration": {
            "bootstrapServers": "kafka-shared.local:9092"
          }
        }
      ]
    }
  ]
}
```

## Restrictions

* If no endpoint matches the gateway's tenant after filtering, requests fail with `503 No endpoint available`. There is no automatic fallback to shared endpoints — fallback must be explicitly configured by including an untagged endpoint.
* Within an endpoint group, only the first tenant-matching endpoint is selected. Multiple matching endpoints are not load-balanced.
* Tenant filtering applies at gateway startup and hot-reload. Changing an endpoint's tenant tags requires redeploying the API or triggering a sync.
* Tenant identifiers are case-sensitive and must match exactly between the gateway configuration and endpoint tags.
* Health checks, metrics, and monitoring reflect only the tenant-eligible endpoints. Tenant-mismatched endpoints do not appear in operational views.
* Tenant objects must be created in the organization before they can be assigned to endpoints. Unknown tenant IDs are displayed as raw strings in the Console.
* When a gateway with a configured tenant encounters no matching endpoint, the error is logged at WARN level (not ERROR) and the request completes without propagating the exception further. The `KafkaNoApiEndpointFoundException` distinguishes between "no endpoint found for tenant" and "no endpoint found for API" scenarios.
