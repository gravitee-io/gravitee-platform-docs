---
description: Overview of OpenID Connect.
---

# OpenID Connect

## Overview <a href="#overview" id="overview"></a>

You can authenticate users with any provider which implement the OpenID Connect specification.

## Steps <a href="#steps" id="steps"></a>

To connect your application to an OIDC provider, you will:

* Register a new application in you provider
* Create an OpenID identity provider in Gravitee AM
* Set up the connection in OIDC provider
* Test the connection

### Register a new application to the provider <a href="#register-a-new-application-to-the-provider" id="register-a-new-application-to-the-provider"></a>

This step is specific to the provider you are using. To be able to connect Access Management with your provider you will have to create a confidential application with one of the three authentication method:

* client\_secret\_basic
* client\_secret\_post
* mutual TLS

### Create an OpenID identity provider in Gravitee AM <a href="#create-an-openid-identity-provider-in-gravitee-am" id="create-an-openid-identity-provider-in-gravitee-am"></a>

1. Log in to AM Console.
2. Click the plus icon ![](https://documentation.gravitee.io/~gitbook/image?url=https%3A%2F%2Fdocumentation.gravitee.io%2F%7Egitbook%2Fimage%3Furl%3Dhttps%253A%252F%252Fdocs.gravitee.io%252Fimages%252Ficons%252Fplus-icon.png%26width%3D300%26dpr%3D4%26quality%3D100%26sign%3Dd153b85e%26sv%3D1\&width=300\&dpr=4\&quality=100\&sign=db6a087e\&sv=1).
3. Choose the **OpenID** identity provider type and click **Next**.

Ensure you have the generated Client ID and Client Secret from the provider application to hand.

1. Give your identity provider a name.
2. Enter the clientID and clientSecret of your application.
3. Select the authentication method you want to use as defined in you provider application. To be able to use tls\_client\_auth, you have to provide the [certificates](../../certificates/#certificate-for-mutual-tls-authentication) to Access Management and select this certificate into the dropdown list
4. Specify the provider endpoints to connect with. If the provider expose a discovery endpoint, you just have to specify the WellKnown endpoint, otherwise you will have to provide all the endpoints manually
5. Specify the flow you want to use and how the user profile will be retrieved. By default the profile is read using the user info endpoint but you can use the id\_token by enabling the option, if you do so you will have to specify the Public Key Resolver method.
6. provide the scopes to get information you need. To be able to get user information, you should at least provide the scope `openid`
7. Click **Create**.

#### **Public Key Resolver**

When the user information are extract from the id\_token, you have to specify a way to validate the token signature using a public key. For doing this, you have two options:

* provide the public key in PEM format (option GIVEN\_KEY)
* provide a JWKS\_URL and specify the endpoint to download the JWKS structure

{% hint style="info" %}
If you provide the WellKnown endpoint, you may not have to specify the JWKS\_URL as most of the time it is provided by the auto discovery endpoint.
{% endhint %}

### Set up the connection in OIDC provider <a href="#set-up-the-connection-in-oidc-provider" id="set-up-the-connection-in-oidc-provider"></a>

Go to your provider application settings and add the **Redirect URI** provided by the identity provider you configured into Gravitee Access Management in the right side panel.

### Test the connection <a href="#test-the-connection" id="test-the-connection"></a>

Once you are done with the configuration, you can enable the identity provider in your [domain application](../../applications.md#application-identity-providers) and try to authenticate a user.
