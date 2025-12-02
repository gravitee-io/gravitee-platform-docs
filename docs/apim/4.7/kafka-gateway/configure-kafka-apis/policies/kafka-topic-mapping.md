---
description: An overview about kafka topic mapping.
---

# Kafka Topic Mapping

## Overview <a href="#user-content-description" id="user-content-description"></a>

The Kafka Topic Mapping policy lets you map one topic to another so that the Kafka client can use a topic name that is different from the topic name used in the Kafka broker.

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

<table><thead><tr><th width="183">Property</th><th>Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td><code>mappings</code></td><td>No</td><td>A list of mappings between the client topic and the broker topic.</td><td>Array</td><td></td></tr><tr><td><code>mappings.client</code></td><td>No</td><td>The name provided on the client side that will be mapped in something else.</td><td>String</td><td></td></tr><tr><td><code>mappings.broker</code></td><td>No</td><td>The name that will be sent on the broker side. Supports EL expressions.</td><td>String</td><td></td></tr></tbody></table>

## Examples <a href="#user-content-supported-kafka-apikeys" id="user-content-supported-kafka-apikeys"></a>

The following examples demonstrate how to expose a broker-side (internal) topic name with a consumer-friendly client-side (external) topic name.

### Simple mapping

The simplest use case is a straightforward mapping between broker-side and client-side topic names.

#### Example 1: I want to map an internal topic name to something else (externally)

If you have a broker-side topic called `internal.orders.processed` and you want to expose that as a consumer-friendly name, then configure the Kafka Topic Mapping policy as follows:

* Client-side name: `processed-orders`
* Broker-side name: `internal.orders.processed`

Kafka clients will now be able to specify the mapped topic name (`processed-orders`) in their connection configuration. For example: `kafka-console-consumer.sh --bootstrap-server foo.kafka.local:9092 --consumer.config config/client.properties --topic processed-orders`

{% tabs %}
{% tab title="Using the APIM Console" %}
This shows how to implement the example above using the APIM Console:

<figure><img src="../../../.gitbook/assets/00 1.png" alt=""><figcaption><p>Kafka Topic Mapping policy configuration UI</p></figcaption></figure>
{% endtab %}

{% tab title="v4 API definition" %}
This code snippet of a v4 API definition shows how to implement the example above:

```json
{
  "api": {
    ...
  },
  "plans: [    
    {
      "flows": [
        {
          "interact": [
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "broker": "internal.orders.processed",
                    "client": "processed-orders"
                  }
                ]
              }
              ...
            }
          ]
        }
      ]
    }
  }
}
```
{% endtab %}
{% endtabs %}

### Dynamic mapping

The following examples are more complex and use Gravitee Expression Language.

#### Example 2: I want to simplify internal-only topic names as an external-friendly topic name (with support from an OAuth2 provider)

In this scenario, each customer of a company has their own dedicated topic in the Kafka cluster. Each customer also has their own unique `organizationId`, so the topic naming schema is `internal.organization-updates.{organizationId}`.

The customer may not know their own `organizationId`, but it has been included in their access token in a field named `rf_org`. After the user has authenticated with the identity provider, Gravitee can extract this payload data from their access token, as shown below:

{% code title="Example access token payload:" %}
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "rf_org": "12345"
}
```
{% endcode %}

Using the above payload data, the broker-side topic should be: `internal.organization-updates.12345`.

This company wants to simplify customer requirements so customers can specify a generic client-side topic, such as `organization-updates`, and Gravitee will dynamically map that to the relevant broker-side topic in Kafka using the details obtained from each OAuth2 access token payload.

You can use the Kafka Topic Mapping policy to create a new topic mapping with a client-side name of `organization-updates` and a broker-side name of `integrator.organization-updates.{#jsonPath(#context.attributes['oauth.payload'], '$.rf_org')}`. This broker-side name includes the use of Gravitee Expression Language to dynamically inject the `rf_org` value from the OAuth2 payload.

{% tabs %}
{% tab title="Using the APIM Console" %}
This shows how to implement the example above using the APIM Console:

<figure><img src="../../../.gitbook/assets/image (227) (1).png" alt=""><figcaption><p>Kafka Topic Mapping policy configuration UI</p></figcaption></figure>
{% endtab %}

{% tab title="v4 API definition" %}
This shows how to implement the example above in a v4 API definition:

```json
{
  "api": {
    ...
  },
  "plans: [
    {
      "flows": [
        {
          ...
          "interact": [
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "client": "organization-updates",
                    "broker": "integrator.organization-updates.{#jsonPath(#context.attributes['oauth.payload'], '$.rf_org')}"
                   }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```
{% endtab %}
{% endtabs %}

#### Example 3: I want dynamic topic mapping based on user identity and permissions (with support from an OAuth2 provider)

Suppose an enterprise system dynamically maps topics based on user roles. Admins need to access the full `internal.system.logs` topic, but other users should only see a filtered version that is mapped to `internal.user.logs`.

Topics can be be mapped based on user roles retrieved from an OAuth2 provider, with the correct permissions applied based on user identity. First, the user's role is extracted from the OAuth2 access token supplied by the identity server. OAuth2 roles are automatically added to `context.attributes` by Gravitee. Next, topics are dynamically mapped based on user role.

With this configuration, admin users see logs mapped to `internal.system.logs` and other users see logs mapped to `internal.user.logs`.

{% tabs %}
{% tab title="Using the APIM Console" %}
This shows how to implement the example above using the APIM Console:

<figure><img src="../../../.gitbook/assets/00 2.png" alt=""><figcaption><p>Kafka Topic Mapping policy configuration UI</p></figcaption></figure>
{% endtab %}

{% tab title="v4 API definition" %}
This shows how to implement the example above in a v4 API definition:

```json
{
  "api": {
    ...
  },
  "plans: [
    {
      "flows": [
        {
          "interact": [
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "client": "logs",
                    "broker": "{#context.attributes['user.role'] == 'admin' ? 'internal.system.logs' : 'internal.user.logs'}"
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  }
} 
```
{% endtab %}
{% endtabs %}

### In combination with the Kafka ACL policy

When using topic mapping together with the [Kafka ACL policy](kafka-acl.md), order is important. If topic mapping occurs before ACL, the ACL policy must use the broker-side name of the topic mapping. Conversely, if ACL occurs before topic mapping, the ACL policy must use the mapped name, which is the client-side name of the topic mapping.

The following examples show how you can place the topic mapping and ACL policies in relation to one another to achieve specific results.

#### Example 4: I want to execute the ACL policy after topic mapping

An API Gateway enforces Kafka ACL rules to control access to topics. However, if ACL checks happen before topic mapping, requests may be rejected because the client-side topic name isn't recognized.

To ensure that ACL rules are applied correctly, the ACL policy should be executed after the Topic Mapping policy so that it evaluates the actual broker-side topic.

{% tabs %}
{% tab title="Using the APIM Console" %}
This shows how to implement the example above using the APIM Console.

Kafka Topic Mapping configuration:

<figure><img src="../../../.gitbook/assets/00 3.png" alt=""><figcaption><p>Kafka Topic Mapping policy configuration UI</p></figcaption></figure>

Kafka ACL configuration:

<figure><img src="../../../.gitbook/assets/00 5.png" alt=""><figcaption><p>Kafka ACL policy configuration UI</p></figcaption></figure>

Here is how the policies should be ordered in the policy chain:

<figure><img src="../../../.gitbook/assets/00 ta.png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="v4 API definition" %}
This shows how to implement the example above in a v4 API definition:

```json
{
  "api": {
    ...
  },
  "plans: [    
    {
      "flows": [
        {
          "interact": [
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "client": "orders",
                    "broker": "internal.orders.processing.12345"
                  }
                ]
              }
            },
            {
              "name": "Kafka ACL Policy",
              "enabled": true,
              "policy": "kafka-acl",
              "configuration": {
                "authorizedTopics": [
                  "internal.orders.processing.12345"
                ],
                "authorizationType": "READ"
              }
            }
          ]
        }
      ]
    }
  }
}
```
{% endtab %}
{% endtabs %}

#### Example 5: I want to enforce ACL before topic mapping with wildcard permissions

Suppose a security-first organization requires Kafka ACL rules to be enforced before topic mapping, but some applications need wildcard-based access control to produce or consume messages from any topic that matches a pattern.

In this scenario, the ACL policy must be able to handle wildcard rules for groups of topics. In addition, topics must be mapped after authorization so that consumers don’t need to know internal topic names.

With this configuration:

* ACL ensures users can access only `internal.orders.*` topics.
* Topic mapping consolidates all internal topics into a single `orders` topic for external consumers.

{% tabs %}
{% tab title="Using the APIM Console" %}
This shows how to implement the example above using the APIM Console.

ACL configuration:

<figure><img src="../../../.gitbook/assets/00 6.png" alt=""><figcaption></figcaption></figure>

Topic mapping configuration:

<figure><img src="../../../.gitbook/assets/00 4.png" alt=""><figcaption></figcaption></figure>

Here is how the policies should be ordered in the policy chain:

<figure><img src="../../../.gitbook/assets/00 at.png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="v4 API definition" %}
This shows how to implement the example above in a v4 API definition:

```json
{
  "api": {
    ...
  },
  "plans: [    
    {
      "flows": [
        {
          "interact": [
            {
              "name": "Kafka ACL Policy",
              "enabled": true,
              "policy": "kafka-acl",
              "configuration": {
                "authorizedTopics": [
                  "internal.orders.*"
                ],
                "authorizationType": "READ_WRITE"
              }
            },
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "client": "orders",
                    "broker": "internal.orders.global"
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  }
}
```
{% endtab %}
{% endtabs %}
