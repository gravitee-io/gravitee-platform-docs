---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one endpoint group with a single endpoint. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Multi-tenant endpoint support

Multi-tenant endpoint support enables a single Kafka API definition to route traffic to different backend Kafka clusters based on the gateway's tenant configuration. This allows platform operators to deploy one API across multiple gateway instances, each serving a distinct tenant (e.g., internal, external, partner) without duplicating API definitions.

{% hint style="info" %}
Multi-tenant endpoint support requires configuring tenant identifiers at the gateway level and mapping them to specific backend Kafka clusters within the API definition.
{% endhint %}

### Tenant matching rules

The gateway evaluates its configured tenant identifier against each endpoint's tenant list. The following table describes the matching behavior:

| Gateway Tenant | Endpoint Tenants | Match Result |
|:---------------|:-----------------|:-------------|
| Not configured | Any value | ✅ Match |
| Configured (e.g., "tenant-a") | `null` or `[]` | ✅ Match |
| Configured (e.g., "tenant-a") | Contains "tenant-a" | ✅ Match |
| Configured (e.g., "tenant-c") | Does NOT contain "tenant-c" | ❌ No Match |

The gateway selects the first endpoint that satisfies the tenant filter. If no endpoint matches, the request fails with a `KafkaNoApiEndpointFoundException`.

### Gateway configuration

Configure the gateway-level tenant identifier to enable tenant-based endpoint filtering. If omitted, the gateway matches all endpoints regardless of tenant configuration.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tenant` | String | Not set | Gateway-level tenant identifier used to filter endpoints. If omitted, gateway matches all endpoints. |

Configure the tenant identifier in `gravitee.yml`:

```yaml
tenant: internal
```

### Restrictions

Multi-tenant endpoint support has the following limitations:

* **No load balancing across tenant-matched endpoints:** Only the first matching endpoint is selected. If multiple endpoints match the gateway's tenant configuration, the gateway uses the first match and does not distribute requests across them.
* **Immediate failure on tenant mismatch:** If no endpoint matches the gateway's tenant, the request fails immediately with `KafkaNoApiEndpointFoundException`.
* **Case-sensitive matching:** Tenant matching is case-sensitive. A gateway configured with `tenant: "Internal"` will not match an endpoint with `tenants: ["internal"]`.
* **Restart required for tenant configuration changes:** Changing a gateway's tenant configuration requires a restart to take effect.

### Error handling

When no endpoint matches the gateway's tenant configuration, the gateway throws a `KafkaNoApiEndpointFoundException`. This exception is logged at WARN level with one of the following messages:

* When tenant is configured: `No endpoint found for tenant: {tenantValue}`
* When tenant is not configured: `No endpoint found for api`

Error logging for missing endpoints uses WARN level when caused by tenant mismatch, ERROR level for other endpoint creation failures.

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

### Tenant assignment

Use the `tenants` property to control which gateway tenants can route traffic to this endpoint.

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `tenants` | Array of strings | List of tenant identifiers that can route to this endpoint. If omitted or empty, the endpoint matches any gateway tenant. | `["internal", "partner"]` |

To configure tenant assignment:

1. Navigate to the endpoint configuration form in the Management Console.
2. Use the multi-select dropdown to assign tenants to the endpoint.
   * The dropdown displays tenant names with descriptions.
   * If a tenant is deleted, the UI displays the tenant ID instead.

{% hint style="info" %}
If the `tenants` property is omitted or empty, the endpoint will match any gateway tenant.
{% endhint %}

## Create a multi-tenant Kafka API

Define a Kafka API with multiple endpoints in a single endpoint group, each tagged with one or more tenant identifiers.

### Prerequisites

Before configuring multi-tenant Kafka endpoints, ensure the following requirements are met:

* Gravitee API Management 4.x with Native Kafka reactor support
* Gateway instances configured with distinct tenant identifiers (if tenant isolation is required)
* Kafka API definition with Native Kafka endpoint groups

### Configuration steps

1. In the API definition, create a Native Kafka endpoint group.
2. Add an endpoint for each backend Kafka cluster.
   * Set the `tenants` array to the tenant identifiers that should route to that cluster. For example, `["internal"]` for an internal-facing cluster.
3. Configure each endpoint's `bootstrapServers` to point to the appropriate Kafka broker.
4. Deploy the API to multiple gateway instances, each configured with a different `tenant` value.

The gateway automatically selects the matching endpoint based on its tenant configuration.

### Example endpoint group configuration

```json
{
  "endpointGroups": [
    {
      "name": "multi-tenant-group",
      "type": "native-kafka",
      "endpoints": [
        {
          "name": "internal-endpoint",
          "type": "native-kafka",
          "tenants": ["internal"],
          "configuration": {
            "bootstrapServers": "internal-kafka.example.com:9093"
          }
        },
        {
          "name": "external-endpoint",
          "type": "native-kafka",
          "tenants": ["external"],
          "configuration": {
            "bootstrapServers": "external-kafka.example.com:9093"
          }
        }
      ]
    }
  ]
}
```

## Management Console UI changes

The Management Console endpoint groups table includes a **Tenants** column displaying comma-separated tenant names for each endpoint. The column is hidden if no endpoints in the group have tenants configured. The endpoint configuration form's tenant selector is always visible.


