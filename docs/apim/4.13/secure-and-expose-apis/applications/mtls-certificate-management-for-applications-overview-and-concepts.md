# mTLS certificate management for applications

## Overview

mTLS certificate management lets application owners upload, rotate, and retire client certificates for mutual TLS authentication directly from the new Developer Portal, without raising tickets to platform administrators. Administrators control whether the feature is exposed to application owners through a per-environment toggle in the Management Console.

{% hint style="info" %}
This feature is Enterprise Edition only and only appears in the **new** Developer Portal. It isn't available in the classic Developer Portal.
{% endhint %}

## Key concepts

### Client certificates

A client certificate identifies an application when it subscribes to an mTLS plan. Each certificate has a name, a PEM-encoded body, and optional `startsAt` and `endsAt` dates that control when it's eligible to authenticate subscriptions. Gravitee extracts and persists the certificate's expiration, subject, issuer, and SHA-256 fingerprint during upload.

### Certificate status

A certificate's status is derived from its activation window and whether it's been replaced:

| Status | Meaning |
|:-------|:--------|
| `ACTIVE` | Currently active with no end date set. |
| `ACTIVE_WITH_END` | Currently active with a scheduled end date. |
| `SCHEDULED` | Uploaded but not yet active (`startsAt` is in the future). |
| `REVOKED` | No longer valid — either the end date has passed or it was explicitly deleted. |

In the new Developer Portal, non-revoked certificates appear in the **Active certificates** tab and revoked certificates appear in the **Certificate history** tab.

### Grace-period rotation

When an application owner uploads a new certificate while another certificate is already active, the portal prompts for a **grace period end** date on the currently active certificate. During the grace period both certificates authenticate subscriptions, so traffic doesn't fail while clients cut over. The grace period end can't be later than the currently active certificate's own expiration date. Once the grace period ends, the old certificate is revoked automatically.

### Fingerprint uniqueness

Gravitee computes a SHA-256 fingerprint for every uploaded certificate and rejects uploads whose fingerprint is already in use by a non-revoked certificate bound to another active application in the same environment. This prevents the same private key from being used by two applications at once.

## Constraints

- The certificate body must be a valid X.509 certificate in PEM format. CA certificates (certificates with `basicConstraints` set) are rejected.
- If the PEM contains a chain, only the first certificate is stored.
- The certificate name can't be longer than 255 characters.
- The file picker in the portal accepts `.pem`, `.crt`, and `.cer` extensions. If you paste PEM text directly, any extension restriction doesn't apply.
- You can't delete the last certificate of an application while that application has active mTLS subscriptions — delete the subscriptions or upload a replacement first.

## Required permissions

Application owners who open the Developer Portal need the following permissions on the application:

| Permission | Used for |
|:-----------|:---------|
| `APPLICATION_DEFINITION[READ]` | Viewing the Certificates section and listing existing certificates. |
| `APPLICATION_DEFINITION[UPDATE]` | Uploading, updating, and deleting certificates through the Developer Portal. |

## Related pages

- [Configuring mTLS certificate management (administrator guide)](../../developer-portal/new-developer-portal/configuring-mtls-certificate-management-administrator-guide.md)
- [Creating and managing mTLS certificates (application owner guide)](../../developer-portal/new-developer-portal/creating-and-managing-mtls-certificates-application-owner-guide.md)
- [mTLS certificate management API reference](../../configure-and-manage-the-platform/management-api/mtls-certificate-management-api-reference.md)
