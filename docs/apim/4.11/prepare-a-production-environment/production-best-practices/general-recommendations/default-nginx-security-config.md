---
description: Guide on applying policies related to default nginx security config.
metaLinks:
  alternates:
    - default-nginx-security-config.md
---

# Default Nginx Security Config

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
