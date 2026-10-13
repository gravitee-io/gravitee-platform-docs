---
description: The AMReporter custom resource declares an audit reporter of an Access Management security domain for the Gravitee Kubernetes Operator 4.13. See its fields and how to get the default reporter back.
---

# AMReporter

The `AMReporter` custom resource declares a reporter of a security domain in Gravitee Access Management (AM). A reporter stores the audit events of the domain. The resource names the [`AMSecurityDomain`](amsecuritydomain.md) it belongs to, and GKO creates, updates, and deletes the reporter under that domain, through the domain's [`AMContext`](amcontext.md).

## Overview

The `domainRef` is required, can't change, and must name an `AMSecurityDomain` in the same namespace as the reporter. In AM, the key of the reporter is the namespace and the name of the resource joined with a hyphen. The rules of a domain key apply: lowercase letters, digits, and hyphens, up to 255 characters.

You can apply the reporter before its domain. It's stored with a warning, its `ResolvedRefs` condition stays `False` until AM has created the domain, and GKO then creates the reporter. The domain owns the reporter: deleting the `AMSecurityDomain` deletes the reporter in AM and removes the `AMReporter` resource.

AM creates no default reporter for a domain that GKO creates. To get the reporter that AM builds from its own configuration, apply an `AMReporter` with `system: true`. Only `domainRef` and `system` are needed then. The `name`, `type`, `configuration`, `attributeMappings`, and `attributeMappingEventTypes` fields are ignored, with a warning when they're set, and the status shows the name and type AM gave the reporter. A domain has at most one system reporter. The `system` flag can't change once the resource is created.

The `type` names an AM reporter plugin, such as `reporter-am-file` or `reporter-am-kafka`, and `configuration` holds the settings of that plugin as a free-form object. For the plugins and their settings, see [Reporters](https://documentation.gravitee.io/am/getting-started/configuration/configure-reporters) in the Access Management documentation. The `type` can't change once the resource is created. A value in `configuration` can come from a Kubernetes Secret through a template. See [Templating](../../guides/templating.md). AM returns the sensitive values of the configuration masked, as `********`, and GKO treats a masked value as unchanged when it compares the resource with AM.

When you apply the resource, GKO checks it with AM before Kubernetes accepts it. AM validates the resource in a dry run, without creating or changing anything in AM:

- If AM reports an error, Kubernetes rejects the resource.
- If AM reports a warning, Kubernetes accepts the resource and shows you the warning.
- If AM can't be reached, Kubernetes rejects the resource.

GKO skips this check when the parent AMSecurityDomain hasn't been created in AM yet. Kubernetes accepts the resource with a warning, and GKO creates the resource in AM once the domain exists.
See [Admission validation](../admission-validation.md) and [Drift detection](../drift-detection.md).

Deleting the resource deletes the reporter in AM. A reporter already deleted in AM, or deleted with its domain, doesn't block the deletion.

## Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: banking-audit
  namespace: production
stringData:
  password: <password>
---
apiVersion: gravitee.io/v1alpha1
kind: AMReporter
metadata:
  name: audit-kafka
  namespace: production
spec:
  domainRef:
    name: banking
  name: Banking audit to Kafka
  type: reporter-am-kafka
  configuration:
    bootstrapServers: kafka.banking.svc:9092
    topic: banking-audit
    acks: "1"
    username: gravitee
    password: "[[ secret `banking-audit/password` ]]"
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.domainRef` | `name` of the `AMSecurityDomain`, in the same namespace. Required, and can't change |
| `spec.name` | Name of the reporter. Required unless `system` is `true` |
| `spec.type` | Reporter plugin. Required unless `system` is `true`, and can't change |
| `spec.configuration` | Settings of the plugin, as a free-form object. Required unless `system` is `true` |
| `spec.enabled` | Whether the reporter is on. Defaults to `true` |
| `spec.system` | Whether the resource is the domain's system reporter, built by AM. Defaults to `false`, and can't change |
| `spec.attributeMappings` | Extra attributes exported with each audit event. Each entry pairs an `expression` evaluated against the audit context with the `exportedName` its value takes |
| `spec.attributeMappingEventTypes` | Audit event types the attribute mappings apply to. Every type when empty |

## Validation

* `spec.domainRef` is required, can't change, and names a domain in the same namespace.
* `spec.name`, `spec.type`, and `spec.configuration` are required unless `spec.system` is `true`.
* `spec.type` and `spec.system` can't change.
* The namespace and name of the resource give a key of lowercase letters, digits, and hyphens, up to 255 characters.
* A domain that doesn't exist, or that AM hasn't created yet, gives a warning. The reporter is created once the domain is.
* An error reported by AM rejects the resource. An AM that can't be reached rejects it too.

## Verification

List the reporters of a namespace:

```sh
kubectl get amreporters -n production
```

Next to each resource, the output shows the name and type AM stored, the domain the reporter belongs to, and whether it's on.
