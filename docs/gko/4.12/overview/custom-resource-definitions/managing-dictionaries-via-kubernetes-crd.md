# Dictionary CRD reference

This page describes the `Dictionary` custom resource specification, with examples for manual and dynamic dictionaries, how to reference a dictionary from an API, and how to reference Kubernetes Secrets and ConfigMaps.

## Common specification

Define a Dictionary resource using the `gravitee.io/v1alpha1` API version and the `Dictionary` kind. Every dictionary shares these `spec` fields, regardless of type:

* `contextRef`: Reference to the `ManagementContext` resource that determines which APIM environment the dictionary syncs to
* `name`: Display name of the dictionary
* `type`: Either `MANUAL` or `DYNAMIC`
* `deployed`: Boolean that controls the deployment state
* `description`: Optional description of the dictionary

Provide `manual` when `type` is `MANUAL`, and `dynamic` when `type` is `DYNAMIC`.

## Manual dictionary

A manual dictionary stores static key-value pairs in a `manual.properties` map, which holds at least one entry:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Dictionary
metadata:
  name: e2e-dict-manual
spec:
  contextRef:
    name: dev-ctx
    namespace: default
  name: e2e-dict-manual
  type: MANUAL
  deployed: true
  manual:
    properties:
      env: test
```

## Dynamic dictionary

A dynamic dictionary fetches its properties from an external HTTP provider on a schedule, then maps the response into key-value pairs using a JOLT specification. For a dynamic dictionary, define:

* `dynamic.provider`: HTTP provider configuration with `type` (`HTTP`), `url`, `method`, and `specification` (JOLT), plus optional `body`, `useSystemProxy`, and `headers`
* `dynamic.trigger`: Polling schedule with `rate` and `unit` (one of `MICROSECONDS`, `MILLISECONDS`, `SECONDS`, `MINUTES`, `HOURS`, or `DAYS`)

The following example polls the Gravitee echo API every five seconds and exposes its response headers as properties:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Dictionary
metadata:
  name: e2e-dict-dynamic
spec:
  contextRef:
    name: dev-ctx
    namespace: default
  name: e2e-dict-dynamic
  description: Expose echo API headers as properties
  type: DYNAMIC
  deployed: true
  dynamic:
    provider:
      type: HTTP
      url: https://api.gravitee.io/echo
      method: GET
      headers:
        - name: X-Test-Specific
          value: ABCDEF
      specification: |
        [
          {
            "operation": "shift",
            "spec": {
              "headers": {
                "*": {
                  "$": "[#2].key",
                  "@": "[#2].value"
                }
              }
            }
          }
        ]
    trigger:
      rate: 5
      unit: SECONDS
```

## Reference a dictionary from an API

The Gravitee Kubernetes Operator builds the dictionary key by joining the namespace and name of the `Dictionary` resource with a hyphen: `<namespace>-<name>`. A dictionary created as `e2e-dict-manual` in the `default` namespace has the key `default-e2e-dict-manual`. The same rule applies to manual and dynamic dictionaries.

Reference the key in Gravitee Expression Language to read a property: `{#dictionaries['<namespace>-<name>']['<property>']}`.

The following `ApiV4Definition` adds a request header whose value comes from the `env` property of the `default-e2e-dict-manual` dictionary. Listeners, endpoint groups, and plans are omitted for brevity:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: e2e-api-with-dict
spec:
  contextRef:
    name: dev-ctx
    namespace: default
  name: e2e-api-with-dict
  version: "1.0"
  type: PROXY
  state: STARTED
  # listeners, endpointGroups, and plans omitted for brevity
  flows:
    - name: Add dictionary header
      enabled: true
      selectors:
        - type: HTTP
          path: /
          pathOperator: STARTS_WITH
      request:
        - name: Transform Headers
          enabled: true
          policy: transform-headers
          configuration:
            addHeaders:
              - name: X-Dict-Env
                value: "{#dictionaries['default-e2e-dict-manual']['env']}"
```

## Reference Secrets and ConfigMaps

Reference Kubernetes Secrets or ConfigMaps from a dynamic dictionary to keep credentials out of the `Dictionary` resource. This matters most for dynamic dictionaries: the provider `url`, `headers`, and any tokens are pushed to APIM during reconciliation and are visible to authorized users in the API Management Console, so storing them inline exposes them in plain text.

Each template expression uses `[[ ]]` delimiters and takes a single `<resource-name>/<key>` argument. Use the `secret` keyword to read from a Secret and the `configmap` keyword to read from a ConfigMap. The operator resolves the value from the referenced resource in the dictionary's namespace.

{% hint style="warning" %}
Create the referenced Secret or ConfigMap before you create the dictionary. The operator reads the value during reconciliation, and reconciliation fails if the value isn't found.
{% endhint %}

Create the Secret that holds the provider URL and header value:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: e2e-dict-dyn-tpl-secret
type: Opaque
stringData:
  provider-url: https://api.gravitee.io/echo
  header-value: ABCDEF
```

Reference the Secret keys from the dynamic dictionary, using the same JOLT `specification` shown in the dynamic dictionary example:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Dictionary
metadata:
  name: e2e-dict-dyn-tpl
spec:
  contextRef:
    name: dev-ctx
    namespace: default
  name: e2e-dict-dyn-tpl
  description: Dynamic dictionary with templated secret values
  type: DYNAMIC
  deployed: true
  dynamic:
    provider:
      type: HTTP
      url: "[[ secret `e2e-dict-dyn-tpl-secret/provider-url` ]]"
      method: GET
      headers:
        - name: X-Test-Specific
          value: "[[ secret `e2e-dict-dyn-tpl-secret/header-value` ]]"
      specification: |
        [ ... ]
    trigger:
      rate: 5
      unit: SECONDS
```

To read the same values from a ConfigMap, use the `configmap` keyword in place of `secret`:

```yaml
url: "[[ configmap `my-config/provider-url` ]]"
```

## Status and conditions

The Dictionary status includes:

* `id`: Assigned dictionary UUID
* `organizationId`: Organization identifier
* `environmentId`: Environment identifier
* `conditions`: Array of condition objects
* `errors`: Object containing `severe` and `warning` arrays

The `conditions` array tracks the resource state:

| Condition | Description |
|:----------|:------------|
| `Accepted` | The dictionary was created in APIM |
| `ResolvedRefs` | The `contextRef` points to an existing `ManagementContext` |

The operator sets the `gravitee.io/last-spec-hash` annotation, which triggers reconciliation when the spec changes.

The `errors` object is populated during admission validation and contains validation failures categorized by severity.
