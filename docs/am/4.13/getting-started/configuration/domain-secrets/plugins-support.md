---
description: Configuration guide for plugin support.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/getting-started/configuration/domain-secrets/plugins-support
---

# Plugins support

## Plugins that support secrets

The following tables list the plugins that support secrets, the minimum required plugin version, and the fields that accept secret values.

### Certificates

The following table lists the certificate plugins that support secrets, the minimum version required, and the fields that accept secret values.

| Plugin          | Plugin version | Fields                                                    |
| --------------- | -------------- | --------------------------------------------------------- |
| Java Keystore   | 4.10.0 +       | <ul><li>Keystore password</li><li>Key password</li></ul>  |
| PKCS 12         | 4.10.0 +       | <ul><li>Keystore password</li><li>Key password</li></ul>  |
| AWS Certificate | 3.1.0 +        | <ul><li>Access key id</li><li>Secret access key</li></ul> |
| AWS CloudHSM    | 2.6.0 +        | <ul><li>Username</li><li>Password</li></ul>               |

### Bot detection

The following table lists the bot detection plugins that support secrets, the minimum version required, and the fields that accept secret values.

| Plugin              | Plugin version | Fields      |
| ------------------- | -------------- | ----------- |
| Google ReCaptcha V3 | 4.11.0 +       | `secretKey` |

### Identity provider

The following table lists the identity provider plugins that support secrets, the minimum version required, and the fields that accept secret values.

| Plugin             | Plugin version | Fields                                                                   |
| ------------------ | -------------- | ------------------------------------------------------------------------ |
| Facebook           | 4.11.0 +       | `clientSecret`                                                           |
| GitHub             | 4.11.0 +       | `clientSecret`                                                           |
| Google             | 4.11.0 +       | `clientSecret`                                                           |
| JDBC               | 4.11.0 +       | `password`                                                               |
| MongoDB            | 4.11.0 +       | <ul><li>`uri`</li><li>`password`</li><li>`Credential`</li></ul>          |
| LinkedIn           | 4.11.0 +       | `clientSecret`                                                           |
| Twitter            | 4.11.0 +       | `clientSecret`                                                           |
| Generic OAuth/OIDC | 4.11.0 +       | `clientSecret`                                                           |

### Reporter

The following table lists the reporter plugins that support secrets, the minimum version required, and the fields that accept secret values.

| Plugin | Plugin version | Fields     |
| ------ | -------------- | ---------- |
| Kafka  | 4.11.0 +       | `password` |

### Resource

The following table lists the resource plugins that support secrets, the minimum version required, and the fields that accept secret values.

| Plugin  | Plugin version | Fields                                                                                        |
| ------- | -------------- | --------------------------------------------------------------------------------------------- |
| Infobip | 4.11.0 +       | `apiKey`                                                                                      |
| SMTP    | 4.11.0 +       | <ul><li>`password`</li><li>`oauth2ClientSecret`</li><li>`oauth2RefreshToken`</li></ul>        |
