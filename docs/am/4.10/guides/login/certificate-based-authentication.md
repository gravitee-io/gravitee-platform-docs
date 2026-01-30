# Certificate Based Authentication

## Overview

The Certificate-Based Authentication (CBA) feature extends our Access Management platform with a strong, cryptographically backed method of verifying user identity. Instead of relying on WebAuthN or one-time codes, the user presents a client certificate stored in their browser or operating system, similar in spirit to WebAuthN but based on X.509 certificates. During authentication, the platform validates the certificate’s metadata against the records stored for the user, checks expiration, and uses it as a secure proof of identity. This mechanism provides a seamless, phishing-resistant, and high-assurance login experience for users operating on managed devices or within enterprise security policies.

The CBA authentication flow relies on mTLS to present the client certificate to the Access Management system. Because this step occurs **before** HTTP request resolution, the final setup requires two distinct entry points. The following configurations are supported:

1. **Two AM Gateways** — one of them operating with `SSL_VERIFY_CLIENT` enabled.
2. **A proxy with two IP/PORT entry points** — one configured with `SSL_VERIFY_CLIENT` enabled and performing TLS termination, where the extracted certificate is forwarded to AM in a predefined HTTP header.

## Setup

### Install plugin

The enterprise **gravitee-am-authenticator-cba** must be installed in the Gateway component. Once the plugin is successfully loaded, the following log entry should appear in the server’s standard output:

```
INFO  i.g.a.g.h.v.VertxSecurityDomainHandler - 	 Authenticator cba-authenticator loaded
```

### Gateway settings

&#x20;`auth.cba.jwt.state.ttl` - default is 30. Specifies the TTL (in seconds) of the state token passed between regular and mTLS-enabled hosts.

`http.ssl.certificateHeader` - Header where the peer certificate is read if there are no sslSession (default is null)

### Enable CBA

The CBA can be enabled in two places. For all applications in the domain:

1. Log in to AM Console
2. Go to **Settings** and select **Login** submenu option
3. In **Passwordless** section, enable **Passwordless Certificate Based Authentication** and setup **Base URL**

Or for specific application

1. Log in to AM Console
2. Go to **Applications** and select an application from the list
3. Go to **Settings** and select **Login** tab
4. Disable **Inherit configuration** option
5. In **Passwordless** section, enable **Passwordless Certificate Based Authentication** and setup **Base URL**

The CBA authentication base URL must be configured as the entrypoint where `SSL_VERIFY_CLIENT` is enabled.&#x20;

## Register user's certificate

In order to register User's Certificate credential, go to&#x20;

1. Log in to AM Console
2. In **Settings** go to **Users** page and select a user
3. Go to **Credentials** tab and select **Enroll Certificate** button

{% hint style="info" %}
The option is available only when CBA is enabled on Domain's level or Application's assigned to the user&#x20;
{% endhint %}

The certificate can be added by selecting a file from the browser or by pasting the PEM content&#x20;

{% hint style="info" %}
Within a single domain, only one certificate with a unique thumbprint is allowed.
{% endhint %}

## Sign in

In order to sign in, the Certificate must be installed in local store (browser or system)

When you visit the AM login page, the **Sign in with Certificate using mTLS** option should be visible. Selecting it redirects you to the CBA login page, where clicking **Next** sends you to the mTLS-enabled endpoint. A system dialog displaying the installed client certificates will appear. After selecting and presenting a valid certificate, the user is successfully authenticated.

## Caveats

* AM checks only certificate's **subjectDN**, **issuerDN** and **serialNumber**.
* AM verifies the expiration date of presented certificate during the mTLS connection process.&#x20;
