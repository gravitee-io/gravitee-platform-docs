---
description: An overview about protections.
---

# Protections

## Overview

This page discusses the following:

* [Brute-force protection](protections.md#brute-force-protection)
* [Browser protection](protections.md#browser-protection)

## Brute-force protection

### ReCaptcha

Ensure that ReCaptcha is configured to protect forms against bots and brute-force attempts:

```yaml
# Allows to enable or disable recaptcha (see https://developers.google.com/recaptcha/docs/v3). Currently, it only affect the user registration route.
reCaptcha:
  enabled: true
  siteKey: <your_site_key>
  secretKey: <your_secret_key>
  minScore: 0.5
  serviceUrl: https://www.google.com/recaptcha/api/siteverify
```

Gravitee relies on [ReCaptcha V3](https://developers.google.com/recaptcha/docs/v3?hl=en), which is non-intrusive for the end user. You can obtain your site key and secret key directly from your Google developer account ([https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)).

### Fail2Ban

If your platform is particularly exposed to the outside world, we recommend adding additional protection against pure brute-force attacks by [setting up Fail2Ban](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/security#fail2ban).

Fail2Ban scans log files and automatically bans IPs that show malicious signs, e.g., too many password failures, seeking an opportunity for exploitation, etc.

## Browser protection

### Enable CSRF protection

Cross-site request forgery (CSRF) is a web security vulnerability that allows an attacker to induce users to perform actions that they do not intend to perform. You can protect your end users by checking that the CSRF protection is enabled (enabled by default):

```yaml
http: 
  csrf:
    # Allows to enable or disable the CSRF protection. Enabled by default.
    enabled: true
```

We strongly recommend **NEVER** disabling CSRF protection unless you are absolutely sure of what you are doing and that your users may be exposed to [Cross Site Request Forgery attacks](https://en.wikipedia.org/wiki/Cross-site_request_forgery).

### Configure CORS

CORS is one of the most important things to set up to protect your users and your system against malicious attackers. It allows the user's browser to enable native protection preventing unauthorized websites to perform a JavaScript HTTP call to the Console or REST API. Basically, when well-configured, you only allow your own Console website (e.g., `https://gio-console.mycompany.com`) and Dev Portal website (e.g., `https://gio-portal.mycompany.com`) to make calls from a browser to their respective APIs.

Make sure CORS is well-configured for both the Console AND the Portal APIs:

```yaml
http:
  api:
    management:
      cors:
        allow-origin: 'https://gio-console.mycompany.com'
    portal:
      cors:
        allow-origin: 'https://gio-portal.mycompany.com'
```

`allow-origin: '*'` should be considered a security risk because it permits all cross-origin requests. **We highly recommend fine-tuning the allow-origin setting. Refer to** the [Gravitee documentation](../../configure-v2-apis/proxy-settings.md) for other useful information related to CORS.
