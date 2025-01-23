---
description: Gravitee Kubernetes Operator 4.6 Release Notes.
---

# GKO 4.6

## Kafka Proxy API support with GKO

Gravitee API management 4.6 includes the introduction of the Gravitee Kafka Gateway, allowing you to natively expose the Kafka protocol to Kafka consumers and producers, while proxying an upstream Kafka cluster.

With GKO 4.6, we've added the ability to define Native Kafka APIs using the Gravitee Kubernetes Operator, so that you can create familiar APIOps automation pipelines to configure you native Kafka APIs.&#x20;

Practically speaking, Native Kafka APIs are just a new type of v4 API, alongside proxy and message APIs. Below is a simple example of a Native Kafka API defined using GKO's ApiV4Definition CRD:

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

Just like other API definitions managed by the Gravitee Kubernetes Operator, native Kafka APIs can carry policies, lifecycle information, plans to control access, documentation pages, RBAC, and more!&#x20;

## Manage JWT, OAuth, and mTLS subscriptions with GKO

With 4.6, the operator now includes a new Subscription CRD. This allows you to create subscriptions to API plans in APIM. A subscription ties an Application to a specific plan from an API, thereby giving that application permission to consume the API.&#x20;

This significantly expands the scope of what you can do with GKO, thereby providing GitOps support across an even larger part of the API lifecycle. This will be particularly attractive for covering automated deployments that also need to enable consumption by applications as part of the automation.

GKO will support three plan types: JWT, OAuth, and mTLS. API key is not supported at this time, but is likely to come in a future release.&#x20;

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

This resources references:

* an **API** called `api-v4-jwt`, based on its Kubernetes metadata name
* a **plan** called `jwt-plan`, based on the key that uniquely identifies the plan in the `api-v4-jwt` resource
* an **application** called `oauth-app`, based on its Kubernetes metadata name

One this resource is created, the subscription is considered active. When deleted, the subscription ends. In the future, we'll likely provide an **enabled** boolean flag that lets you easily toggle a subscription on and off without need to delete the resource completely.&#x20;

For more details on how this works, check out the accompanying release blog post and video that run through a complete example that uses Gravitee Access Management as the identity provider for issuing JWT tokens.

The GKO GitHub repository also includes great [end-to-end guides](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/examples/usecase) for setting up JWT and mTLS subscriptions without needing an external identity provider.&#x20;

## Other improvements

#### Continued improvements to the validation webhook

Since 4.5, GKO includes a validation webhook that will perform syntactic and semantic checks on your Gravitee resources before creating them. The purpose of this is to fail fast and provide useful feedback, in order to improve the developer experience.

With 4.6, validation rules have been added for the new Subscription CRD, for the new Native API type, and more have been added to existing CRDs.

**Add Failover parameters for V4 APIs**

Failover configuration settings are now supported for PROXY and MESSAGE API types, with NATIVE support planned for a future release.

#### Remove the field DisplayName from v2 and v4 APIs

The `DisplayName` field is no longer part of API exports, ensuring cleaner data handling.

We looking forward to hearing your thoughts on this new release!&#x20;



**New GKO logging configuration options**

In the GKO Helm chart, an additional block of parameters has been introduced to allow you to better configure logging:

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

Note that parameter **manager.logs.json** has been deprecated in favour of new **manager.logs.format.**
