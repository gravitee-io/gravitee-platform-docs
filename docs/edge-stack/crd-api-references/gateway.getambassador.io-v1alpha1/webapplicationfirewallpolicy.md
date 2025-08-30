# WebApplicationFirewallPolicy

## The WebApplicationFirewallPolicy Resource (v1alpha1)

The `WebApplicationFirewallPolicy` resource configures the matching patterns for when [WebApplicationFirewalls](webapplicationfirewall.md) get executed against requests; while the `WebApplicationFirewall` resource provides the configuration for an instance of a Web Application Firewall.

This doc is an overview of all the fields on the `WebApplicationFirewallPolicy` Custom Resource with descriptions of the purpose, type, and default values of those fields. Tutorials and guides for Web Application Firewalls can be found in the [usage guides section](webapplicationfirewallpolicy.md#web-application-firewall-usage-guides)

{% hint style="info" %}
The `WebApplicationFirewallPolicy` resource was introduced more recently than the `Filter` and `FilterPolicy` resources, and does not have an older `getambassador.io/v3alpha1` CRD version
{% endhint %}

### WebApplicationFirewallPolicy API Reference

```yaml
---
apiVersion: gateway.getambassador.io/v1alpha1
kind: WebApplicationFirewallPolicy
metadata:
  name: "example-wafpolicy"
  namespace: "example-namespace"
spec:
  rules:  []WafMatchingRule           # required
  - host: string                      # optional, default: `"*"` (runs on all hosts)
    path: string                      # optional, default: `"*"` (runs on all paths)
    ifRequestHeader: HTTPHeaderMatch  # optional
      type: Enum                      # optional, default: `"Exact"`
      name: string                    # required
      value: string                   # optional
      negate: bool                    # optional, default: `false`
    wafRef:                           # required
      name: string                    # required
      namespace: string               # required
    onError:                          # optional
      statusCode: int                 # required, min: `400`, max: `599`
    precedence: int                   # optional
status:                               # field managed by controller
  conditions: []metav1.Condition
  ruleStatuses:
  - index: int
    host: string
    path: string
    conditions: []metav1.Condition
```

#### WebApplicationFirewallPolicy Spec

| **Field** | **Type**                                                              | **Description**                                                                                                                                                                                                                                          |
| --------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rules`   | \[][WafMatchingRule](webapplicationfirewallpolicy.md#wafmatchingrule) | This object configures matching requests and executes WebApplicationFirewalls on them. Multiple different rules can be supplied in one `WebApplicationFirewallPolicy` instead of multiple separate `WebApplicationFirewallPolicy` resouurces if desired. |

#### WafMatchingRule

| **Field**            | **Type**                                                           | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `host`               | `string`                                                           | A "glob-string" that matches on the `:authority` header of the incoming request. If not set, it will match on all incoming requests.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `path`               | `string`                                                           | A "glob-string" that matches on the request path. If not provided, then it will match on all incoming requests.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `ifRequestHeader`    | [HTTPHeaderMatch](webapplicationfirewallpolicy.md#httpheadermatch) | Checks if exact or regular expression matches a value in a request header to determine if the `WebApplicationFirewall` is executed or not.                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `wafRef`             | [WafReference](webapplicationfirewallpolicy.md#wafreference)       | A reference to a `WebApplicationFirewall` to be applied against the request.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `onError.statusCode` | `int`                                                              | Configure a response code to be sent to the downstream client when when a request matches the rule but there is a configuration or runtime error. By default, requests are allowed on error if this field is not configured. This covers runtime errors such as those caused by networking/request parsing as well as configuration errors such as if the `WebApplicationFirewall` that is referenced is misconfigured, cannot be found, or when its configuration cannot be loaded properly. Details about the errors can be found either in the `WebApplicationFirewall` status or container logs. |

#### HTTPHeaderMatch

**Appears On**: [WafMatchingRule](webapplicationfirewallpolicy.md#wafmatchingrule) Checks if exact or regular expression matches a value in a request header to determine if the `WebApplicationFirewall` is executed or not.

| **Field** | **Type**                                | **Description**                                                                                                                                                                         |
| --------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`    | `Enum`(`"Exact"`,`"RegularExpression"`) | Specifies how to match against the value of the header. Allowed values are `"Exact"`/`"RegularExpression"`.                                                                             |
| `name`    | `string`                                | Name of the HTTP Header to be matched. Name matching MUST be case-insensitive. (See [https://tools.ietf.org/html/rfc7230#section-3.2](https://tools.ietf.org/html/rfc7230#section-3.2)) |
| `value`   | `string`                                | Value of HTTP Header to be matched. If type is `RegularExpression`, then this must be a valid regex with a length of at least 1.                                                        |
| `negate`  | `bool`                                  | Allows the match criteria to be negated or flipped.                                                                                                                                     |

#### WafReference

**Appears On**: [WafMatchingRule](webapplicationfirewallpolicy.md#wafmatchingrule) A reference to a `WebApplicationFirewall`

| **Field**   | **Type**                                                                                                                                                                                                                                                                                                                                 | **Description** |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| `name`      | Name of the `WebApplicationFirewall` being referenced                                                                                                                                                                                                                                                                                    |                 |
| `namespace` | Namespace of the `WebApplicationFirewall`. This field is required. It must be a RFC 1123 label. Valid values include: `"example"`. Invalid values include: `"example.com"` - `"."` is an invalid character. The maximum allowed length is 63 characters, and the regex pattern `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` is used for validation. |                 |

### Web Application Firewall Usage Guides

The following guides will help you get started using Web Application Firewalls

* [using-web-application-firewalls-in-ambassador-edge-stack.md](../../edge-stack-user-guide/web-application-firewalls/using-web-application-firewalls-in-ambassador-edge-stack.md "mention")
* [configuring-web-application-firewall-rules-in-ambassador-edge-stack.md](../../edge-stack-user-guide/web-application-firewalls/configuring-web-application-firewall-rules-in-ambassador-edge-stack.md "mention")
* [using-web-application-firewall-in-production.md](../../edge-stack-user-guide/web-application-firewalls/using-web-application-firewall-in-production.md "mention")
