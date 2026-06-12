# Managing Topics, Partitions, Configurations, and Admin Operations

## Key Concepts

### DELEGATE_TO_BROKER SASL Mechanism

The DELEGATE_TO_BROKER mechanism passes the client's SASL handshake through to the backend broker as-is. The gateway does not interpret or validate the SASL exchange — the backend broker handles authentication directly. This mechanism requires no additional configuration fields: the schema definition sets `additionalProperties: false`, meaning no JAAS config, credentials, or other fields are permitted when this mechanism is selected.

### Kafka Cluster Entity

A Kafka Cluster is a reusable connection profile to a real Kafka backend. Each cluster owns a name and one or more connections, where each connection specifies bootstrap servers and security settings (PLAINTEXT, SSL, SASL_PLAINTEXT, or SASL_SSL). Multiple APIs can reference the same cluster — changes to the cluster propagate to all referencing APIs.

A single cluster can contain multiple connections to model different listeners on the same backend — for example, port 9091 PLAINTEXT for internal clients and port 9095 SASL_SSL for external partners. APIs referencing the cluster can select the appropriate connection without duplicating the cluster entity.

### Conditional Display Logic

SASL configuration fields appear only when the security protocol is SASL_PLAINTEXT or SASL_SSL. SSL configuration fields appear only when the security protocol is SASL_SSL or SSL. The form uses relative JSON path references (`../protocol`) to evaluate these conditions. Previously, the form used absolute path references (`value.security.protocol`), which prevented correct conditional rendering. This fix affects only form rendering logic in the UI and does not require data migration for existing Kafka cluster configurations.

## Gateway Configuration

For HOST routing mode (the default), configure the **Default Kafka Domain** at **Console → Organization → Entrypoints & Sharding Tags**. The gateway maps each API's host prefix to `<prefix>.<defaultDomain>:9092`. mTLS plans require HOST mode because the SNI handshake is required for client certificate validation.
