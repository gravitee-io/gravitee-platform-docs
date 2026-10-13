---
description: The AMIdentityProvider custom resource declares an identity provider of an Access Management security domain for the Gravitee Kubernetes Operator 4.13. See its fields and how it waits for its domain.
---

# AMIdentityProvider

The `AMIdentityProvider` custom resource declares an identity provider of a security domain in Gravitee Access Management (AM). It names the [`AMSecurityDomain`](amsecuritydomain.md) it belongs to, and GKO creates, updates, and deletes the identity provider under that domain, through the domain's [`AMContext`](amcontext.md).

## Overview

The `domainRef` is required, can't change, and must name an `AMSecurityDomain` in the same namespace as the identity provider. In AM, the key of the identity provider is the namespace and the name of the resource joined with a hyphen. The rules of a domain key apply: lowercase letters, digits, and hyphens, up to 255 characters.

You can apply the identity provider before its domain. It's stored with a warning, its `ResolvedRefs` condition stays `False` until AM has created the domain, and GKO then creates the identity provider. The domain owns the identity provider: deleting the `AMSecurityDomain` deletes the identity provider in AM and removes the `AMIdentityProvider` resource.

The `type` names an AM identity provider plugin, such as `inline-am-idp`, and `configuration` holds the settings of that plugin as a free-form object. For the plugins and their settings, see [Identity Providers](https://documentation.gravitee.io/am/guides/identity-providers) in the Access Management documentation. The `type` can't change once the resource is created. A value in `configuration` can come from a Kubernetes Secret through a template. See [Templating](../../guides/templating.md). AM returns the sensitive values of the configuration masked, as `********`, and GKO treats a masked value as unchanged when it compares the resource with AM.

With `system: true`, the resource gives the domain the default identity provider that AM builds from its own configuration. Only `domainRef` and `system` are needed then. The `name`, `type`, and `configuration` fields are ignored, with a warning when they're set, and the status shows the name and type AM gave the identity provider. A domain has at most one system identity provider. The `system` flag can't change once the resource is created.

Before the resource is stored, GKO asks AM to validate it without saving it, unless the domain isn't in AM yet. An error reported by AM rejects the resource, a warning is returned with it, and an AM that can't be reached rejects it. See [Admission validation](../admission-validation.md) and [Drift detection](../drift-detection.md).

Deleting the resource deletes the identity provider in AM. An identity provider already deleted in AM, or deleted with its domain, doesn't block the deletion. AM refuses to delete an identity provider that an application still uses: the resource then stays, and its `Accepted` condition carries the message from AM.

## Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: idp-users
  namespace: production
stringData:
  admin-password: <password>
---
apiVersion: gravitee.io/v1alpha1
kind: AMIdentityProvider
metadata:
  name: inline-users
  namespace: banking
spec:
  domainRef:
    name: banking
  name: Inline users
  type: inline-am-idp
  configuration:
    users:
      - username: admin
        firstname: Admin
        lastname: User
        email: admin@example.com
        password: "[[ secret `idp-users/admin-password` ]]"
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.domainRef` | `name` of the `AMSecurityDomain`, in the same namespace. Required, and can't change |
| `spec.name` | Name of the identity provider. Required unless `system` is `true` |
| `spec.type` | Identity provider plugin. Required unless `system` is `true`, and can't change |
| `spec.configuration` | Settings of the plugin, as a free-form object. Required unless `system` is `true` |
| `spec.system` | Whether the resource is the domain's system identity provider, built by AM. Defaults to `false`, and can't change |
| `spec.mappers` | Maps the attributes the provider returns to attributes of the user profile |
| `spec.roleMapper` | Maps a role to the user attribute values that grant it |
| `spec.groupMapper` | Maps a group to the user attribute values that grant it |
| `spec.domainWhitelist` | Email domains allowed to sign in through the identity provider. When set, a user with another email domain is rejected |

## Validation

* `spec.domainRef` is required, can't change, and names a domain in the same namespace.
* `spec.name`, `spec.type`, and `spec.configuration` are required unless `spec.system` is `true`.
* `spec.type` and `spec.system` can't change.
* The namespace and name of the resource give a key of lowercase letters, digits, and hyphens, up to 255 characters.
* A domain that doesn't exist, or that AM hasn't created yet, gives a warning. The identity provider is created once the domain is.
* An error reported by AM rejects the resource. An AM that can't be reached rejects it too.

## Verification

List the identity providers of a namespace:

```sh
kubectl get amidentityproviders -n banking
```

Next to each resource, the output shows the name and type AM stored and the domain the identity provider belongs to.
