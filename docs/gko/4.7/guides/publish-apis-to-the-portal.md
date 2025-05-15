# Publish APIs to the Developer Portal

Whether APIs managed by GKO are published to the Gravitee Developer Portal is controlled by an attribute called `lifecycle_state` in V2, `lifecycleState` in V4 CRDs.

These CRDs are also used to determine which [categories](publish-apis-to-the-portal.md#setting-a-category-for-an-api) an API should belong to. Categories help consumers navigate through large numbers of APIs on the Developer Portal.

## Publish an API to the Portal

By default, APIs are not published to the Developer Portal. To publish an API, set the `lifecycle_state` property value in V2 and `lifecycleState` in V4 property value to `PUBLISHED`:

V2 example:

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

V4 example:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4
spec:
  name: "api-v4"
  description: "API v4 managed by Gravitee Kubernetes Operator"
  version: "1.0"
  lifecycleState: PUBLISHED
  type: PROXY
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

To unpublish the API, change the `lifecycle_state` property value in V2 and the `lifecycleState` property value in V4 to `UNPUBLISHED`.

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
