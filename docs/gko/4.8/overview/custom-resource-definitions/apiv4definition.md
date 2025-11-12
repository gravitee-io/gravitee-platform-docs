# ApiV4Definition

The `ApiV4Definition` custom resource represents the configuration for a v4 API on the Gravitee Gateway. v4 APIs are created from the latest version of the Gravitee API definition, which supports both synchronous and asynchronous APIs. GKO also supports the previous [v2 API definition](apidefinition.md) with a dedicated CRD.

## Creating an `ApiV4Definition`

You can create the following types of `ApiV4Definition` :

* Proxy
* Message
* Kafka Native

### Proxy

The Proxy `ApiV4Definition` accepts HTTP and TCP services such as REST APIs, SOAP, and WebSocket. Requests pass through the Gravitee Gateway to a REST endpoint, which applies your policies and plans to a request and then returns the response.

The following example shows a Proxy `ApiV4Definition` custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4
  namespace: gravitee
spec:
  name: "api-v4"
  description: "API v4 managed by Gravitee Kubernetes Operator"
  version: "1.0"
  type: PROXY
  contextRef: 
    name: "management-context-1"
  definitionContext:
    origin: KUBERNETES
    syncFrom: MANAGEMENT
  listeners:
    - type: HTTP
      paths:
        - path: "/echo-v4"
      entrypoints:
        - type: http-proxy
          qos: AUTO
  endpointGroups:
    - name: Default HTTP proxy group
      type: http-proxy
      endpoints:
        - name: Default HTTP proxy
          type: http-proxy
          inheritConfiguration: false
          configuration:
            target: https://api.gravitee.io/echo
          secondary: false
  flowExecution:
    mode: DEFAULT
    matchRequired: false
  plans:
    KeyLess:
      name: "Free plan"
      description: "This plan does not require any authentication"
      security:
        type: "KEY_LESS"
```

### Message

The Message `ApiV4Definition` accepts HTTP and TCP requests. When the request passes through the Gateway, the Gateway sends the request to a Message endpoint, such as Kafka or Solace, and then returns the response.

The following example shows a Proxy `ApiV4Definition` custom resource definition:

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "message-api"
spec:
  name: "message-api"
  version: "1.0"
  type: "MESSAGE"
  listeners:
  - type: "HTTP"
    paths:
    - path: "/message/"
      overrideAccess: false
    entrypoints:
    - type: "websocket"
      qos: "AUTO"
      configuration:
        subscriber:
          enabled: true
        publisher:
          enabled: true
  endpointGroups:
  - name: "Default Kafka group"
    type: "kafka"
    loadBalancer:
      type: "ROUND_ROBIN"
    sharedConfiguration:
      security:
        protocol: "PLAINTEXT"
      consumer:
        encodeMessageId: true
        checkTopicExistence: false
        removeConfluentHeader: false
        topics:
        - "test"
        enabled: true
        autoOffsetReset: "latest"
    endpoints:
    - name: "Default Kafka"
      type: "kafka"
      weight: 1
      inheritConfiguration: true
      configuration:
        bootstrapServers: "localhost:8082"
      services: {}
      secondary: false
    services: {}
  analytics:
    enabled: true
    sampling:
      type: "COUNT"
      value: "1"
  plans:
    Default Keyless (UNSECURED):
      name: "Default Keyless (UNSECURED)"
      description: "Default unsecured plan"
      security:
        type: "KEY_LESS"
      order: 1
      status: "PUBLISHED"
      type: "API"
      validation: "MANUAL"
      mode: "STANDARD"
  flowExecution:
    mode: "default"
    matchRequired: false
  visibility: "PRIVATE"
  lifecycleState: "UNPUBLISHED"
  definitionVersion: "V4"

```

### Kafka Native

With the Kafka Native `APIV4Definition`, the Gravitee Gateway acts like a Kafka server, which you can connect to using a any Kafka client. After you send a Kafka request, the Gateway applies your policies and plans, connects to your upstream Kafka server, and then returns the response in the protocol that you requested.

The following example shows a Kafka Native `ApiV4Definition` custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-native-with-context
spec:
  contextRef:
    name: "dev-ctx"
  name: "api-v4-native-with-context"
  description: "V4 Native API managed by Gravitee Kubernetes Operator 2"
  version: "1.0"
  type: NATIVE
  state: STARTED
  listeners:
    - type: KAFKA
      host: "kafka.local"
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
            bootstrapServers: "kafka.local:9001"
          secondary: false
  plans:
    KeyLess:
      name: "Free plan"
      description: "This plan does not require any authentication"
      security:
        type: "KEY_LESS"
  flows:
    - name: "default"
      enabled: true
      interact:
        - name: "Debug Log policy"
          enabled: true
          policy: "debug-log"
```

## The `ApiV4Definition` lifecycle

The following workflow is applied when a new `ApiV4Definition` resource is added to the cluster:

1. The GKO listens for `ApiV4Definition` resources.
2. The GKO performs required changes, such as automatically computing IDs or CrossIDs (for APIs or plans).
3. The GKO converts the definition to JSON format.
4. The GKO compares the definition to the existing definition. If something has changed, the GKO pushes the definition to the Management API (if a `ManagementContext` resource is provided).
5. The GKO deploys the API to the API Gateway.

The `ApiV4Definition` resource has a `Processing Status` field used to view the status of the resource in the cluster. The following `Processing Status` field values are possible:

<table><thead><tr><th width="143.5">Status</th><th>Description</th></tr></thead><tbody><tr><td>[None]</td><td>The API definition has been created but not yet processed.</td></tr><tr><td>Completed</td><td>The API definition has been created or updated successfully.</td></tr><tr><td>Reconciling</td><td>The operator has encountered a recoverable error. A retry will be performed every 5 seconds until the cluster retry limit is reached.</td></tr><tr><td>Failed</td><td>The operator has encountered an unrecoverable error. These are errors that require manual action to correct. No retry will be performed.</td></tr></tbody></table>

Events are added to the resource as part of each action performed by the operator.

{% hint style="info" %}
**For more information**

* The `ApiV4Definition` and `ApiDefinition` CRDs are available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/helm/gko/crds).
* The `ApiV4Definition` and `ApiDefinition` CRD API references are documented [here](docs/gko/4.8/reference/api-reference.md).
{% endhint %}
