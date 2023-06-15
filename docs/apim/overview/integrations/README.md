---
description: >-
  Learn more about how Gravitee integrates with your larger enterprise tech
  ecosystem
---

# Integrations

## Gravitee API Management integrations

Please see the below sections and tables that outline major integrations that Gravitee API Management offers with other enterprise tooling.

### Event brokers

<table><thead><tr><th width="144">Event broker</th><th>Integration description</th><th>Plugin or add-on required</th></tr></thead><tbody><tr><td>Kafka</td><td>Gravitee can expose backend Kafka data sources as <a href="../../guides/create-apis/how-to.md">supported client-side APIs.</a></td><td>Gateway Kafka Endpoint connector</td></tr><tr><td>Confluent</td><td>Gravitee can expose backend Confluent data sources as <a href="../../guides/create-apis/how-to.md">supported client-side APIs.</a> Gravitee also supports Confluent Schema registry as schema validation resource.</td><td>Gateway Kafka Endpoint connector<br><br>Various serialization and deserialization policies</td></tr><tr><td>Solace</td><td>Gravitee can expose backend Solace event APIs as <a href="../../guides/create-apis/how-to.md">supported client-side APIs.</a> Gravitee can also auto-import Solace event APIs.</td><td>Management Solace Sync Service plugin<br><br>Gateway Solace Endpoint Connector</td></tr><tr><td>HiveMQ</td><td>Gravitee can expose backend MQTT data sources as <a href="../../guides/create-apis/how-to.md">supported client-side APIs.</a></td><td>Gateway MQTT Endpoint Connector</td></tr><tr><td>Mosquito</td><td>Gravitee can expose backend MQTT data sources as <a href="../../guides/create-apis/how-to.md">supported client-side APIs.</a></td><td>Gateway MQTT Endpoint Connector</td></tr><tr><td>(Other MQTT broker running MQTT 5)</td><td>Gravitee can expose backend MQTT data sources as <a href="../../guides/create-apis/how-to.md">supported client-side APIs.</a></td><td>Gateway MQTT Endpoint Connector</td></tr></tbody></table>

## APM and Observability

<table><thead><tr><th width="144">Monitoring solution</th><th>Integration description</th><th>Plugin or add-on required</th></tr></thead><tbody><tr><td>Splunk</td><td>Gravitee can push API metrics and monitoring data to Splunk for visualization in Splunk dashboards.</td><td>File reporter plugin</td></tr><tr><td>Datadog</td><td>Gravitee can push API metrics and monitoring data to Datadog for visualization in Datadog dashboards.</td><td>Datadog reporter plugin<br><br>File reporter plugin (less advanced version)</td></tr><tr><td>Dynatrace</td><td>Gravitee can push API metrics and monitoring data to Dynatrace for visualization in Dynatrace dashboards.</td><td>File reporter plugin</td></tr><tr><td>Prometheus</td><td>Gravitee can push API metrics and monitoring data to Prometheus for visualization in Prometheus dashboards.</td><td>File reporter plugin</td></tr></tbody></table>

## Service Discovery

<table><thead><tr><th width="144">Solution</th><th>Integration description</th><th>Plugin or add-on required</th></tr></thead><tbody><tr><td>Hashcorp Consul</td><td>Gravitee can </td><td>File reporter plugin</td></tr></tbody></table>
