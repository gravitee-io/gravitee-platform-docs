---
description: Configure general API Management 4.12 Management API settings in the gravitee.yaml file. Browse the configuration guides you need.
metaLinks:
  alternates:
    - ./
---

# Management API

## Overview

You can configure your general Gravitee APIM Management API settings using the `gravitee.yaml` file. As detailed in [APIM Components](README.md), you can override these settings by using system properties or environment variables.

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

## Default `gravitee.yaml` config file

The following is a reference of the default configuration of APIM Management API in your `gravitee.yml` file:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-distribution/gravitee-apim-distribution-standalone/gravitee-apim-distribution-standalone-rest-api/src/main/resources/config/gravitee.yml" %}

## Identity provider tokens in the browser

From APIM 4.12.22, four settings decide whether the identity provider's access token and ID token reach the browser when a user signs in through an identity provider. The `console` settings apply to the APIM Console and the Gamma console, and the `portal` settings apply to the Developer Portal (classic and new). All four default to `true`, so both tokens reach the browser. Set one to `false` to hide that token.

The settings apply to the whole installation. You can't set them per organization or environment, or from the APIM Console. For what hiding each token changes, see [Keep identity provider tokens out of the browser](../manage-organizations-and-environments/authentication/README.md#keep-identity-provider-tokens-out-of-the-browser).

In `gravitee.yml`, set the following keys:

```yaml
console:
  authentication:
    expose:
      accessToken: true
      idToken: true
portal:
  authentication:
    expose:
      accessToken: true
      idToken: true
```

With Helm, set the following values in `values.yaml`:

```yaml
api:
  authentication:
    console:
      exposeAccessToken: true
      exposeIdToken: true
    portal:
      exposeAccessToken: true
      exposeIdToken: true
```

{% hint style="warning" %}
**Known limitation in APIM 4.12:** setting `console.authentication.expose.idToken` to `false` stops users from signing in to the APIM Console and the Gamma console through a provider whose **Scopes** include `openid`. Keep it `true` while users sign in through such a provider.
{% endhint %}
