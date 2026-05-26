# Managing Dictionaries via Kubernetes CRD

## Kubernetes CRD Configuration

### Dictionary Resource Specification

Define a Dictionary resource using the `gravitee.io/v1alpha1` API version and `Dictionary` kind. The `spec` must include:

* `contextRef`: Points to a `ManagementContext` resource
* `name`: Dictionary name (minimum 3 characters)
* `type`: Either `MANUAL` or `DYNAMIC`
* `deployed`: Boolean flag controlling deployment state

For manual dictionaries, provide a `manual.properties` map with at least one key-value pair. For dynamic dictionaries, define:

* `dynamic.provider`: HTTP provider configuration with `type`, `url`, `method`, `specification` (JOLT), optional `body`, `useSystemProxy`, and `headers`
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

### Secret and ConfigMap References

For dynamic dictionaries, reference Secrets or ConfigMaps in the provider configuration using Go template syntax. The dictionary key in API references follows the pattern `<namespace>-<name>`.

{% hint style="warning" %}
Secrets must exist before dictionary creation. The operator does not retry on secret creation.
{% endhint %}

```yaml
dynamic:
  provider:
    type: HTTP
    url: "{{ secret `my-secret` `url` }}"
    headers:
      - name: Authorization
        value: "{{ secret `my-secret` `token` }}"
```

ConfigMap references use the same syntax:

```yaml
dynamic:
  provider:
    type: HTTP
    url: "{{ configmap `my-config` `url` }}"
    headers:
      - name: Authorization
        value: "{{ configmap `my-config` `token` }}"
```

### Status and Conditions

The Dictionary status includes:

* `id`: Assigned dictionary UUID
* `organizationId`: Organization identifier
* `environmentId`: Environment identifier
* `conditions`: Array of condition objects
* `errors`: Object containing `severe` and `warning` arrays

The `conditions` array tracks resource state:

| Condition | Description |
|:----------|:------------|
| `Accepted` | Indicates successful creation in APIM |
| `ResolvedRefs` | Validates the `contextRef` points to an existing `ManagementContext` |

The operator sets the following annotations:

| Annotation | Purpose |
|:-----------|:--------|
| `gravitee.io/last-spec-hash` | Triggers reconciliation when spec changes |
| `gravitee.io/automation-api-managed` | Marks dictionaries managed via Automation API |

The `errors` object is populated during admission validation and contains validation failures categorized by severity.
