---
description: The AMSecurityDomain custom resource declares an Access Management security domain for the Gravitee Kubernetes Operator 4.13. See its key, its fields, and what a new domain starts with.
---

# AMSecurityDomain

The `AMSecurityDomain` custom resource declares a security domain in Gravitee Access Management (AM). GKO creates the domain through the [`AMContext`](amcontext.md) the resource names, updates it on every change, and deletes it in AM when you delete the resource.

## Overview

The domain is created in the organization and environment of its `AMContext`. The `contextRef` is required and can't change once the resource is created. When it gives no namespace, GKO looks for the `AMContext` in the namespace of the domain.

In AM, the key of the domain is the namespace and the name of the resource joined with a hyphen, for example `production-banking` for a resource named `banking` in the `production` namespace. The key never changes. AM accepts lowercase letters, digits, and hyphens, up to 255 characters, so a resource whose namespace or name contains a dot is rejected. A key that belongs to a domain created in the AM console or through the Management API is rejected too, because the Automation API only manages the domains it created.

A domain that GKO creates starts empty. AM doesn't give it the default certificate, identity provider, and reporter that a domain created in the console gets. Declare them with [`AMCertificate`](amcertificate.md), [`AMIdentityProvider`](amidentityprovider.md), and [`AMReporter`](amreporter.md) resources. With `system: true`, each of them gives the domain the default that AM builds from its own configuration.

Before the resource is stored, GKO asks AM to validate it without saving it. An error reported by AM rejects the resource, a warning is returned with it, and an AM that can't be reached rejects it. On an update, GKO can also compare the resource with the domain's current state in AM. See [Admission validation](../admission-validation.md) and [Drift detection](../drift-detection.md).

Deleting the resource deletes the domain in AM, with its identity providers, certificates, and reporters. The `AMIdentityProvider`, `AMCertificate`, and `AMReporter` resources that reference the domain are removed with it. A domain already deleted in AM doesn't block the deletion of the resource.

The `dataPlaneId` field is optional when the domain is created, and can't change after that. For how AM picks a data plane when the field isn't set, see [Automation API](https://documentation.gravitee.io/am/guides/automation-api) in the Access Management documentation. The fields of the resource accept templates. See [Templating](../../guides/templating.md).

## Example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: AMSecurityDomain
metadata:
  name: banking
  namespace: production
spec:
  contextRef:
    name: am-ctx
    namespace: production
  name: Banking
  path: /banking
  description: Customer-facing banking applications
  tags:
    - production
  loginSettings:
    forgotPasswordEnabled: true
  accountSettings:
    loginAttemptsDetectionEnabled: true
    maxLoginAttempts: 5
    loginAttemptsResetTime: 600
    accountBlockedDuration: 1800
  corsSettings:
    enabled: true
    allowedOrigins:
      - https://bank.example.com
    allowedMethods:
      - GET
      - POST
    allowedHeaders:
      - Authorization
      - Content-Type
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.contextRef` | `name`, and optional `namespace`, of the `AMContext`. Required, and can't change |
| `spec.name` | Name of the domain. Required |
| `spec.path` | Context path the domain is served under, starting with `/`. Required |
| `spec.description` | Description of the domain |
| `spec.enabled` | Whether the domain handles authentication and authorization requests. Defaults to `true` |
| `spec.dataPlaneId` | Data plane the domain is created on. Optional at creation, and can't change afterwards |
| `spec.tags` | Sharding tags that decide which gateways deploy the domain |
| `spec.vhostMode` and `spec.vhosts` | Expose the domain on virtual hosts instead of its context path |
| `spec.master` | Whether the domain is the master domain of its environment |
| `spec.alertEnabled` | Whether alerting is on for the domain |
| `spec.loginSettings` | The login flow and the features offered on the sign-in page |
| `spec.accountSettings` | Brute-force protection, registration, password reset, remember-me, and MFA challenge settings |
| `spec.passwordSettings` | Password policy of the domain's users |
| `spec.selfServiceAccountManagementSettings` | Whether end users can manage their own account, and the rules that apply |
| `spec.webAuthnSettings` | WebAuthn settings for passwordless and multi-factor authentication |
| `spec.oidc` | OpenID Connect settings: dynamic client registration, CIBA, the security profile, workload identity, and redirect URI matching |
| `spec.saml` | Settings for the domain as a SAML 2.0 identity provider |
| `spec.scim` | SCIM 2.0 provisioning settings |
| `spec.uma` | User-Managed Access 2.0 settings |
| `spec.tokenExchangeSettings` | OAuth 2.0 token exchange settings |
| `spec.keyRetrievalSettings` | Limits on fetching keys from the trusted domains of the security domain |
| `spec.certificateSettings.fallbackCertificate` | Key of an `AMCertificate` of the domain, in the form `<namespace>-<name>`, used when a client doesn't name one |
| `spec.corsSettings` | Cross-origin resource sharing settings |
| `spec.webProtectionSettings` | HTTP security headers of the login and consent pages |
| `spec.secretExpirationSettings` | Whether client secrets expire, and after how long |

For every field, see the [API reference](../../reference/api-reference.md).

## Validation

* `spec.contextRef` is required and can't change.
* `spec.name` and `spec.path` are required, and `spec.path` starts with `/`.
* The namespace and name of the resource give a key of lowercase letters, digits, and hyphens, up to 255 characters.
* `spec.dataPlaneId` can't change once the domain is created.
* An error reported by AM rejects the resource. An AM that can't be reached rejects it too.

## Verification

List the domains of a namespace:

```sh
kubectl get amsecuritydomains -n banking
```

The output shows the name, the path, and whether each domain is enabled. Open a domain with `-o yaml` to read its `status`: `key` holds the key of the domain in AM, and the `Accepted` condition is `True` once AM has created it.
