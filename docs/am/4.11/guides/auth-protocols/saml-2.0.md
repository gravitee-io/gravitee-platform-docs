---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/guides/auth-protocols/saml-2.0
---

# SAML 2.0

## Overview

[The Security Assertion Markup Language (SAML)](http://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html) standard defines an XML-based framework for describing and exchanging security information between online business partners.

Gravitee Access Management (AM) supports the SAML protocol and can serve both as Identity Provider (IdP) and Service Provider (SP) :

* [Configure AM as SAML Identity Provider](saml-2.0.md#enable-saml-2.0-identity-provider-support)
* [Configure AM as SAML Service Provider](../identity-providers/enterprise-identity-providers/saml-2.0.md)

## Participants

At a minimum, SAML exchanges take place between system entities referred to as a SAML asserting party and a SAML relying party. In many SAML use cases, a user, perhaps running a web browser or executing a SAML-enabled application, is also a participant, and may even be the asserting party.

**Service provider (SP)**

A relying party that uses assertions it has received from the Identity Provider (IdP) to grant the principal access to local resources.

**Identity provider (IdP)**

An entity that authenticates users and provides to service providers (SP) an authentication assertion that indicates a principal has been authenticated.

<figure><img src="../../.gitbook/assets/graviteeio-am-devguide-protocols-saml-overview.png" alt=""><figcaption><p>SAML diagram</p></figcaption></figure>

## Enable SAML 2.0 Identity Provider support

AM supports the following SAML bindings :

* HTTP-Redirect
* HTTP-POST

AM also supports the following options:

* Web Browser SSO Profile
* Single Logout Profile
* SP-Initiated flow
* Support for signed SAML assertions (SAML Request and SAML Response)

{% hint style="info" %}
Support for encrypted SAML assertions will be provided in a future version of the SAML 2.0 IdP protocol plugin.
{% endhint %}

### Install the SAML 2.0 IdP protocol plugin

The SAML 2.0 IdP protocol plugin (`gravitee-am-gateway-handler-saml2-idp`) is a Gravitee Enterprise feature. A valid Enterprise Edition license key is required to activate it. The plugin must be installed on both the AM Gateway and AM Management API.

{% hint style="warning" %}
The SAML 2.0 IdP protocol plugin isn't available in the Community Edition of AM. Contact your Gravitee account representative to obtain an Enterprise license key.
{% endhint %}

### **Self-hosted installation (ZIP)**

The SAML 2.0 IdP protocol plugin is included in the default AM Enterprise Edition distribution and doesn't require a separate download.

1. Verify the plugin ZIP file exists in the AM Gateway plugins directory at `${gravitee.home}/plugins/`. Look for a file named `gravitee-am-gateway-handler-saml2-idp-<version>.zip`.
2. Verify the same plugin ZIP file exists in the AM Management API plugins directory at `${gravitee.home}/plugins/`.
3. Place your `license.key` file in the `${gravitee.home}/license/` directory of both the AM Gateway and AM Management API installations.
4. Restart both the AM Gateway and AM Management API.

{% hint style="info" %}
The default plugins directory is `${gravitee.home}/plugins`. To customize it, update the `plugins.path` property in `gravitee.yml`.
{% endhint %}

#### **Docker installation**

The AM Docker images don't include Enterprise plugins by default. Download the SAML 2.0 IdP protocol plugin from the [Gravitee Enterprise download portal](https://download.gravitee.io/#graviteeio-ee/am/plugins/gateway/handlers/gravitee-am-gateway-handler-saml2-idp/) and mount it alongside the license key.

For the AM Gateway:

```sh
docker run  \
        --publish 8092:8092  \
        --name am-gateway  \
        --env GRAVITEE_MANAGEMENT_MONGODB_URI=mongodb://username:password@mongohost:27017/dbname \
        --env GRAVITEE_PLUGINS_PATH_0=/opt/graviteeio-am-gateway/plugins \
        --env GRAVITEE_PLUGINS_PATH_1=/opt/graviteeio-am-gateway/plugins-ee \
        -v license.key:/opt/graviteeio-am-gateway/license \
        -v plugins-dir-ee:/opt/graviteeio-am-gateway/plugins-ee \
        --detach  \
        graviteeio/am-gateway:latest
```

For the AM Management API:

```sh
docker run  \
        --publish 8093:8093  \
        --name am-management-api \
        --env GRAVITEE_MANAGEMENT_MONGODB_URI=mongodb://username:password@mongohost:27017/dbname \
        --env GRAVITEE_PLUGINS_PATH_0=/opt/graviteeio-am-management-api/plugins \
        --env GRAVITEE_PLUGINS_PATH_1=/opt/graviteeio-am-management-api/plugins-ee \
        -v license.key:/opt/graviteeio-am-management-api/license \
        -v plugins-dir-ee:/opt/graviteeio-am-management-api/plugins-ee \
        --detach  \
        graviteeio/am-management-api:latest
```

Place the `gravitee-am-gateway-handler-saml2-idp-<version>.zip` file in the local `plugins-dir-ee` directory before starting the containers.

For more information on Docker EE configuration, see [Docker images install.](../../getting-started/install-and-upgrade-guides/run-in-docker/docker-images-install.md)

#### **Kubernetes installation (Helm)**

Create a Kubernetes secret from your license key file:

```sh
kubectl create secret generic graviteeio-license --from-file=license.key
```

Then configure the Helm `values.yaml` to download the plugin and mount the license key for both the Gateway and Management API:

```yaml
gateway:
  additionalPlugins:
  - https://download.gravitee.io/graviteeio-ee/am/plugins/gateway/handlers/gravitee-am-gateway-handler-saml2-idp/gravitee-am-gateway-handler-saml2-idp-<version>.zip
  extraVolumeMounts: |
    - name: graviteeio-license
      mountPath: /opt/graviteeio-am-gateway/license
      readOnly: true
  extraVolumes: |
    - name: graviteeio-license
      secret:
        secretName: graviteeio-license

api:
  additionalPlugins:
  - https://download.gravitee.io/graviteeio-ee/am/plugins/gateway/handlers/gravitee-am-gateway-handler-saml2-idp/gravitee-am-gateway-handler-saml2-idp-<version>.zip
  extraVolumeMounts: |
    - name: graviteeio-license
      mountPath: /opt/graviteeio-am-management-api/license
      readOnly: true
  extraVolumes: |
    - name: graviteeio-license
      secret:
        secretName: graviteeio-license
```

For more information on Kubernetes installation, see Deploy in Kubernetes.

## Verify the plugin installation

After installing the plugin and the license key, verify the SAML 2.0 IdP protocol plugin is loaded:

1.  Check the AM Gateway startup logs for the following message:

    ```bash
    Protocol saml2-idp loaded
    ```

    If the plugin isn't installed or the license key is missing, this message doesn't appear in the logs.
2. Log in to AM Console.
3. Select your security domain.
4. Click **Settings**.
5. Click **SAML 2.0**.
6. Confirm the **SAML 2.0 IdP support** toggle is available without a lock icon. A lock icon indicates the license doesn't include this feature.

### Activate SAML 2.0 IdP

{% hint style="info" %}
Be sure to have your SAML 2.0 IdP protocol plugin and your license key installed in your environment before configuring the connection.
{% endhint %}

1. Log in to AM Console.
2. Select your security domain.
3. Click **Settings**.
4. Click **SAML 2.0**.
5. Enable the **SAML 2.0 IdP support** toggle.
6. Enter the IdP **Entity ID**.
7. Select a certificate to sign the SAML Response assertion.
8. Click **SAVE**.

{% hint style="info" %}
If you don't select a certificate, the SAML Response assertion won't be signed.
{% endhint %}

{% hint style="warning" %}
SAML can't currently be configured at the Organization level.
{% endhint %}

### Test the connection

To connect your applications to the AM SAML 2.0 IdP, you need at least the following information:

* **SingleSignOnService**, the SAML IdP Sign In URL : `https://AM_GATEWAY/{domain}/saml2/idp/SSO`
* **SingleLogoutService**, the SAML IdP Sign Out URL : `https://AM_GATEWAY/{domain}/saml2/idp/logout`
* **Signing certificate**, the public signing certificate (encoded in PEM)

{% hint style="info" %}
SAML IdP metadata information can be found here: `https://AM_GATEWAY/{domain}/saml2/idp/metadata`
{% endhint %}

Test the SAML 2.0 connection using a web application created in AM:

1. In AM Console, click **Settings**.
2. Click **SAML 2.0**.
3. Verify and update the SAML 2.0 application settings.
4. Select an identity provider to connect your users.
5. Call the Login page (the `/saml/idp/SSO?SAMLRequest=…` endpoint).
6. Enter the username and password, then click **Sign in**.
7. If the configuration is correct, the user is redirected to the application **attribute consume service URL** with the SAML Response assertion as a parameter.

{% hint style="info" %}
The SAML 2.0 IdP protocol is compatible out of the box with all existing AM features, such as passwordless, MFA, and social login, just like the OAuth 2.0/OpenID Connect protocol.
{% endhint %}
