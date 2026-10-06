---
description: Upload, rotate, and retire client certificates for mutual TLS on an API Management 4.13 application. Learn how certificate management works.
---

# mTLS certificate management for applications

## Overview

An application that subscribes to an [mTLS plan](../plans/mtls.md) holds one or more client certificates. The Gateway accepts a call when the certificate that the client presents matches an active certificate of an application that holds a subscription to the plan.

Because an application holds several certificates at once, you rotate a certificate without interrupting traffic. Add the new certificate, keep the old one active for a grace period while your clients switch, and let APIM revoke the old one when the grace period ends.

You manage the certificates of an application from the following places.

| Surface                                   | Where the certificates are                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| APIM Console                              | The **Certificates** section of the application's **Global settings** page. See [Global Settings](global-settings.md).                                                                                                                                                                                                                                                                                                                                                                                  |
| New Developer Portal                      | The **Certificates** section of the application's **Settings & Security** tab, in edit mode, once an administrator turns on **Enable mTLS Certificate Management** for the environment. See [Configure mTLS certificate management (administrator guide)](../../developer-portal/new-developer-portal/configuring-mtls-certificate-management-administrator-guide.md) and [Create and manage mTLS certificates (application owner guide)](../../developer-portal/new-developer-portal/creating-and-managing-mtls-certificates-application-owner-guide.md). |
| Management API and Portal API             | The certificates endpoints of the application. See [mTLS certificate management API reference](../../configure-and-manage-the-platform/management-api/mtls-certificate-management-api-reference.md).                                                                                                                                                                                                                                                                                             |
| Gravitee Kubernetes Operator (GKO)        | The `spec.settings.tls.clientCertificates` list of an `Application` resource. See [Kubernetes CRD Configuration for Client Certificates](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/kubernetes-crd-configuration-for-client-certificates).                                                                                                                                                                                                                       |
| Terraform                                 | The `settings.tls.client_certificates` list of the `apim_application` resource. See the [Certificate rotation](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_rotation-tutorial) tutorial in the Terraform Registry.                                                                                                                                                                                                                                             |

{% hint style="info" %}
Managing certificates from the Console, the APIs, GKO, and Terraform doesn't depend on your license. Self-service management by application owners is an Enterprise Edition feature. The **New Developer Portal** section of the portal settings, which holds the **Enable mTLS Certificate Management** toggle, appears in the Console only with an Enterprise Edition license.
{% endhint %}

## Certificate status

Every certificate carries an optional start date and an optional end date. APIM computes the status of a certificate from those two dates. The Console and the New Developer Portal show the same status under different names.

| Status            | Condition                                                                | Console shows                                                                              | New Developer Portal shows                                        |
| ----------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| `ACTIVE`          | No end date, and no start date or a start date in the past.              | **Active**                                                                                 | **Active** in the **Active certificates** tab                     |
| `ACTIVE_WITH_END` | An end date in the future, and no start date or a start date in the past. | **Active**, or the number of days left when the end date is 15 days away or less          | **Active with end** in the **Active certificates** tab            |
| `SCHEDULED`       | A start date in the future.                                              | **Scheduled**                                                                              | **Scheduled** in the **Active certificates** tab                  |
| `REVOKED`         | An end date in the past.                                                 | **Expired**                                                                                | **Revoked** in the **Certificate history** tab                    |

APIM recomputes the status when you add a certificate, when you edit its dates, and when the [scheduled job](#scheduled-activation-and-automatic-revocation) runs. Between two runs of the job, a certificate whose start or end date has passed keeps its previous status.

## What the Gateway trusts

The Gateway never reads the certificates of an application directly. APIM copies the active certificates of the application into each of its mTLS subscriptions, and the Gateway loads the certificates of every subscription into an in-memory truststore.

* Only certificates with the status `ACTIVE` or `ACTIVE_WITH_END` reach the Gateway. A `SCHEDULED` certificate reaches it once the job activates it, and a `REVOKED` certificate is withdrawn.
* The Gateway identifies the calling application by the SHA-256 fingerprint of the certificate that the client presents, and looks that fingerprint up among the certificates of the subscriptions to the plan.
* When the certificates of a subscription change, the Gateway registers the new certificates before it withdraws the old ones, so traffic isn't cut during a rotation.
* When no active certificate remains on an application, its mTLS subscriptions keep their status but carry no certificate anymore, and the Gateway rejects every call made with the withdrawn certificate.

## Rotate a certificate with a grace period

A rotation replaces the certificate that clients present today with a new one, without a period during which neither is accepted.

1. Add the new certificate. Because a certificate is already active, the Console and the New Developer Portal ask for a grace period end date for the current certificate.
2. APIM creates the new certificate and sets the end date of the current certificate to the grace period end. The current certificate moves to the status `ACTIVE_WITH_END`.
3. Until the grace period ends, both certificates are active and the Gateway accepts either of them. Switch your clients to the new certificate during that time.
4. When the grace period ends, the scheduled job revokes the old certificate and updates the mTLS subscriptions of the application.

In the Console, the grace period end can't be later than the expiration date of the current certificate. In the New Developer Portal, it can't be later than the **Active until** date of the current certificate when one is set.

Through the APIs, GKO, or Terraform, you perform the same rotation by adding the new certificate and setting the `endsAt` date of the current one in the same update.

## Scheduled activation and automatic revocation

A scheduled job of the Management API applies the start and end dates. On each run, it activates every `SCHEDULED` certificate whose start date has passed and revokes every `ACTIVE_WITH_END` certificate whose end date has passed. It then updates the mTLS subscriptions of the applications concerned and writes an audit log entry for each certificate it changed.

By default the job is enabled and runs every day at midnight. A certificate is therefore activated or revoked at the next run after its date, up to 24 hours later. To change the schedule, configure the following properties in the `gravitee.yml` file of the Management API. The `cron` value uses the 6-field cron format, with seconds first.

```yaml
services:
  certificate-revocation:
    enabled: true
    cron: "0 0 0 * * *"
```

The APIM Helm chart has no dedicated value for this service.

{% hint style="warning" %}
Nothing prevents you from setting an end date on the last active certificate of an application. When that date passes, the job revokes the certificate and the mTLS subscriptions of the application no longer carry any certificate, so the calls of the application fail until you add a new certificate.
{% endhint %}

## Subscriptions and certificates

* An application needs at least one active certificate to subscribe to an mTLS plan. Otherwise, APIM rejects the subscription with the message `You cannot subscribe to a mTLS plan without a client_certificate configured at application level`.
* An application holds at most one subscription to an mTLS plan per API, not counting rejected and closed subscriptions. A second one is rejected with the message `An other mTLS plan is already subscribed by the same application.`
* When you subscribe, you don't provide a certificate. The subscription records every active certificate of the application.
* Whenever a certificate is added, edited, deleted, activated, or revoked, APIM updates the certificates of the accepted, pending, and paused mTLS subscriptions of the application.

## Validation and constraints

* The certificate must be a PEM-encoded X.509 certificate. A certificate authority certificate is rejected with the message `Certificate Authorities are not supported, requires a client certificate`.
* When the PEM content contains a chain, APIM keeps only the first certificate.
* The start date must be before the end date.
* The name of a certificate has at most 255 characters.
* APIM rejects a certificate whose SHA-256 fingerprint already belongs to a certificate that isn't revoked on an active application of the same environment, with the message `Client certificate with fingerprint [<fingerprint>] is already used by another active application.` Through the Console, the New Developer Portal, and the certificates endpoints, this check also rejects a certificate that the same application already holds.
* You can't change the content of a certificate after you add it. Edit its name, start date, or end date, or add a new certificate.
* Deleting a certificate removes it from APIM immediately and updates the mTLS subscriptions of the application. A certificate that reaches its end date isn't deleted. It stays listed with the status `REVOKED`.
* You can't delete the last active certificate of an application that has accepted, pending, or paused mTLS subscriptions. APIM rejects the deletion with the message `Client certificate cannot be revoked for application '<application ID>': active subscriptions exist, and this is the last certificate.` Add a replacement first, or close the subscriptions.

## Who can manage certificates

In the Console, anyone who opens the **Global settings** page of the application sees its certificates and their details. The **Add certificate** button is shown only to users who are allowed to update the application. The **Revoke certificate** action is shown to everyone, but the deletion succeeds only for users who are allowed to delete the application definition. When the application is archived or managed by GKO, the Console shows neither **Add certificate** nor **Revoke certificate**, so the certificates of a GKO-managed application are changed through the `Application` resource.

In the New Developer Portal, the **Certificates** section is part of the edit form of the **Settings & Security** tab, so only members who are allowed to update the application see it and manage certificates.

## Upgrade from a single certificate

Before APIM 4.11, an application held a single client certificate. When you upgrade, APIM converts that certificate into a certificate named after the application, with no start date and no end date. When the stored certificate can't be parsed, APIM logs a warning and the application ends up with no certificate, so add one again after the upgrade.

The application endpoints of the Management API and the Portal API keep exposing the single `client_certificate` field for compatibility. See [mTLS certificate management API reference](../../configure-and-manage-the-platform/management-api/mtls-certificate-management-api-reference.md) for what each endpoint returns and accepts.

## Related pages

* [mTLS](../plans/mtls.md)
* [Global Settings](global-settings.md)
* [Configure mTLS certificate management (administrator guide)](../../developer-portal/new-developer-portal/configuring-mtls-certificate-management-administrator-guide.md)
* [Create and manage mTLS certificates (application owner guide)](../../developer-portal/new-developer-portal/creating-and-managing-mtls-certificates-application-owner-guide.md)
* [mTLS certificate management API reference](../../configure-and-manage-the-platform/management-api/mtls-certificate-management-api-reference.md)
