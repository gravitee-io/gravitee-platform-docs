# Dictionary CRD reference

## Kubernetes CRD configuration

This section describes the `Dictionary` resource specification and how to reference Kubernetes Secrets and ConfigMaps from a dynamic dictionary.

### Dictionary resource specification

Define a Dictionary resource using the `gravitee.io/v1alpha1` API version and the `Dictionary` kind. The `spec` includes these required fields:

* `contextRef`: Reference to a `ManagementContext` resource that determines which APIM instance the dictionary is synced to
* `name`: Display name of the dictionary
* `type`: Either `MANUAL` or `DYNAMIC`
* `deployed`: Boolean flag that controls the deployment state

The `description` field is optional. Provide `manual` when `type` is `MANUAL`, and `dynamic` when `type` is `DYNAMIC`.

For manual dictionaries, provide a `manual.properties` map with at least one key-value pair. For dynamic dictionaries, define:

* `dynamic.provider`: HTTP provider configuration with `type`, `url`, `method`, `specification` (JOLT), and optional `body`, `useSystemProxy`, and `headers`
* `dynamic.trigger`: Polling configuration with `rate` and `unit`

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Dictionary
metadata:
  name: my-dict
spec:
  contextRef:
    name: dev-ctx
    namespace: default
  name: "My Dictionary"
  type: MANUAL
  deployed: true
  manual:
    properties:
      key1: value1
```

### Secret and ConfigMap references

For dynamic dictionaries, reference Kubernetes Secrets or ConfigMaps in the provider configuration using template expressions. Each expression uses `[[ ]]` delimiters and takes a single `<resource-name>/<key>` argument. When the dictionary is referenced from an API, the dictionary key follows the pattern `<namespace>-<name>`.

{% hint style="warning" %}
Create the referenced Secret or ConfigMap before you create the dictionary. The operator reads the value during reconciliation, and reconciliation fails if the value isn't found.
{% endhint %}

```yaml
dynamic:
  provider:
    type: HTTP
    url: "[[ secret `my-secret/url` ]]"
    headers:
      - name: Authorization
        value: "[[ secret `my-secret/token` ]]"
```

ConfigMap references use the same syntax:

```yaml
dynamic:
  provider:
    type: HTTP
    url: "[[ configmap `my-config/url` ]]"
    headers:
      - name: Authorization
        value: "[[ configmap `my-config/token` ]]"
```

### Status and conditions

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
