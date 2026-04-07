# Publish APIs to the Developer Portal

Whether APIs managed by GKO are published to the Gravitee Developer Portal is controlled by an attribute called `lifecycle_state` that is common to both `ApiV4Definition` and `ApiDefinition` CRDs.

These CRDs are also used to determine which [categories](publish-apis-to-the-portal.md#setting-a-category-for-an-api) an API should belong to. Categories help consumers navigate through large numbers of APIs on the Developer Portal.

## Publish an API to the Portal

By default, APIs aren't published to the Developer Portal. To publish an API, set the `lifecycle_state` property value to `PUBLISHED`:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
  namespace: gravitee
spec:
  name: gko-example
  contextRef: 
    name: "management-context-1"
  version: 1.0.0
  description: Basic api managed by Gravitee Kubernetes Operator
  lifecycle_state: PUBLISHED
  local: false
  proxy:
    virtual_hosts:
      - path: /k8s-basic
    groups:
      - endpoints:
          - name: Default
            target: https://api.gravitee.io/echo
```

To unpublish the API, change the `lifecycle_state` property value to `UNPUBLISHED`.

## Deprecate or archive an API

For `ApiV4Definition` resources, the `lifecycleState` field also accepts `DEPRECATED` and `ARCHIVED`:

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
  lifecycleState: "DEPRECATED"
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

* **DEPRECATED**: The API is no longer visible to consumers. New plans can't be created on it. Existing subscriptions and Gateway traffic aren't affected.
* **ARCHIVED**: The API is fully retired. It can't be started or stopped through the Management API. This is a terminal state.

{% hint style="info" %}
The operator supports transitioning from DEPRECATED to ARCHIVED. To archive a deprecated API, update the `lifecycleState` field to `ARCHIVED`. The Console and Management API don't allow this transition directly.
{% endhint %}

{% hint style="info" %}
For the full list of allowed lifecycle state transitions and validation rules, see [API lifecycle states](../../../apim/4.11/create-and-configure-apis/configure-v4-apis/api-lifecycle-states.md) in the APIM documentation.
{% endhint %}

## Setting a category for an API

APIs can be grouped into categories to help API consumers navigate through APIs they discover on the Developer Portal. Both `ApiV4Definition` and `ApiDefinition` can reference categories in APIM by name. If a referenced category does not exist in APIM, it will be ignored.

Below is an example `ApiV4Definition` that references two categories, called `banking` and `credit`:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4
  namespace: gravitee
spec:
  name: api-v4
  contextRef: 
    name: "management-context-1"
  definitionContext:
    origin: KUBERNETES
    syncFrom: MANAGEMENT
  description: API v4 managed by Gravitee Kubernetes Operator
  version: 1.0
  type: PROXY
  categories: 
    - banking
    - credit
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
      name: Free plan
      description: This plan does not require any authentication
      security:
        type: KEY_LESS
```
