---
noIndex: true
---

# EnvoyFilterPolicy

## The EnvoyFilterPolicy Resource (v3alpha1)

The `EnvoyFilterPolicy` custom resource provides a way to manage how Envoy filters are applied to incoming requests in Ambassador Edge Stack. It allows users to define rules that specify which filters to apply, the order in which they're evaluated using precedence, and the specific Ambassador instances they should target. This ensures flexible, consistent, and centralized control over request processing, which enhances security, observability, and traffic management across services.

This document provides an overview of all the fields in the `EnvoyFilterPolicy` custom resource, including their purpose, type, and default values. This page is specific to the `getambassador.io/v3alpha1` version of the `EnvoyFilterPolicy` resource.

### Envoy Filter Policy API Reference

To define an Envoy Filter Policy, set `kind` to `EnvoyFilterPolicy` and provide the desired configuration under the `spec.rules` field.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: EnvoyFilterPolicy
metadata:
  name: "example-envoy-filter-policy"
  namespace: "example-namespace"
spec: EnvoyFilterPolicy
  ambassador_id: []string                # optional, defaults to ["default"]
  rules: []EnvoyFilterPolicyRule         # required, minItems: 1
  - precedence: int                      # optional
    envoyFilters: []EnvoyFilterReference # required
    - name: string                       # required
      namespace: string                  # required
```

The following sections provide resource details formatted into markdown tables for each property, including nested objects.

#### EnvoyFilterPolicy

| **Field**       | **Type**                       | **Description**                                                                               |
| --------------- | ------------------------------ | --------------------------------------------------------------------------------------------- |
| `ambassador_id` | `array[string]`                | Declares which Ambassador instances should watch this resource. The default is `["default"]`. |
| `rules`         | `array[EnvoyFilterPolicyRule]` | Defines rules for how `EnvoyFilter` is applied. It must contain at least one item.            |

***

#### EnvoyFilterPolicyRule

| **Field**      | **Type**                      | **Description**                                                                             |
| -------------- | ----------------------------- | ------------------------------------------------------------------------------------------- |
| `envoyFilters` | `array[EnvoyFilterReference]` | A list of `EnvoyFilter` references.                                                         |
| `precedence`   | `integer`                     | An optional way to specify how rules are ordered when a request matches more than one rule. |

***

#### EnvoyFilterReference

| **Field**   | **Type** | **Description**                     |
| ----------- | -------- | ----------------------------------- |
| `name`      | `string` | The name of the `EnvoyFilter`.      |
| `namespace` | `string` | The namespace of the `EnvoyFilter`. |

***

#### EnvoyFilterPolicy Example

The following example applies an `EnvoyFilterPolicy` to the `payment-services` namespace in both production and staging environments. The rules are organized by precedence, allowing security filters to be applied before observability filters. In this example, precedence ensures that security filters (e.g., authentication and validation) are applied before observability filters (e.g., logging).

```yaml
apiVersion: getambassador.io/v3alpha1
kind: EnvoyFilterPolicy
metadata:
  name: payment-service-filters
  namespace: payment-services
spec:
  ambassador_id:
    - production
    - staging
  rules:
    - precedence: 10
      envoyFilters:
        - name: payment-auth-filter
          namespace: payment-services
        - name: transaction-validation-filter
          namespace: security
    - precedence: 20
      envoyFilters:
        - name: logging-filter
          namespace: observability
```
