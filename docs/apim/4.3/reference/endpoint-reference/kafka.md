---
description: This page contains the technical details of the Kafka endpoint plugin
---

# Kafka

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/gravitee-apim-enterprise-edition/README.md)**.**
{% endhint %}

## Overview

Use this endpoint to publish and/or subscribe to events in Kafka via web-friendly protocols such as HTTP or WebSocket. The reactive Gateway mediates the protocol between the client and the backend. Refer to the following sections for additional details.

* [Quality of Service](kafka.md#user-content-quality-of-service)
* [Compatibility matrix](kafka.md#user-content-compatibility-matrix)
* [Endpoint identifier](kafka.md#user-content-endpoint-identifier)
* [Endpoint configuration](kafka.md#user-content-endpoint-configuration)
* [Using SASL OAUTHBEARER](kafka.md#user-content-using-sasl-oauthbearer)
* [Using SASL\_AWS\_MSK\_IAM](kafka.md#user-content-using-sasl-aws\_msk\_iam)

## Quality Of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

<table><thead><tr><th width="159.99999999999997">QoS</th><th width="131">Delivery</th><th>Description</th></tr></thead><tbody><tr><td>None</td><td>Unwarranted</td><td>Improve throughput by removing auto commit</td></tr><tr><td>Balanced</td><td>0, 1 or n</td><td>Used well-knowing consumer group and offsets mechanism to balance between performances and quality</td></tr><tr><td>At-Best</td><td>0, 1 or n</td><td>Almost the same as <em>Balanced</em> but doing our best to delivery message once only but depending on entrypoint could rely on extra features to ensure which was the last message sent.</td></tr><tr><td>At-Most-Once</td><td>0 or 1</td><td>Depending on the entrypoint, this level could introduce performance degradation by forcing consumer to commit each message to ensure messages are sent 0 or 1 time.</td></tr><tr><td>At-Least-Once</td><td>1 or n</td><td>Depending on the entrypoint, this level could introduce performance degradation by forcing consumer to acknowledge each message to ensure messages are sent 1 or multiple times.</td></tr></tbody></table>

## Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version    |
| -------------- | --------------- |
| 1.x to 2.1.4   | 3.20.x to 4.0.4 |
| 2.2.0 and up   | 4.0.5 to latest |

{% hint style="warning" %}
**Deprecation**

* Gravitee context attribute `gravitee.attribute.kafka.topics` is deprecated and will be removed in future versions. Use `gravitee.attribute.kafka.producer.topics` or `gravitee.attribute.kafka.consumer.topics`.
* Use `gravitee.attribute.kafka.producer.topics` as the message attribute to publish messages to a specific topic.
{% endhint %}

## Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

To use this plugin, declare the following `kafka` identifier while configuring your API endpoints.

## Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

<table><thead><tr><th width="179">Attributes</th><th width="100">Default</th><th width="119">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>bootstrapServers</td><td>N/A</td><td>Yes</td><td>Define the comma-separated list of host/port pairs used to establish the initial connection to the Kafka cluster.</td></tr></tbody></table>

### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

#### **Security configuration**

<table><thead><tr><th>Attributes</th><th width="122">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>protocol</td><td>PLAINTEXT</td><td>No</td><td>Define your Kafka-specific authentication flow (PLAINTEXT, SASL_PLAINTEXT, SASL_SSL, and SSL).</td></tr><tr><td>sasl.saslMechanism</td><td>N/A</td><td>No</td><td>Define the SASL mechanism (GSSAPI, OAUTHBEARER, PLAIN, SCRAM_SHA-256, or SCRAM-SHA-512).</td></tr><tr><td>sasl.saslJaasConfig</td><td>N/A</td><td>No</td><td>Define the JAAS login context parameters for SASL connections in JAAS configuration file format.</td></tr><tr><td>ssl.trustStore.type</td><td>JKS</td><td>No</td><td>Define the TrustStore type (NONE, PEM, PKCS12, JKS).</td></tr><tr><td>ssl.trustStore.location</td><td>N/A</td><td>No</td><td>Define the TrustStore location.</td></tr><tr><td>ssl.trustStore.password</td><td>N/A</td><td>No</td><td>Define the TrustStore password.</td></tr><tr><td>ssl.trustStore.certificates</td><td>N/A</td><td>No</td><td>Define the TrustStore certificates.</td></tr><tr><td>ssl.keystore.type</td><td>JKS</td><td>No</td><td>Define the KeyStore type (NONE, PEM, PKCS12, JKS).</td></tr><tr><td>ssl.keystore.location</td><td>N/A</td><td>No</td><td>Define the KeyStore location.</td></tr><tr><td>ssl.keystore.password</td><td>N/A</td><td>No</td><td>Define the KeyStore password.</td></tr><tr><td>ssl.keystore.key</td><td>N/A</td><td>No</td><td>Define the KeyStore key.</td></tr><tr><td>ssl.keystore.keyPassword</td><td>N/A</td><td>No</td><td>Define the KeyStore key password.</td></tr><tr><td>ssl.keystore.certificateChain</td><td>N/A</td><td>No</td><td>Define the KeyStore certificate chain.</td></tr></tbody></table>

#### **Producer configuration**

<table><thead><tr><th>Attributes</th><th width="95">Default</th><th width="124">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Allow enabling or disabling the producer capability.</td></tr><tr><td>topics</td><td>N/A</td><td>Yes</td><td>List of topics.</td></tr><tr><td>compressionType</td><td>none</td><td>No</td><td>Define the compression type (none, gzip, snappy, lz4, zstd).</td></tr></tbody></table>

The following is an example of how to produce messages:

```json
{
  "name": "default",
  "type": "kafka",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {
    "bootstrapServers": "kafka:9092"
  },
  "sharedConfigurationOverride": {
    "producer": {
        "enabled": true,
        "topics" : ["demo"]
    },
    "security": {
      "protocol": "PLAINTEXT"
    }
  }
}
```

#### **Consumer configuration**

<table><thead><tr><th width="189">Attributes</th><th width="101">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Allow enabling or disabling the consumer capability.</td></tr><tr><td>topics</td><td>N/A</td><td>No</td><td>The topic(s) from which your Gravitee Gateway client will consume messages.</td></tr><tr><td>topics.pattern</td><td>N/A</td><td>No</td><td>A regex pattern to select topic(s) from which your Gravitee Gateway client will consume messages.</td></tr><tr><td>encodeMessageId</td><td>true</td><td>No</td><td>Allow encoding message IDs in base64.</td></tr><tr><td>autoOffsetReset</td><td>latest</td><td>No</td><td>Define the behavior if no initial offset (earliest, latest, none).</td></tr></tbody></table>

The following is an example of how to consume messages:

```json
{
  "name": "default",
  "type": "kafka",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {
    "bootstrapServers": "kafka:9092"
  },
  "sharedConfigurationOverride": {
    "consumer": {
      "enabled": true,
      "topics": [
        "demo"
      ],
      "autoOffsetReset": "earliest"
    }
  }
}
```

## Using SASL OAUTHBEARER <a href="#user-content-using-sasl-oauthbearer" id="user-content-using-sasl-oauthbearer"></a>

To facilitate support for SASL OAUTHBEARER, this plugin includes a [login callback handler for token retrieval](https://docs.confluent.io/platform/current/kafka/authentication\_sasl/authentication\_sasl\_oauth.html#login-callback-handler-for-token-retrieval). This handler is configured using the following JAAS configuration:

```bash
"org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required access_token=\"<ACCESS_TOKEN>\";"
```

The access token can be provided using EL to retrieve it from a Gravitee context attribute:

```json
{
  "name": "default",
  "type": "kafka",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {
    "bootstrapServers": "kafka:9092"
  },
  "sharedConfigurationOverride": {
    "security" : {
        "protocol" : "SASL_PLAINTEXT",
        "sasl" : {
          "saslMechanism" : "OAUTHBEARER",
          "saslJaasConfig" : "org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required access_token=\"{#context.attributes['gravitee.attribute.kafka.oauthbearer.token']}\";"
        }
      },
      "producer" : {
        "enabled" : true
        "topics" : [ "demo" ],
        "compressionType" : "none",
      },
      "consumer" : {
        "enabled" : true,
        "encodeMessageId" : true,
        "topics" : [ "demo" ],
        "autoOffsetReset" : "latest"
      }
  }
}
```

## Using SASL AWS\_MSK\_IAM <a href="#user-content-using-sasl-aws_msk_iam" id="user-content-using-sasl-aws_msk_iam"></a>

The Kafka plugin includes the Amazon MSK Library for AWS Identity and Access Management, which enables you to use AWS IAM to connect to their Amazon MSK cluster.

This mechanism is only available with the SASL\_SSL protocol. Once selected, you must provide a valid JAAS configuration. Different options are available depending on the AWS CLI credentials:

* To use the default credential profile, the client can use the following JAAS configuration:

```bash
software.amazon.msk.auth.iam.IAMLoginModule required;
```

* To specify a particular credential profile as part of the client configuration (rather than through the environment variable AWS\_PROFILE), the client can pass the name of the profile in the JAAS configuration:

```bash
software.amazon.msk.auth.iam.IAMLoginModule required  awsProfileName="<Credential Profile Name>";
```

* As another way to configure a client to assume an IAM role and use the role’s temporary credentials, the IAM role’s ARN and, optionally, accessKey and secretKey can be passed in the JAAS configuration:

```bash
software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="arn:aws:iam::123456789012:role/msk_client_role" awsRoleAccessKeyId="ACCESS_KEY"  awsRoleSecretAccessKey="SECRET";
```

More details can be found in the library’s [README](https://github.com/aws/aws-msk-iam-auth).

### Dynamic configuration <a href="#user-content-dynamic-configuration" id="user-content-dynamic-configuration"></a>

The Kafka endpoint includes the dynamic configuration feature, meaning that you can:

*   Override any configuration parameters using an attribute (via the Assign Attribute policy). Your attribute needs to start with `gravitee.attributes.endpoint.kafka`, followed by the property you want to override (e.g. `gravitee.attributes.endpoint.kafka.security.sasl.saslMechanism`). To override the topics property, add an Assign Attribute policy and set the attribute `gravitee.attributes.endpoint.kafka.consumer.topics` using a request header value or a query param, for example.\


    <figure><img src="../../.gitbook/assets/Assign attributes.png" alt=""><figcaption></figcaption></figure>
* Use EL in any "String" type property. The following example shows how to use EL to populate the consumer autoOffsetReset property:

```json
{
  "name": "default",
  "type": "kafka",
  "weight": 1,
  "inheritConfiguration": false,
  "configuration": {
    "bootstrapServers": "kafka:9092"
  },
  "sharedConfigurationOverride": {
    "consumer": {
      "enabled": true,
      "topics": [ "default_topic" ],
      "autoOffsetReset": "{#request.headers['autoOffsetReset'][0]}"
    }
  }
}
```
