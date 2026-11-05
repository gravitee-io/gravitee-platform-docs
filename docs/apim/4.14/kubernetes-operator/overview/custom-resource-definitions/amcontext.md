---
description: The AMContext custom resource connects the Gravitee Kubernetes Operator 4.13 to an Access Management organization and environment. See the token it needs and the checks it goes through.
---

# AMContext

The `AMContext` custom resource connects the Gravitee Kubernetes Operator (GKO) to one organization and environment of Gravitee Access Management (AM). An [`AMSecurityDomain`](amsecuritydomain.md) names an `AMContext`, and GKO creates the domain, its identity providers, its certificates, and its reporters in that environment through the AM Automation API.

## Overview

An `AMContext` lives in a namespace. It holds the URL of the AM Management API, the organization and environment to target, and a bearer token. The token is either set inline or read from a Kubernetes Secret that holds a `bearerToken` key. When the Secret reference gives no namespace, GKO looks for the Secret in the namespace of the `AMContext`.

The Automation API is turned off by default in AM. Turn it on before you apply an `AMContext`. See [Automation API](https://documentation.gravitee.io/am/getting-started/configuration/configure-automation-api) in the Access Management documentation.

The token is a service account token or a user's access token. See [Authentication](https://documentation.gravitee.io/am/guides/automation-api#authentication) in the Access Management documentation. The account behind the token needs roles that let it create, read, update, delete, and list security domains, and their certificates, identity providers, and reporters, in the target environment.

When you apply an `AMContext`, GKO checks that the required fields are set and that a referenced Secret exists, then calls AM with the token. An AM that can't be reached gives a warning, and the resource is stored. An error answer from AM, such as a rejected token or a token without the required roles, rejects the resource with the message AM returned.

GKO keeps a Secret that an `AMContext` references from being deleted until no `AMContext` references it. An `AMContext` can't be deleted while an `AMSecurityDomain` references it: the error gives the number of domains and a `kubectl` command that lists them. A domain that's being deleted still counts until it's gone.

The fields of an `AMContext` accept templates. See [Templating](../../guides/templating.md).

## Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: am-automation-token
  namespace: gravitee
stringData:
  bearerToken: <token>
---
apiVersion: gravitee.io/v1alpha1
kind: AMContext
metadata:
  name: am-ctx
  namespace: gravitee
spec:
  baseUrl: https://am-api.example.com
  organizationId: DEFAULT
  environmentId: DEFAULT
  auth:
    secretRef:
      name: am-automation-token
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.baseUrl` | URL of the AM Management API, starting with `http://` or `https://`. Required |
| `spec.path` | Path that GKO appends to `baseUrl` in place of `/automation`, when AM is reverse proxied behind a URL rewrite |
| `spec.organizationId` | Organization to target. Required |
| `spec.environmentId` | Environment to target, within the organization. Required |
| `spec.auth.bearerToken` | The token, set inline |
| `spec.auth.secretRef` | `name`, and optional `namespace`, of a Secret that holds the token under a `bearerToken` key |

## Validation

* `spec.baseUrl`, `spec.organizationId`, and `spec.environmentId` are required, and `spec.baseUrl` must start with `http://` or `https://`.
* `spec.auth` is required, with either `bearerToken` or `secretRef`.
* A Secret named in `spec.auth.secretRef` must exist when the resource is applied.
* An error answer from AM rejects the resource. An AM that can't be reached gives a warning.
* An `AMContext` that an `AMSecurityDomain` references can't be deleted.

## Verification

List the contexts of a namespace:

```sh
kubectl get amcontexts -n gravitee
```

The `BASEURL` column shows the AM URL. Open a context with `-o yaml` to read its `status`: the `Accepted` and `ResolvedRefs` conditions are `True` once GKO has accepted it.
