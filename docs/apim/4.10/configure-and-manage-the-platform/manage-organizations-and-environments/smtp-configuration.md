---
description: An overview about smtp configuration.
metaLinks:
  alternates:
    - smtp-configuration.md
---

# SMTP Configuration

## Overview

This section shows the SMTP configuration used for sending email.

You can configure SMTP using `gravitee.yml`, environment variables or directly in APIM Console. If SMTP is configured with `gravitee.yml` or environment variables, then that configuration will be used, even if settings exist in the database.

SMTP can be applied at two different levels:

1. Environment
2. Organization

where the more specific level overrides the broader level: Environment > Organization.

Here's an example of configuring SMTP using the `gravitee.yml` file:

```yaml
email:
  host: smtp.my.domain
  port: 465
  from: noreply@my.domain
  subject: "[Gravitee.io] %s"
  username: user@my.domain
  password: password
```

## Configure in APIM Console

{% hint style="info" %}
If you change the SMTP settings using the `gravitee.yml` or environment variables, then the SMTP settings will be greyed out in the APIM console.
{% endhint %}

You can also configure SMTP at the organization level in the **Organization > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-20 at 3.27.18 PM (1).png" alt=""><figcaption><p>Organization SMTP settings</p></figcaption></figure>

Or at the environment level in the **Settings > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-20 at 3.30.01 PM (1).png" alt=""><figcaption><p>Environment SMTP settings</p></figcaption></figure>

## Configure the Gmail SMTP server

If required, you can configure the GMAIL SMTP server in `gravitee.yml` as follows:

```yaml
email:
  enabled: true
  host: smtp.gmail.com
  port: 587
  from: user@gmail.com
  subject: "[Gravitee.io] %s"
  username: user@gmail.com
  password: xxxxxxxx
  properties:
    auth: true
    starttls.enable: true
    ssl.trust: smtp.gmail.com
```

If you are using 2-Factor Authentication (which is recommended), you need to [generate an application password](https://security.google.com/settings/security/apppasswords).
