---
description: Overview of Filter.
noIndex: true
---

# Filter

## The Filter Resource (v3alpha1)

The `Filter` custom resource works in conjunction with the [FilterPolicy custom resource](../filterpolicy.md) to define how and when Ambassador Edge Stack will modify or intercept incoming requests before sending them to your upstream Service. `Filters` define what actions to take on a request, while `FilterPolicies` define the matching criteria for requests, such as the headers, hostname, and path, and supply references to one or more `Filters` to execute against those requests. Filters are largely used to add built-in authentication and security, but Ambassador Edge Stack also supports developing custom filters to add your own processing and logic.

This doc is an overview of all the fields on the `Filter` Custom Resource with descriptions of the purpose, type, and default values of those fields. This page is specific to the `getambassador.io/v3alpha1` version of the `Filter` resource. For the newer `gateway.getambassador.io/v1alpha1` resource, please see the [v1alpha1 Filter api reference](../../gateway.getambassador.io-v1alpha1/filter/).

{% hint style="info" %}
Filtering actions of all types in Ambassador Edge Stack are only ever executed on incoming requests and not on responses from your upstream Services.
{% endhint %}

{% hint style="info" %}
`v3alpha1` `Filters` can only be referenced from `v3alpha1` `FilterPolicies`.
{% endhint %}

### v3alpha1 Filter API Reference

Filtering is configured using `Filter` custom resources. The body of the resource `spec` depends on the filter type:

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Filter
metadata:
  name: "example-filter"
  namespace: "example-namespace"
spec:
  ambassador_id: []string           # optional
  JWT:           JWTFilter          # optional
  OAuth2:        OAuth2Filter       # optional
  APIKey:        APIKeyFilter       # optional
  External:      ExternalFilter     # optional
  plugin:        PluginFilter       # optional
```

#### FilterSpec

Other than `ambassador_id`, only one of the following fields may be configured. For example you cannot create a `Filter` with both `JWT` and `External`.

| **Field**       | **Type**                                      | **Description**                                                                                                                                                                                                                                                                                                  |
| --------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ambassador_id` | \[]`string`                                   | Ambassador id accepts a list of strings that allow you to restrict which instances of Ambassador Edge Stack can use/view this resource. If `ambassador_id` is configured, then only Deployments of Ambassador Edge Stack with a matching `AMBASSADOR_ID` environment variable will be able to use this resource. |
| `JWT`           | [JWTFilter](the-jwt-filter-type.md)           | Provides configuration for the JWT Filter type                                                                                                                                                                                                                                                                   |
| `OAuth2`        | [OAuth2Filter](the-oauth2-filter-type.md)     | Provides configuration for the OAuth2 Filter type                                                                                                                                                                                                                                                                |
| `APIKey`        | [APIKeyFilter](the-apikey-filter-type.md)     | Provides configuration for the APIKey Filter type                                                                                                                                                                                                                                                                |
| `External`      | [ExternalFilter](the-external-filter-type.md) | Provides configuration for the External Filter type                                                                                                                                                                                                                                                              |
| `Plugin`        | [PluginFilter](the-plugin-filter-type.md)     | Provides configuration for the Plugin Filter type                                                                                                                                                                                                                                                                |
