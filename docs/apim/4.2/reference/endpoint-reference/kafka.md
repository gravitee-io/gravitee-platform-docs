---
description: This page contains the technical details of the Kafka endpoint plugin
---

# Kafka

This is an Enterprise feature

### Description <a href="#user-content-description" id="user-content-description"></a>

Endpoint to publish and subscribe events in Kafka using web-friendly protocols such as HTTP or Websocket. The reactive gateway mediates the protocol between the client and the backend.

#### Quality Of Service <a href="#user-content-quality-of-service" id="user-content-quality-of-service"></a>

| QoS           | Delivery    | Description                                                                                                                                                                        |
| ------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| None          | Unwarranted | Improve throughput by removing auto commit                                                                                                                                         |
| Balanced      | 0, 1 or n   | Used well-knowing consumer group and offsets mechanism to balance between performances and quality                                                                                 |
| At-Best       | 0, 1 or n   | Almost the same as _Balanced_ but doing our best to delivery message once only but depending on entrypoint could rely on extra features to ensure which was the last message sent. |
| At-Most-Once  | 0 or 1      | Depending on the entrypoint, this level could introduce performance degradation by forcing consumer to commit each message to ensure messages are sent 0 or 1 time.                |
| At-Least-Once | 1 or n      | Depending on the entrypoint, this level could introduce performance degradation by forcing consumer to acknowledge each message to ensure messages are sent 1 or multiple times.   |

### Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version  | APIM version    |
| --------------- | --------------- |
| 1.x to 2.1.4    | 3.20.x to 4.0.4 |
| 2.2.0 and upper | 4.0.5 to latest |

#### Deprecation <a href="#user-content-deprecation" id="user-content-deprecation"></a>

* ⚠️ Gravitee context attribute `gravitee.attribute.kafka.topics` is deprecated and will be removed in future versions. Use `gravitee.attribute.kafka.producer.topics` or `gravitee.attribute.kafka.consumer.topics`.
* Use `gravitee.attribute.kafka.producer.topics` as message attribute to publish messages to a specific topic.

### Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

In order to use this endpoint, you have to declare the following identifier `kafka` while configuring your API endpoints.

### Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

#### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

| Attributes       | Default | Mandatory | Description                                                                                                       |
| ---------------- | ------- | --------- | ----------------------------------------------------------------------------------------------------------------- |
| bootstrapServers | N/A     | Yes       | Define the comma-separated list of host/port pairs used to establish the initial connection to the Kafka cluster. |

#### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

**Security configuration**

| Attributes                    | Default   | Mandatory | Description                                                                                      |
| ----------------------------- | --------- | --------- | ------------------------------------------------------------------------------------------------ |
| protocol                      | PLAINTEXT | No        | Define your Kafka-specific authentication flow (PLAINTEXT, SASL\_PLAINTEXT, SASL\_SSL, and SSL). |
| sasl.saslMechanism            | N/A       | No        | Define the Sasl mechanism (GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512).        |
| sasl.saslJaasConfig           | N/A       | No        | Define the JAAS login context parameters for SASL connections in JAAS configuration file format. |
| ssl.trustStore.type           | JKS       | No        | Define the TrustStore type (NONE, PEM, PKCS12, JKS).                                             |
| ssl.trustStore.location       | N/A       | No        | Define the TrustStore location.                                                                  |
| ssl.trustStore.password       | N/A       | No        | Define the TrustStore password.                                                                  |
| ssl.trustStore.certificates   | N/A       | No        | Define the TrustStore certificates.                                                              |
| ssl.keystore.type             | JKS       | No        | Define the KeyStore type (NONE, PEM, PKCS12, JKS).                                               |
| ssl.keystore.location         | N/A       | No        | Define the KeyStore location.                                                                    |
| ssl.keystore.password         | N/A       | No        | Define the KeyStore password.                                                                    |
| ssl.keystore.key              | N/A       | No        | Define the KeyStore key.                                                                         |
| ssl.keystore.keyPassword      | N/A       | No        | Define the KeyStore key password.                                                                |
| ssl.keystore.certificateChain | N/A       | No        | Define the KeyStore certificate chain.                                                           |

**Producer configuration**

| Attributes      | Default | Mandatory | Description                                                  |
| --------------- | ------- | --------- | ------------------------------------------------------------ |
| enabled         | false   | No        | Allow enabling or disabling the producer capability.         |
| topics          | N/A     | Yes       | List of topics.                                              |
| compressionType | none    | No        | Define the compression type (none, gzip, snappy, lz4, zstd). |

**Consumer configuration**

| Attributes      | Default | Mandatory | Description                                                                                       |
| --------------- | ------- | --------- | ------------------------------------------------------------------------------------------------- |
| enabled         | false   | No        | Allow enabling or disabling the consumer capability.                                              |
| topics          | N/A     | No        | The topic(s) from which your Gravitee Gateway client will consume messages.                       |
| topics.pattern  | N/A     | No        | A regex pattern to select topic(s) from which your Gravitee Gateway client will consume messages. |
| encodeMessageId | true    | No        | Allow encoding message IDs in base64.                                                             |
| autoOffsetReset | latest  | No        | Define the behavior if no initial offset (earliest, latest, none).                                |

**Examples**

**Produce messages**

```
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

**Consume messages**

```
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

#### Using SASL OATHBEARER <a href="#user-content-using-sasl-oathbearer" id="user-content-using-sasl-oathbearer"></a>

To ease the support of SASL OAUTHBEARER, this plugin includes a [login callback handler for token retrieval](https://docs.confluent.io/platform/current/kafka/authentication\_sasl/authentication\_sasl\_oauth.html#login-callback-handler-for-token-retrieval). This handler is configured using the following JAAS configuration:

```
"org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required access_token=\"<ACCESS_TOKEN>\";"
```

The access token can be provided using an EL to retrieve it from a Gravitee context attribute:

```
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

#### Using SASL AWS\_MSK\_IAM <a href="#user-content-using-sasl-aws_msk_iam" id="user-content-using-sasl-aws_msk_iam"></a>

The plugin includes the Amazon MSK Library for AWS Identity and Access Management. This library enables the user to use AWS IAM to connect to their Amazon MSK cluster.

This mechanism is only available with SASL\_SSL protocol. Once selected, you need to provide a valid JAAS configuration.

Different options are available depending on the AWS CLI credentials:

* To use the default credential profile, the client can use the following JAAS configuration:

```
software.amazon.msk.auth.iam.IAMLoginModule required;
```

* If the client wants to specify a particular credential profile as part of the client configuration rather than through the environment variable AWS\_PROFILE, they can pass in the name of the profile in the JAAS configuration:

```
software.amazon.msk.auth.iam.IAMLoginModule required  awsProfileName="<Credential Profile Name>";
```

* The library supports another way to configure a client to assume an IAM role and use the role’s temporary credentials. The IAM role’s ARN and optionally, accessKey and secretKey to assume the role can be passed in the JAAS configuration:

```
software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="arn:aws:iam::123456789012:role/msk_client_role" awsRoleAccessKeyId="ACCESS_KEY"  awsRoleSecretAccessKey="SECRET";
```

More details can be found in the library’s [README](https://github.com/aws/aws-msk-iam-auth).

#### Dynamic configuration <a href="#user-content-dynamic-configuration" id="user-content-dynamic-configuration"></a>

This endpoint has the dynamic configuration feature meaning that you can:

* Override any configuration parameters using an attribute (via the assign-attribute policy). Your attribute needs to start with `gravitee.attributes.endpoint.kafka` followed by the property you want to override (e.g. `gravitee.attributes.endpoint.kafka.security.sasl.saslMechanism`). If we wanted to override the topics property, we could then add an assign attribute policy and set the attribute `gravitee.attributes.endpoint.kafka.consumer.topics` using a value from a header of the request or a query param for example.
* Use EL in any "String" type property. Here is an example showing how to use an EL to populate the consumer autoOffsetReset property.

```
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
