---
description: An overview about smtp configuration.
metaLinks:
  alternates:
    - smtp-configuration.md
hidden: true
noIndex: true
---

# SMTP Configuration

## Overview

This section shows the SMTP configuration used for sending email.

You can configure SMTP using `gravitee.yml`, environment variables or directly in APIM Console. If SMTP is configured with `gravitee.yml` or environment variables, then that configuration will be used, even if settings exist in the database.

SMTP can be applied at two different levels:

1. Environment
2. Organization

where the more specific level overrides the broader level: Environment > Organization.

Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
Update the `email:` section of the Management API `gravitee.yml` file:

```yaml
email:
  host: smtp.my.domain
  port: 465
  from: noreply@my.domain
  subject: "[Gravitee.io] %s"
  username: user@my.domain
  password: password
```
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by `docker-compose.yml`, or to the `environment:` block of the Management API service:

```bash
gravitee_email_host=smtp.my.domain
gravitee_email_port=465
gravitee_email_from=noreply@my.domain
gravitee_email_subject=[Gravitee.io] %s
gravitee_email_username=user@my.domain
gravitee_email_password=password
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the top-level `smtp:` section of your `values.yaml`. The APIM Helm chart renders the `smtp:` values into the Management API `gravitee.yml` `email:` block at install time:

```yaml
smtp:
  enabled: true
  host: smtp.my.domain
  port: 465
  from: noreply@my.domain
  subject: "[Gravitee.io] %s"
  username: user@my.domain
  password: password
```
{% endtab %}
{% endtabs %}

## Configure in APIM Console

{% hint style="info" %}
If you change the SMTP settings using the `gravitee.yml` or environment variables, then the SMTP settings will be greyed out in the APIM console.
{% endhint %}

You can also configure SMTP at the organization level in the **Organization > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-20 at 3.27.18 PM.png" alt=""><figcaption><p>Organization SMTP settings</p></figcaption></figure>

Or at the environment level in the **Settings > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-20 at 3.30.01 PM.png" alt=""><figcaption><p>Environment SMTP settings</p></figcaption></figure>

## Configure the Gmail SMTP server

Configure the Gmail SMTP server using the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
Update the `email:` section of the Management API `gravitee.yml` file:

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
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by `docker-compose.yml`, or to the `environment:` block of the Management API service:

```bash
gravitee_email_enabled=true
gravitee_email_host=smtp.gmail.com
gravitee_email_port=587
gravitee_email_from=user@gmail.com
gravitee_email_subject=[Gravitee.io] %s
gravitee_email_username=user@gmail.com
gravitee_email_password=xxxxxxxx
gravitee_email_properties_auth=true
gravitee_email_properties_starttls_enable=true
gravitee_email_properties_ssl_trust=smtp.gmail.com
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the top-level `smtp:` section of your `values.yaml`:

```yaml
smtp:
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
{% endtab %}
{% endtabs %}

If you are using 2-Factor Authentication (which is recommended), you need to [generate an application password](https://security.google.com/settings/security/apppasswords).
