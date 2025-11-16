---
noIndex: true
---

# Filter

## The Filter Resource (v1alpha1)

The `Filter` custom resource works in conjunction with the [FilterPolicy custom resource](../filterpolicy.md) to define how and when Ambassador Edge Stack will modify or intercept incoming requests before sending them to your upstream Service. `Filters` define what actions to take on a request, while `FilterPolicies` define the matching criteria for requests, such as the headers, hostname, and path, and supply references to one or more `Filters` to execute against those requests. Filters are largely used to add built-in authentication and security, but Ambassador Edge Stack also supports developing custom filters to add your own processing and logic.

This doc is an overview of all the fields on the `Filter` Custom Resource with descriptions of the purpose, type, and default values of those fields. This page is specific to the `gateway.getambassador.io/v1alpha1` version of the `Filter` resource. For the older `getambassador.io/v3alpha1` resource, please see the [v3alpha1 Filter api reference](../../getambassador.io-v3alpha1/filter/README.md).

{% hint style="info" %}
`v1alpha1` `Filters` can only be referenced from `v1alpha1` `FilterPolicies`.&#x20;
{% endhint %}

{% hint style="info" %}
Filtering actions of all types in Ambassador Edge Stack are only ever executed on incoming requests and not on responses from your upstream Services.
{% endhint %}

### Filter API Reference

Filtering is configured using `Filter` custom resources. The body of the resource `spec` depends on the filter type:

```yaml
---
apiVersion: gateway.getambassador.io/v1alpha1
kind: Filter
metadata:
  name: "example-filter"
  namespace: "example-namespace"
spec:
  type:      Enum               # required
  jwt:       JWTFilter          # optional, required when `type: "jwt"`
  oauth2:    OAuth2Filter       # optional, required when `type: "oauth2"`
  apikey:    APIKeyFilter       # optional, required when `type: "apikey"`
  external:  ExternalFilter     # optional, required when `type: "external"`
  plugin:    PluginFilter       # optional, required when `type: "plugin"`
status:      []metav1.Condition # field managed by controller, max items: 8
```

#### FilterSpec

| **Field**  | **Type**                                                       | **Description**                                                                                       |
| ---------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `type`     | `Enum` (`"jwt"`/`"oauth2"`/`"apikey"`/`"external"`/`"plugin"`) | Required field that identifies the type of the Filter that is configured to be executed on a request. |
| `jwt`      | [JWTFilter](the-jwt-filter-type.md)                            | Provides configuration for the JWT Filter type                                                        |
| `oauth2`   | [OAuth2Filter](the-oauth2-filter-type.md)                      | Provides configuration for the OAuth2 Filter type                                                     |
| `apikey`   | [APIKeyFilter](the-apikey-filter-type.md)                      | Provides configuration for the APIKey Filter type                                                     |
| `external` | [ExternalFilter](the-external-filter-type.md)                  | Provides configuration for the External Filter type                                                   |
| `plugin`   | [PluginFilter](the-plugin-filter-type.md)                      | Provides configuration for the Plugin Filter type                                                     |

#### FilterStatus

This field is set automatically by Ambassador Edge Stack to provide info about the status of the `Filter`.

| **Field**    | **Type**                                                                                 | **Description**                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `conditions` | \[][metav1.Condition](https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Condition) | Describes the current conditions of the WebApplicationFirewall, known conditions are `Accepted`;`Ready`;`Rejected` |

{% hint style="info" %}
The short name for `Filter` is `fil`, so you can get filters using `kubectl get filter` or `kubectl get fil`.
{% endhint %}
