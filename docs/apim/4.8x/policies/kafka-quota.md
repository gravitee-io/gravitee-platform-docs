---
hidden: true
---

# Kafka Quota

## Overview <a href="#user-content-description" id="user-content-description"></a>

The Gravitee Kafka Policy Quota is a policy designed to enforce quotas on Kafka messages. It allows you to define limits on the amount of data that can be produced or consumed by a Kafka client. This policy can be used to protect your Kafka cluster from being overwhelmed by a single client.

<figure><img src="../.gitbook/assets/image (180).png" alt=""><figcaption><p>Kafka Quota Policy UI</p></figcaption></figure>

## Phases <a href="#user-content-phases" id="user-content-phases"></a>

This policy can be applied in the Publish and/or Subscribe phase.

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

<table><thead><tr><th width="231">Property</th><th>Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>key</td><td>No</td><td>Key to identify a consumer against whom the quota will be applied. Leave it empty to use the default behavior (plan/subscription pair). Supports EL.</td><td>String</td><td></td></tr><tr><td>useKeyOnly</td><td>No</td><td>Only uses the custom key to identify the consumer, regardless of the subscription and plan.</td><td>Boolean</td><td>false</td></tr><tr><td>limit.value</td><td>No</td><td>Static value defining the limit of data passed through the proxy (this limit is used if the value > 0).</td><td>Integer</td><td>0</td></tr><tr><td>limit.dynamicValue</td><td>No</td><td>Dynamic value defining the limit of data passed through the proxy (this limit is used if the value > 0). The dynamic value is based on EL expressions.</td><td>String</td><td></td></tr><tr><td>limit.unit</td><td>No</td><td>Defines the unit of the limit.</td><td>String</td><td>Bytes</td></tr></tbody></table>
