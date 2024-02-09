---
description: >-
  This page contains the changelog entries for AM 4.2.x and any future minor or
  patch AM 4.2.x releases
---

# AM 4.2.x

## Gravitee Access Management 4.2.3 - February 8, 2024



<details>
<summary>Bug fixes</summary>

**Gateway**

* Invalid form parameter when ResponseMode is set to form_post [#9179](https://github.com/gravitee-io/issues/issues/9179)
* SCIM search operator PR doesn't work as expected [#9265](https://github.com/gravitee-io/issues/issues/9265)
* Authentication flow rejected due to redirect_uri when PAR is used [#9478](https://github.com/gravitee-io/issues/issues/9478)
* MFA challenge should be prompted before registering a passwordless device [#9479](https://github.com/gravitee-io/issues/issues/9479)
* Remember Device Not Functioning with Conditional MFA [#9484](https://github.com/gravitee-io/issues/issues/9484)
* WebAuthn : "Force authenticator integrity" - LastCheckedAt systematically updated at each webauthn login [#9327](https://github.com/gravitee-io/issues/issues/9327)

**Management API**

* Apply timeout on blockingGet in ManagementAPI filters [#9476](https://github.com/gravitee-io/issues/issues/9476)

</details>


## Gravitee Access Management 4.2.2 - January 30, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Passwordless not working for iOS v17.2.1 [#9470](https://github.com/gravitee-io/issues/issues/9470)
* Flow - Add WebAuthn credential register flow (improvement)

</details>

## Gravitee Access Management 4.2.1 - January 17, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Avoid BodyHandler processing for GET request [#9352](https://github.com/gravitee-io/issues/issues/9352)
* WebAuthnCredentialId is null into the EL context [#9455](https://github.com/gravitee-io/issues/issues/9455)

**Other**

* AEConnector not initialized properly since AM 4.1 [#9454](https://github.com/gravitee-io/issues/issues/9454)

</details>

## Gravitee Access Management 4.2 - December 21, 2023

For more in-depth information on what's new, please refer to the [Gravitee AM 4.2 release notes](../release-notes/am-4.2.md).

<details>

<summary>What's new</summary>

**Enterprise Edition**

New SMS resource provider based on the SFR vendor. Administrators can set up their SFR credentials to link Gravitee AM to SFR SMS service and activate the MFA SMS factor for selected applications.

A new Secret Management plugin that uses the Key/Value engine of HashiCorp Vault.

**Community Edition**

A new Secret Management plugin that fetches secret and TLS pairs from Kubernetes.io.

Gravitee AM 4.2 enhancements to the Remember Device feature that provides login authentication.

It is now possible to improve the security of a client secret by storing a hashed value.

Password Policy can be reset at the domain level to fallback to the default policy defined in the `gravitee.yaml`.

</details>

<details>

<summary>Breaking changes</summary>

The client secret will no longer be available through the AM Console or Management API. The secret will be provided only once, after the application creation or after the secret renewal. Before upgrading to AM 4.2, make sure to copy the client secret of your existing applications.

</details>
