---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one or more endpoint groups, with each group containing one or more endpoints. The **Endpoints** section lets you configure and manage your Kafka endpoint groups and endpoints.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

Gravitee Kafka Native APIs support advanced endpoint management through two key enhancements:

1. **Multi-endpoint support**: Configure multiple Kafka endpoints within a single API using endpoint groups.
2. **Tenant-based endpoint selection**: Enable automatic endpoint selection based on gateway tenant configuration.

These features enable organizations to manage complex Kafka deployments—such as multi-region routing, disaster recovery scenarios, and planned cluster migrations—without duplicating API definitions.

<!-- GAP: No version number or release information provided for when these features became available -->
<!-- GAP: No indication whether tenant management is Enterprise-only or available in Community Edition -->

## Key concepts

### Endpoint groups

An **Endpoint Group** organizes and prioritizes multiple Kafka endpoints within a single API. Each Kafka Native API can contain multiple endpoint groups, and each group can contain multiple endpoints. Endpoint groups are primarily used to organize endpoints and determine selection priority.

The gateway evaluates endpoint groups in order and selects the first valid endpoint from the first group based on tenant matching and list order.

### Endpoints

Each endpoint represents a distinct Kafka cluster configuration, including bootstrap servers and security settings. Endpoints can inherit configuration from their endpoint group or override it with custom settings.

A native endpoint group must contain at least one endpoint. Endpoint names must be unique within a group.

### Tenants

A **tenant** is an organization-scoped identifier that binds gateway nodes to specific endpoint subsets. Tenants are configured at the organization level and work similarly to tenants used for classic APIs in APIM.

- Gateways can be assigned a tenant identifier to route traffic to tenant-specific endpoints.
- Endpoints can be tagged with one or more tenants to restrict which gateways can use them.
- Endpoints with no tenant configuration are considered shared and available to all gateways.

Tenants are organization-scoped identifiers managed via the Management API and Console. Each endpoint can be associated with one or more tenants, or left untagged to serve as a shared fallback.

#### Tenant configuration

A tenant can be selected in the gateway general configuration. Each gateway node can be assigned a tenant identifier through:

- Environment variable
- System property `gravitee.tenant`
- `tenant` field in `gravitee.yml`

Omitting the tenant identifier means the node participates in all endpoints and can use any shared endpoint.

### Objectives

The multi-endpoint and tenant management features enable:

- **Multiple Kafka endpoints** within a single API definition
- **Tenant-based endpoint selection** by the gateway at runtime
- **Automatic endpoint determination** based on gateway tenant configuration and defined rules
- **Simplified governance** by consolidating multiple backend clusters into a single API artifact

Multi-endpoint configuration supports scenarios such as:

- **Planned migration or disaster recovery**: Pre-configure primary and backup Kafka clusters, then switch between them by reordering endpoints or marking one as active.
- **Regional routing with tenants**: Deploy the same API across multiple regions (e.g., EU and APAC), with each region using a tenant-scoped endpoint. Gateways automatically select the endpoint matching their configured tenant.
- **Pre-provisioned backup**: Maintain both primary and backup endpoints in a single API definition. If a switch is required, promote the backup endpoint and redeploy.

## Endpoint selection mechanism

The gateway selects a Kafka endpoint at runtime based on the gateway's tenant configuration and the endpoint group's structure. At startup and during hot-reload, gateways activate only the Kafka connectors whose tenant list is empty or contains the configured tenant. Tenant-mismatched connectors are ignored.

### Selection algorithm

The gateway automatically selects the Kafka endpoint to use at runtime according to the following rules:

1. **Dynamic routing attribute** (optional): If a policy sets a context attribute matching a configured endpoint name, that endpoint is used.
2. **Gateway with tenant configured**: The gateway selects the first valid endpoint from the first endpoint group based on tenant matching.
3. **Gateway without tenant configured**: The gateway selects the first endpoint from the first endpoint group. No tenant-based filtering is applied.

### Endpoint validity criteria

An endpoint is considered valid if:

* It has no tenant configuration (generic endpoint usable by all gateways), **OR**
* Its tenant configuration exactly matches the tenant configured on the gateway.

{% hint style="warning" %}
Endpoints with tenant configurations that don't match the gateway's tenant are ignored. If no valid endpoint is found after filtering, the API does not run on that gateway.
{% endhint %}

### Priority order

* Only the first Endpoint Group is considered in the current implementation.
* Endpoints are evaluated in the order they appear within the group.
* The first valid endpoint is selected.

{% hint style="info" %}
Future releases may introduce dynamic routing policies that enable selection of endpoints from other Endpoint Groups.
{% endhint %}

### Failure mode

If no connector is available after tenant filtering, the gateway responds with `503 - No endpoint available`. This signals a tenant coverage gap rather than silently falling back to an unintended endpoint.

To avoid this scenario, include at least one endpoint with no tenant configuration (shared endpoint) in the Endpoint Group to serve as a fallback for gateways without tenant configuration or with non-matching tenants.

### Example

```
[Kafka API | Group: outbound]
  - Endpoint A (tenants=[eu])
  - Endpoint B (tenants=[apac])
  - Endpoint C (tenants=[])  ← shared fallback

[Gateway tenant=eu] → Endpoint A
[Gateway tenant=apac] → Endpoint B
[Gateway no tenant] → Endpoint C
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

## Multi-endpoint configuration

Kafka Native APIs support multiple Endpoint Groups, with multiple Endpoints per group. This allows you to configure alternate Kafka clusters (for disaster recovery, migration, or regional routing) behind a single API.

### Adding multiple endpoints

To add multiple endpoints to a Kafka API:

1. Navigate to the **Endpoints** section of your Kafka API.
2. Click **Add Endpoint** within your endpoint group.
3. Configure each endpoint with a unique name and bootstrap server list.
4. Reorder endpoints using drag-and-drop or explicit controls. The topmost endpoint is considered active when no tenant or dynamic routing applies.

## Tenant-based endpoint selection

Endpoints can be generic (no tenant configuration) or associated with one or more specific tenants. The gateway automatically selects the appropriate endpoint at runtime based on tenant matching rules.

### Configuring tenants on endpoints

To associate an endpoint with specific tenants:

1. Edit the endpoint by clicking the pencil icon under **ACTIONS**.
2. Select the **General** tab.
3. Use the tenant picker to tag the endpoint with one or more tenants.
4. Leave the tenant list empty to declare a shared fallback endpoint.

Tenants are configurable in the organization settings and work similarly to tenants used for v4 proxy APIs.

<!-- GAP: No information provided about UI location or procedure for assigning tenants to Kafka endpoints in the Console -->

### Endpoint tenant assignment

When configuring a Kafka endpoint, you can:

- Leave the tenant list empty to declare a shared endpoint available to all gateways
- Tag the endpoint with one or more tenants to bind it to specific gateway fleets

### Operational considerations

- **Fallback strategy:** To ensure availability, maintain at least one shared (untagged) endpoint in the group as a safety net
- **Monitoring alignment:** Health checks, heartbeat, and metrics only operate on the filtered set of endpoints, so monitoring aligns with what the node can actually reach
- **Tenant visibility:** Tenant tags are visible wherever Kafka endpoints are displayed (Console lists, API descriptors) so platform teams can verify alignment between definitions and gateway placement

### Switching endpoints

To manually switch the active endpoint:

1. Reorder endpoints by moving the desired endpoint to the top of the list, or use the **Set Active** action if available.
2. Save and deploy the changes.
3. The gateway gracefully closes existing connections for the affected API.
4. Kafka clients automatically retry and reconnect to the newly selected endpoint.

{% hint style="warning" %}
The Gateway does not perform automatic failover or health checks. Kafka clients handle reconnection. Switching the active endpoint closes existing connections, and clients retry and reconnect to the newly selected endpoint.
{% endhint %}

## Routing vs failover

The gateway provides deterministic endpoint selection based on tenant matching and list order. It does **not** implement automatic failover or health checks.

- **No automatic failover**: If an endpoint becomes unavailable, the gateway does not automatically switch to another endpoint. Kafka clients handle broker membership and reconnection.
- **No health checks**: The gateway does not monitor endpoint availability or perform circuit-breaking.
- **No load balancing**: The gateway does not distribute traffic across multiple endpoints using round-robin or weighted algorithms.

For disaster recovery or planned migrations, you must explicitly switch endpoints by reordering them or using the **Set Active** action, then redeploying the API.

### Cross-cluster considerations

Switching between Kafka clusters requires careful planning:

- Topic and offset alignment is customer-owned. The gateway does not replicate data or migrate offsets between clusters.
- Ensure clients can handle reconnection and offset management when switching clusters.

## Edit the endpoint group

Gravitee assigns each Kafka API endpoint group the default name **Default Broker group**. To edit the endpoint group, complete the following steps:

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