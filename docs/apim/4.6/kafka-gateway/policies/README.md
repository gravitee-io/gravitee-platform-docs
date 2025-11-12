# Policies

## Introduction

Gravitee policies are customizable rules or logic the Gateway executes during an API transaction. They modify the behavior of the request or response handled by the APIM Gateway to fulfill business rules during request/response processing. Policies are used to secure APIs, transform data, route traffic, restrict access, customize performance, or monitor transactions.&#x20;

Gravitee supports the following Kafka policies, which can be applied to Kafka APIs.

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><a href="kafka-acl.md">Kafka ACL</a></td><td></td><td></td></tr><tr><td><a href="kafka-topic-mapping.md">Kafka Topic Mapping</a></td><td></td><td></td></tr><tr><td><a href="kafka-quota.md">Kafka Quota</a></td><td></td><td></td></tr></tbody></table>

## Policy phases

The request and response of a Kafka API transaction are broken up into the following phases:

* **Connect:** Policies are executed after plan selection and authentication on the Gateway, but before the client connects to the upstream broker.&#x20;
* **Interact:** Policies with a global scope (e.g., topic mapping) are executed on all interactions between the client and the Gateway.&#x20;
* **Publish:** Specific policies acting at the message level are applied to each produced record.
* **Subscribe:** Specific policies acting at the message level are applied to each fetched record.

Which Kafka policies can be applied to each phase is summarized below:

<table><thead><tr><th>Policy</th><th data-type="checkbox">Connect</th><th data-type="checkbox">Interact</th><th data-type="checkbox">Publish</th><th data-type="checkbox">Subscribe</th></tr></thead><tbody><tr><td>Kafka ACL</td><td>false</td><td>true</td><td>false</td><td>false</td></tr><tr><td>Kafka Topic Mapping</td><td>false</td><td>true</td><td>false</td><td>false</td></tr><tr><td>Kafka Quota</td><td>false</td><td>false</td><td>true</td><td>true</td></tr></tbody></table>

Kafka policies can be applied to these phases in policy chains of arbitrary length.

## Configuration

Policies are scoped to different API consumers through flows. Flows are policy enforcement sequences that control where, and under what conditions, one or more policies act on an API transaction. The APIM Console includes a Gravitee Policy Studio where you can design flows to protect or transform how your Kafka APIs are consumed.&#x20;

To learn how to configure flows and policies for your Kafka APIs, click [here](docs/apim/4.6/kafka-gateway/configure-kafka-apis/policies.md).
