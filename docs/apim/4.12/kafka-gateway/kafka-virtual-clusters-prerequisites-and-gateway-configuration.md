# Kafka Virtual Clusters Prerequisites and Gateway Configuration

## Prerequisites

Before configuring Kafka Virtual Clusters, ensure the following requirements are met:

* **Minimum two Kafka Cluster entities** configured in the environment. Virtual clusters with a single backend provide no value over direct cluster references. A minimum of 2 backends is recommended to exercise the MESH multiplex. The practical ceiling is approximately 5–10 backends, as every consumer-group RPC fans out across all backends.
* **Broker ID constraints**: Each backend cluster must expose fewer than 10,000 brokers. Real broker IDs must be less than 10,000.
* **Maximum backend clusters**: Up to 214,748 backend clusters per virtual cluster.
* **Default Kafka domain** (for HOST routing mode): Configure a default Kafka domain in **Console → Organization → Entrypoints & Sharding Tags → Default Kafka Domain**. The gateway requires the `gravitee_kafka_routingHostMode_defaultDomain` property set so each API's `hostPrefix` maps to `<prefix>.<defaultDomain>:9092`.
* **Wildcard TLS certificate** (for HOST routing mode): A wildcard certificate covering `*.<defaultDomain>`.
* **CLUSTER permission**: Environment-scoped **CLUSTER** permission (READ + UPDATE) granted to users who will manage clusters. Configure in **Console → Organization → Roles → USER → CLUSTER**.
* **Native API permissions**: **NATIVE_LOG** and **NATIVE_ANALYTICS** API-scoped permissions granted to relevant roles. These permissions are automatically backfilled on built-in **OWNER** and **PRIMARY_OWNER** roles by the `NativeApiLogPermissionUpgrader`.

{% hint style="warning" %}
**Routing mode constraints:**

* mTLS plans force HOST routing mode. The SNI handshake is required for client-cert validation.
* You cannot mix secure plans (API Key, JWT, OAuth2, mTLS) with Keyless plan on the same API. Mixed Keyless + secure plans on one API is refused at API start with `KafkaServerUnsupportedSecureAndUnsecurePlansException`.
{% endhint %}

## Gateway Configuration

### Routing Mode

The gateway supports two routing modes, controlled by the `kafka.routingMode` property:

| Property | Values | Default | Description |
|:---------|:-------|:--------|:------------|
| `kafka.routingMode` | `host`, `port` | `host` | **host**: Single bootstrap port (9092) for all APIs. Routing by TLS SNI hostname. **port**: Each plan gets a dedicated bootstrap port. Routing by local listening port. mTLS plans force HOST mode. |

**HOST mode** (default):
* Single bootstrap port for all APIs (9092)
* Routing relies on TLS SNI hostname
* Gateway dispatches on `<apiPrefix>.<defaultDomain>` and `broker-<N>-<apiPrefix>.<defaultDomain>`
* Requires a wildcard TLS certificate covering `*.<defaultDomain>`
* Most common deployment model

**PORT mode**:
* Each plan gets a dedicated bootstrap port and broker-port range
* Routing by local listening port (no SNI dispatch)
* Use when wildcard certificates are not acceptable or when the client cannot perform SNI
* Does not require wildcard certificates

{% hint style="warning" %}
mTLS plans force HOST mode regardless of the `kafka.routingMode` setting. The SNI handshake is required for client-cert validation.
{% endhint %}
