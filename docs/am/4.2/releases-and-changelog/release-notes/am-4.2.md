---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.2
---

# AM 4.2

## Secret provider plugins

Gravitee 4.2 offers a set of `secret-provider` plugins that enable Secret Managers to configure Gravitee API Management and Access Management. Secret providers are generic, configurable, and autonomous clients used to:

* Extend the operable range Secret Managers to resolve and watch secrets
* Retrieve sensitive information (passwords, x509 pairs, etc.) from Secret Managers to ensure this information does not appear in clear text
* Manage connections, retries, and credentials renewal when connecting to Secret Managers.&#x20;

Two `secret-provider` plugins are available for Gravitee Gateway, Management API, and Access Management:

* `kubernetes`: A Community Edition plugin that fetches secret and TLS pairs from Kubernetes.io
* `vault`: An Enterprise Edition plugin that uses the Key/Value engine of HashiCorp Vault

For more information, refer to [this page](docs/am/4.2/getting-started/configuration/secret-providers.md).

## SMS factor

Gravitee 4.2 supports a new SMS resource provider based on the SFR vendor. Administrators can set up their SFR credentials to link Gravitee AM to SFR SMS service and activate the MFA SMS factor for selected applications. For more information, see [this section](docs/am/4.2/guides/multi-factor-authentication/factors.md#sms).

## Remember device

Gravitee 4.2 includes enhancements to the Remember Device feature that provides login authentication. After setting up an identifier for your authentication device, you can elect conditional MFA, supply a rule based on context attributes, and toggle **Skip Remember Device collection if conditional MFA evaluates no risk** to ON. If the condition is met, you can bypass MFA when logging in, regardless of other Remember Device settings.&#x20;

<figure><img src="../../.gitbook/assets/skip remember device.png" alt=""><figcaption><p>AM authentication device</p></figcaption></figure>

For more information on configuring an authentication device, see [this page](docs/am/4.2/guides/login/remember-authentication-device.md).&#x20;

## Client secret hash

Gravitee 4.2 offers the option for the client secret to store a hashed value in the AM Database. The algorithm used to hash the client secret can be specified in the `gravitee.yaml` for both [AM Management API](../../getting-started/configuration/configure-am-api/) and [AM Gateway](../../getting-started/configuration/configure-am-gateway/). Available algorithms are:

* None (default)
* SHA-256
* SHA-512
* BCrypt
* PBKDF2.

{% hint style="warning" %}
The client secret will no longer be available through the AM Console or Management API. The secret will be provided only once, after the application creation or after the secret renewal. Before upgrading to AM 4.2, make sure to copy the client secret of your existing applications.

<img src="../../.gitbook/assets/copy-client-secret.png" alt="" data-size="original">
{% endhint %}

{% hint style="info" %}
If you decide to hash the client secret, the authentication method `client_secret_jwt` will no longer be available.
{% endhint %}
