= Gravitee Kafka Transform Key Policy

== Description

The Gravitee Kafka Transform Key Policy is a policy designed to add a custom Kafka message key to your messages, so that you can partition how you want and generally do things like order the transactions.

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
| Custom kafka message key for your messages. Supports EL.
| String
|

| setUnresolvedKeysToNull
| No
| When enabled, and the expression results in an error, set the key to null. Otherwise, throw an error.
| Boolean
| false
|===