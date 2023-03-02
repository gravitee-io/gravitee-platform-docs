# APIM 3.20.x changelog

## APIM 3.20.x changelog

This page contains the changelog entries for APIM 3.20.0 and any future minor APIM 3.20.x releases.

## About upgrades

For upgrade instructions, please refer to the [APIM Migration Guide](installation-guide/installation-guide-migration.md).

!!! warning

```
**Important:** If you plan to skip versions when you upgrade, ensure that you read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.
```

## APIM - 3.20 (2023-01-05)

### API Management - Console

* Brand new menu to unify the experience between all Gravitee products
* Introducing v1 APIs reaching end of support and help users migrate to v2
* APIs list page navigation enhancements
* APIs are read-only if managed by our GKO (Gravitee Kubernetes Operator)
* Allow to delete a media using the Management API
* \[V4 BETA M-API] Manage v4 APIs subscriptions as an API Publisher & an API Consumer

[Event-Native API Management (Beta)](../v4-beta/v4-beta-event-native-apim-introduction.md)

* Endpoint - Kafka Connector Advanced (EE)
  * Ability to connect to a secured Kafka cluster
  * Introducing RESUME & LIMIT capabilities for QoS (Quality of Service)
* Endpoint - MQTT5 Connector
  * Consume messages from a MQTT5 event-broker
  * Push messages to a MQTT5 event-broker
* Endpoint - MQTT5 Connector Advanced (EE)
  * Ability to connect to a secured MQTT5 event-broker
  * Introducing QoS (Quality of Service) capabilities
* Entrypoint - Webhook connector
  * Create an API with a webhook entrypoint
  * Subscribe to an API with a webhook entrypoint
  * Receive messages on my callback url
* Introducing foundation support for sync API on v4 - httpproxy entrypoint & endpoint
* Message filtering policy
* Support conditions on messages

[Gravitee Kubernetes Operator (Beta)](../kubernetes/apim-kubernetes-operator-overview.md)

* CRD Lifecycle - Apply changes related CRDs on update
* Store credentials in K8 secrets
* Export a complex API and import it in a new/same environment
* Manage resources as CRD and reuse them in several APIs
