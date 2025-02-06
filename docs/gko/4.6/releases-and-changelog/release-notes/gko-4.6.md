---
description: Gravitee Kubernetes Operator 4.6 Release Notes.
---

# GKO 4.6

## Kafka Proxy API support with GKO

Gravitee API Management 4.6 includes introduces the Gravitee Kafka Gateway, which allows you to natively expose the Kafka protocol to Kafka consumers and producers while proxying an upstream Kafka cluster.

GKO 4.6 lets you use the Gravitee Kubernetes Operator to define native Kafka APIs, so that you can configure them by creating familiar APIOps automation pipelines.

Practically speaking, native Kafka APIs are just a new type of v4 API, alongside proxy and message APIs. Below is a simple example of a Native Kafka API defined using GKO's `ApiV4Definition` CRD:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-kafka
spec:
  contextRef:
    name: "context"
  name: "api-v4-kafka"
  description: "V4 Native API managed by Gravitee Kubernetes Operator"
  version: "1.0"
  type: NATIVE
  labels: ["kafka"]
  listeners:
    - type: KAFKA
      host: "gko"
      port: 9092
      entrypoints:
        - type: native-kafka
  endpointGroups:
    - name: Default Native endpoint group
      type: native-kafka
      sharedConfiguration:
        security:
          protocol: PLAINTEXT
      endpoints:
        - name: Default Native proxy
          type: native-kafka
          inheritConfiguration: true
          "weight": 1
          configuration:
            bootstrapServers: "your.kafka.cluster:9092"
          secondary: false
  plans:
    KeyLess:
      name: "Free plan"
      description: "This plan does not require any authentication"
      security:
        type: "KEY_LESS"
```

Just like other API definitions managed by the Gravitee Kubernetes Operator, native Kafka APIs can carry policies, lifecycle information, plans to control access, documentation pages, RBAC, and more!

## Manage JWT, OAuth, and mTLS subscriptions with GKO

With 4.6, the operator includes a new `Subscription` CRD. This allows you to create subscriptions to API plans in APIM. A subscription ties an application to a specific API plan, thereby giving that application permission to consume the API.

The `Subscription` CRD significantly expands the scope of what you can do with GKO by providing GitOps support across an even larger part of the API lifecycle. This is particularly attractive because it gives automated deployments the ability to consume applications as part of the automation.

GKO supports three plan types: JWT, OAuth, and mTLS. API key is not supported at this time, but is likely to come in a future release.

Below is an example instance of the new subscription custom resource definition:

```yaml
kind: Subscription
metadata:
  name: v4-api-jwt-subscription
spec:
  api:
    name: api-v4-jwt
  plan: jwt-plan
  application:
    name: oauth-app
```

This resource references:

* An **API** called `api-v4-jwt`, based on its Kubernetes metadata name
* A **plan** called `jwt-plan`, based on the key that uniquely identifies the plan in the `api-v4-jwt` resource
* An **application** called `oauth-app`, based on its Kubernetes metadata name

Once this resource is created, the subscription is considered active. When deleted, the subscription ends. In the future, we'll likely provide an `enabled` boolean flag that lets you easily toggle a subscription on and off without need to delete the resource completely.

For more details on how this works, check out the accompanying release blog post and video that run through a complete example and use Gravitee Access Management as the identity provider for issuing JWT tokens.

The GKO GitHub repository also includes great [end-to-end guides](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/examples/usecase) for setting up JWT and mTLS subscriptions without an external identity provider.

## Other improvements

#### Continued improvements to the validation Webhook

Since 4.5, GKO includes a validation Webhook that performs syntactic and semantic checks on your Gravitee resources before creating them. This is to improve the developer experience by failing fast and providing useful feedback.

With 4.6, validation rules have been added for the new `Subscription` CRD and the new Native API type. More validation rules have been added to existing CRDs.

**Add Failover parameters for V4 APIs**

Failover configuration settings are now supported for PROXY and MESSAGE API types, with NATIVE support planned for a future release.

#### Remove the `DisplayName` field from v2 and v4 APIs

The `DisplayName` field is no longer part of API exports, ensuring cleaner data handling.

#### **New GKO logging configuration options**

In the GKO Helm Chart, an additional block of parameters has been introduced to let you better configure logging:

```yaml
manager:
  logs:
    ## @param manager.logs.format Specifies log output format. Can be either json or console.
    format: json
    ## @param manager.logs.level Specifies log level. Can be either debug, info, warn, or error. Wrong values are converted to `info`.
    level: info
    ## @param manager.logs.levelCase Specifies the case of the level value. Can be either lower or upper. Wrong values are converted to `upper`.
    levelCase: upper
    timestamp:
      ## @param manager.logs.timestamp.field Specifies the name of the field to use for the timestamp.
      field: timestamp
      ## @param manager.logs.timestamp.format Specifies the format to use for the timestamp. Can be either iso-8601, epoch-second, epoch-millis or epoch-nano.
      ## Wrong values are converted to `iso-8601`.
      format: iso-8601
```

Note that the parameter `manager.logs.json` has been deprecated in favor of the new parameter`manager.logs.format`**.**
