# Deploy APIs to a Gateway

The `state` attribute of the `ApiV4Definition` and `ApiDefinition` CRDs determines if an API should be in the `STARTED` or `STOPPED` state. By default, an API's `state` is set to `STARTED`.

To make this explicit, set the value of `state` to `TRUE` in the configuration for your API definition:

```yaml
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
  state: STARTED
  local: false
  proxy:
    virtual_hosts:
      - path: /k8s-basic
    groups:
      - endpoints:
          - name: Default
            target: https://api.gravitee.io/echo
```

To stop the API (or just create an API definition in "stop mode"), set the `state` property value to `STOPPED`:

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
  state: STOPPED
  local: false
  proxy:
    virtual_hosts:
      - path: /k8s-basic
    groups:
      - endpoints:
          - name: Default
            target: https://api.gravitee.io/echo
```

To start the API again, change the `state` property value back to `STARTED`.
