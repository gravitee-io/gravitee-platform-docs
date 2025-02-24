= Gravitee Kafka Policy Quota

== Description

The Gravitee Kafka Policy Quota is a policy designed to enforce quotas on Kafka messages.
It allows you to define limits on the amount of data that can be produced or consumed by a Kafka client.
This policy can be used to protect your Kafka cluster from being overwhelmed by a single client.

== Phases

This policy can be applied in the Publish and/or Subscribe phase.

== Configuration

You can configure the policy with the following options:

[cols="5*", options=header]
|===
^| Property
^| Required
^| Description
^| Type
^| Default

| key
| No
| Key to identify a consumer against whom the quota will be applied. Leave it empty to use the default behavior (plan/subscription pair). Supports EL.
| String
|

| useKeyOnly
| No
| Only uses the custom key to identify the consumer, regardless of the subscription and plan.
| Boolean
| false

| limit.value
| No
| Static value defining the limit of data passed through the proxy (this limit is used if the value > 0).
| Integer
| 0

| limit.dynamicValue
| No
| Dynamic value defining the limit of data passed through the proxy (this limit is used if the value > 0). The dynamic value is based on EL expressions.
| String
|

| limit.unit
| No
| Defines the unit of the limit.
| String
| Bytes
|===
