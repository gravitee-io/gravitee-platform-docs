---
description: Declare an application of an Access Management security domain with a custom resource of the Gravitee Kubernetes Operator 4.14. See its fields and how it references certificates and identity providers.
---

# `AMApplication`

The `AMApplication` custom resource declares an application of a security domain in Gravitee Access Management (AM): an OAuth 2.0 or OpenID Connect client. It names the [`AMSecurityDomain`](amsecuritydomain.md) it belongs to, and GKO creates, updates, and deletes the application under that domain, through the domain's [`AMContext`](amcontext.md).

## Overview

The `domainRef` is required, can't change, and must name an `AMSecurityDomain` in the same namespace as the application. In AM, the key of the application is the namespace and the name of the resource joined with a hyphen. The rules of a domain key apply: lowercase letters, digits, and hyphens, up to 255 characters.

You can apply the application before its domain. It's stored with a warning, its `ResolvedRefs` condition stays `False` until AM has created the domain, and GKO then creates the application. The domain owns the application: deleting the `AMSecurityDomain` deletes the application in AM and removes the `AMApplication` resource.

An application has no client secret until an [`AMClientSecret`](amclientsecret.md) references it.

The application names the certificate that signs its tokens in one of two ways:

* `certificateRef` names an [`AMCertificate`](amcertificate.md) of the same namespace and domain. GKO waits for that resource to exist before it creates the application, and the `ResolvedRefs` condition stays `False` until then.
* `certificate` holds the key of a certificate in AM, or `id:` followed by its identifier, for a certificate that GKO doesn't manage. Neither GKO nor AM checks that the certificate exists, so the application is created right away, and the reference resolves as soon as the certificate exists in AM.

Each item of `identityProviders` names an identity provider the same way, with `identityRef` for an [`AMIdentityProvider`](amidentityprovider.md) or `identity` for a key in AM. A reference to an `AMCertificate` or an `AMIdentityProvider` of another domain, or of another namespace, is rejected. While an application uses an `AMCertificate` or an `AMIdentityProvider` through a reference or through its key, GKO refuses to delete that resource.

The `clientId` is optional. When it's not set, AM generates one, and `status.clientId` shows the client ID AM holds. Once `clientId` is set in the resource, it can't change or be removed.

The `type` can change, except to or from `agent`, which AM rejects. To change it, delete the resource and create it again. The `settings` field holds the settings of the application, such as its OAuth 2.0 settings in `oauth`, with the same fields as the Automation API. For the settings and the rules AM applies, see [Automation API](https://documentation.gravitee.io/am/guides/automation-api) in the Access Management documentation. Setting `enabled` to `false` revokes the application's tokens. The fields of the resource accept templates. See [Templating](../../guides/templating.md).

When you apply the resource, GKO checks it with AM before Kubernetes accepts it. AM validates the resource in a dry run, without creating or changing anything in AM:

- If AM reports an error, Kubernetes rejects the resource.
- If AM can't be reached, Kubernetes rejects the resource.

GKO skips this check when the parent `AMSecurityDomain` hasn't been created in AM yet. Kubernetes accepts the resource with a warning, and GKO creates the resource in AM once the domain exists.
See [Admission validation](../admission-validation.md) and [Drift detection](../drift-detection.md).

Deleting the resource deletes the application in AM, with its client secrets. An application already deleted in AM, or deleted with its domain, doesn't block the deletion.

## Example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: AMApplication
metadata:
  name: mobile-app
  namespace: production
spec:
  domainRef:
    name: banking
  name: Mobile app
  type: native
  certificateRef:
    name: signing
  identityProviders:
    - identityRef:
        name: inline-users
      priority: 0
  settings:
    oauth:
      redirectUris: ["com.example.mobile://callback"]
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.domainRef` | `name` of the `AMSecurityDomain`, in the same namespace. Required, and can't change |
| `spec.name` | Name of the application, also used as its client name. Required |
| `spec.type` | `web`, `native`, `browser`, `service`, `resource_server`, or `agent`. Required |
| `spec.kind` | For an `agent` application, `USER_EMBEDDED`, `HOSTED_DELEGATED`, or `AUTONOMOUS`. Required when `type` is `agent` |
| `spec.certificateRef` | `name` of the `AMCertificate` that signs the tokens, in the same namespace and domain. Set this field or `spec.certificate` |
| `spec.certificate` | Key of a certificate in AM, or `id:` followed by its identifier. Set this field or `spec.certificateRef` |
| `spec.identityProviders` | Identity providers users sign in with. Each item sets `identityRef`, the `name` of an `AMIdentityProvider`, or `identity`, a key in AM, plus its `priority` and an optional `selectionRule` |
| `spec.clientId` | Client ID of the application. AM generates one when it's not set. Can't change or be removed once set |
| `spec.enabled` | Whether the application is enabled. Defaults to `true` |
| `spec.settings` | Settings of the application, such as its OAuth 2.0 settings in `oauth` |
| `status.clientId` | Client ID that AM holds for the application |

## Validation

* `spec.domainRef` is required, can't change, and names a domain in the same namespace.
* `spec.name`, `spec.type`, and `spec.domainRef` are required, and exactly one of `spec.certificate` and `spec.certificateRef` is set.
* Each item of `spec.identityProviders` sets exactly one of `identity` and `identityRef`.
* `spec.certificateRef` and each `identityRef` name a resource in the same namespace and domain as the application.
* Once set, `spec.clientId` can't change or be removed. A `spec.clientId` that differs from `status.clientId` is rejected.
* The namespace and name of the resource give a key of lowercase letters, digits, and hyphens, up to 255 characters.
* A domain, an `AMCertificate`, or an `AMIdentityProvider` that doesn't exist yet gives a warning. The application is created once they exist.
* An error reported by AM rejects the resource. An AM that can't be reached rejects it too.

## Verification

List the applications of a namespace:

```sh
kubectl get amapplications -n production
```

Next to each resource, the output shows its type, the client ID AM holds, its domain, and whether it's enabled.
