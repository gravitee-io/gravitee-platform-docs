---
description: Deployment guide for Deploy APIs.
---

# Deploy APIs to a gateway

The **state** attribute of the `ApiV4Definition` and `ApiDefinition` CRDs determines whether or not an API should be in the `STARTED` or `STOPPED` state. By default, APIs **state** is set to `STARTED`.

You can make this state explicit in your API definition by setting the value of **state** to `TRUE` in your API configuration:

```yaml
kind: ApiDefinition
metadata:
  name: basic-api-example
  namespace: gravitee
spec:
  name: gko-example
  contextRef:
    name: dev-ctx
    namespace: gravitee
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

To stop it (or just create an API definition in "stop mode"), set the `state` property value to `STOPPED`:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
  namespace: gravitee
spec:
  name: gko-example
  contextRef:
    name: dev-ctx
    namespace: apim-example
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
