---
description: An overview about Configuration Settings.
---

# Configuration Settings

## Overview

This page discusses other configuration settings that fall into the following categories:

* [Property encryption](configuration-settings.md#property-encryption)
* [Documentation sanitizer](configuration-settings.md#documentation-sanitizer)
* [Notifiers](configuration-settings.md#notifiers)
* [Default APIM settings](configuration-settings.md#default-apim-settings)
* [Portal & Console default Nginx security config](configuration-settings.md#portal-and-console-default-nginx-security-config)

## Property encryption

Gravitee allows attaching properties to an API and offers the capability to store encrypted property values. **You must change the default encryption secret** with a custom secret that can't be determined easily. You must consider the following when changing the secret:

* The secret must be **changed for both Management and Gateway** and have the same value.
* The secret must be **32 bytes in length**.
* The secret should ideally be generated with a password generation tool to enforce robustness.
* If you have several installations (e.g., one for dev, one for prod), make sure to **set up different secrets for each installation**.

```yaml
api:
  properties:
    encryption:
         secret: <32 byte length secret>
```

You can find additional details about property encryption in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/policy-design/v2-api-policy-design-studio#encryption).

## Documentation sanitizer

Gravitee offers the capability to attach and expose API documentation. Once published, these pages can be accessible to API consumers to discover and understand the purpose of an API. **We recommend enabling the sanitization of the documentation pages** to avoid any script injection that could have an impact on the API consumer when the page is published on the Developer Portal.

```yaml
documentation:
  markdown:
    sanitize: true
```

## Notifiers

By default, APIM allows an API publisher to send notifications related to its APIs. This includes sending notifications over HTTP, which can be useful for automation. However, we recommend disabling this feature if you don't expect to use it:

```yaml
notifiers:
  email:
    enabled: false
  webhook:
    enabled: false
```

Alternatively, if you need to keep the HTTP notification feature enabled, we recommend establishing a list of allowed URLs to send notifications to:

```yaml
notifiers:
  webhook:
    enabled: true
    # Empty whitelist means all urls are allowed.
    whitelist:
      - https://whitelist.domain1.com
      - https://restricted.domain2.com/whitelisted/path
```

Specifying a list of authorized URLs allows the administrator to restrict URL notifications. This is particularly useful for companies that need to rely on a corporate Webhook system.

## Default APIM settings

Perform the following steps in APIM Console to update the most common default settings.

1. Log in to APIM Console.
2. Select **Settings**.
3. In the **Portal** section:
   1. Select **Settings** in the inner sidebar.
   2.  Update the **Company name.**

       <figure><img src="broken-reference" alt=""><figcaption><p>Portal settings</p></figcaption></figure>
4. In the **Gateway** section:
   1. Select **API Logging**.
   2.  Update the maximum logging duration for APIM API logging to avoid flooding. In this example, we have configured a logging duration of 15 minutes:

       <figure><img src="broken-reference" alt=""><figcaption><p>API logging settings</p></figcaption></figure>
5. Select **Organization** in the main sidebar:
   1. In the **Gateway** section:
      1. Select **Sharding Tags**.
      2.  In the **Entrypoint mappings** section of the page, update the **Entrypoint** field with your APIM API endpoint.

          <figure><img src="broken-reference" alt=""><figcaption><p>Save sharding tag</p></figcaption></figure>
   2. Select **Settings** in the inner sidebar:
      * Update the **Title** of APIM Console to make it more appropriate to your own environment.
      *   Update the **Management URL** to your APIM Console URL.

          <figure><img src="broken-reference" alt=""><figcaption><p>Organization settings</p></figcaption></figure>

## Portal & Console default Nginx security config

The APIM Console uses this default config:

```nginx
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Content-Security-Policy "frame-ancestors 'self';" always;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options nosniff;
    add_header X-Permitted-Cross-Domain-Policies none;
```

The APIM Portal uses this default config:

```nginx
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options nosniff;
    add_header X-Permitted-Cross-Domain-Policies none;
```

It is recommended to make use of these available mechanisms to have better control over the resources the user agent is allowed to load for a given page.

For APIM Portal you can improve security to allow specific origins using these headers:

```nginx
add_header X-Frame-Options "ALLOW-FROM=my-domain.com" always;
add_header Content-Security-Policy "frame-ancestors my-domain.com;" always;
```

{% hint style="info" %}
APIM Management Console uses an iframe to preview the portal theme configuration, so it is necessary to add the Management Console in the Developer Portal Nginx config. Learn more about:

* Content-Security\_policy and framing [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors)
* X-Frame-Options [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)
{% endhint %}
