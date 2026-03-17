---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Native Kafka APIs can define multiple endpoints within an endpoint group, enabling pre-configured cluster alternatives for disaster recovery, migration, and regional routing scenarios. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Multi-tenant endpoint support

Multi-tenant endpoint support enables a single Kafka API definition to route traffic to different backend clusters based on the gateway's configured tenant identifier. This eliminates the need to duplicate API definitions across deployment zones (VPN, DMZ, cloud regions) while maintaining governance, analytics, and lifecycle operations in a single artifact. Platform administrators assign a tenant to each gateway node; the runtime automatically filters and activates only the endpoints tagged with that tenant.

### Tenant-based endpoint filtering

Each Kafka endpoint can be tagged with one or more tenant identifiers. At startup and during hot-reload, the gateway loads only endpoints whose tenant list is empty (shared) or contains the gateway's configured tenant. Endpoints that don't match are skipped entirely. Shared (untagged) endpoints are always included in the filtered set alongside tenant-specific endpoints. If all endpoints are tenant-specific and none match the gateway's tenant, the gateway can't route to the API. Connections fail in this scenario.

| Gateway Tenant | Endpoint Tenants | Match Result |
|:--------------|:-----------------|:-------------|
| Not configured | Any value or empty | Match (gateway participates in all endpoints) |
| Configured (for example, `"tenant-a"`) | `null` or `[]` | Match (shared endpoint) |
| Configured (for example, `"tenant-b"`) | Contains `"tenant-b"` | Match |
| Configured (for example, `"tenant-c"`) | Doesn't contain `"tenant-c"` | No Match |

### Endpoint selection

Only the first endpoint group is considered for tenant resolution. If there are multiple endpoint groups, the gateway uses the first group and applies the tenant mechanism if configured. Other groups are ignored.

### Shared endpoints

An endpoint with an empty or null tenant list is considered shared and always matches any gateway, regardless of the gateway's tenant configuration. Shared endpoints are always included in the filtered set, making them useful during gradual rollout or when legacy gateways haven't yet been assigned a tenant.

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

## Create an endpoint group

When creating a Native Kafka API, the endpoint group type is automatically set to `native-kafka`. The load balancing algorithm field isn't displayed for Native Kafka APIs.

To create an endpoint group:

1. In the left sidebar, click **Endpoints**.
2. Click **Add endpoint group**.
3. Enter a **Name** for the endpoint group. The name can't contain `:` and must be unique across all endpoint groups and endpoints.
4. Click **Validate general information**.
5. Configure the endpoint group settings on the **Configuration** step.
6. Click **Create endpoint group**.

A default endpoint named `{groupName} default endpoint` is automatically created and inherits the group's configuration.

Validation requires the group to contain at least one endpoint. Endpoint names must be unique within the group.

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

## Reorder endpoints

To change the active endpoint, reorder endpoints in the group by dragging them in the Console. The first endpoint in the list becomes the active endpoint. Deploying this change triggers a graceful shutdown of existing connections for the API on the gateways, allowing Kafka clients to retry and reconnect to the newly selected endpoint.

{% hint style="warning" %}
Reordering is disabled in read-only mode and while a reordering operation is in progress.
{% endhint %}

## Console display

The Console displays endpoint groups and endpoints with the following columns:

| Column | Description | Displayed for |
|:-------|:------------|:--------------|
| Drag icon | Drag handle for reordering | All endpoints |
| Name | Endpoint name with **Default** badge for the first endpoint in the first group | All endpoints |
| Bootstrap Servers | Kafka bootstrap servers from the endpoint configuration | Native Kafka endpoints |
| Security Protocol | Security protocol badge with tooltip indicating inheritance or override | Native Kafka endpoints with security configuration |
| Actions | Overflow menu (Rename, Duplicate, Delete) | All endpoints |

{% hint style="info" %}
The weight column isn't displayed for Native Kafka APIs.
{% endhint %}

The **Options** column is hidden if no endpoints in the group have configured options.

Security protocol badges display tooltips:

* **Inherited**: "Security protocol inherited from group configuration"
* **Override**: "Security protocol override by endpoint configuration"

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

* If all endpoints are tenant-specific and none match the gateway's tenant, the gateway can't route to the API. Include at least one shared (untagged) endpoint to ensure the API remains accessible to all gateways.
* Only the first endpoint group is considered for tenant resolution. Additional endpoint groups are ignored.
* Tenant filtering applies at gateway startup and hot-reload. Changing an endpoint's tenant tags requires redeploying the API or triggering a sync.
* Tenant identifiers are case-sensitive and must match exactly between the gateway configuration and endpoint tags.
* Tenant objects must be created in the organization before they can be assigned to endpoints.
