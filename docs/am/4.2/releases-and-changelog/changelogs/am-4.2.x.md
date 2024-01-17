---
description: >-
  This page contains the changelog entries for AM 4.2.x and any future minor or
  patch AM 4.2.x releases
---

# AM 4.2.x


## Gravitee Access Management 4.2.1 - January 17, 2024

<details>
<summary>Bug fixes</summary>
**Gateway**

* Avoid BodyHandler processing for GET request https://github.com/gravitee-io/issues/issues/9352[#9352]
* WebAuthnCredentialId is null into the EL context https://github.com/gravitee-io/issues/issues/9455[#9455]

**Other**

* AEConnector not initialized properly since AM 4.1 https://github.com/gravitee-io/issues/issues/9454[#9454]
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
