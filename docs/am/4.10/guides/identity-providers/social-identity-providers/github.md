# Github

## Overview

You can authenticate users in AM with GitHub. Before you begin, you need to sign up for a [GitHub Developer account](https://github.com/join).

## Steps

To connect your application to GitHub, you will:

* Register a new application in GitHub
* Create a GitHub identity provider in Gravitee AM
* Set up the connection in GitHub
* Test the connection

## Register a new application in GitHub

1. [Register a new OAuth application](https://github.com/settings/applications/new) from **GitHub Developer Settings: OAuth Apps**.
2. Give your application a name.
3. For **Homepage URL** enter `https://AM_HOST/SECURITY_DOMAIN`.
4. For **Authorization callback URL** enter `https://AM_HOST/SECURITY_DOMAIN/login/callback`.

{% hint style="info" %}
The `Authorization callback URL` is a temporary value that will be updated when you [set up the connection.](github.md#set-up-the-connection)
{% endhint %}

5. Click **Register application**.

{% hint style="info" %}
GitHub will generate a Client ID and Client Secret for your application. Make a note of these for later use.
{% endhint %}

## Create a GitHub identity provider

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Choose the **GitHub** identity provider type and click **Next**.

{% hint style="info" %}
Ensure you have the GitHub application generated Client ID and Client Secret to hand.
{% endhint %}

5. Give your identity provider a name.
6. Enter your GitHub application Client ID and Client Secret.
7.  Click **Create**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-github.png" alt=""><figcaption><p>Create Github IdP</p></figcaption></figure>

{% hint style="info" %}
On the right side of the screen, under **1. Configure the Redirect URI** copy the value of the URL. You will use it to update your GitHub application settings.
{% endhint %}

{% hint style="info" %}
HTTP client settings apply whether or not HTTP/2 is enabled, but they may affect different request characteristics. In particular, the `HTTP Client max pool size` setting limits the number of concurrent connections, but allows a higher number of concurrent requests with multiplexed HTTP/2 connections. See also [Configure HTTP clients](../../../getting-started/configuration/configure-am-gateway/#configure-http-clients).
{% endhint %}

## Set up the connection

1. Go to your GitHub OAuth application settings.
2. Update the **Authorization callback URL** value with the Redirect URI created in the previous step.

## Test the connection

You can test your GitHub connection using a web application created in AM.

1.  In AM Console, click **Applications** and select your social identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select Github IdP</p></figcaption></figure>
2.  Call the Login Page (i.e the `/oauth/authorize` endpoint). If the connection is working you will see a **Sign in with …​** button.

    If the button is not visible, something may be wrong with the identity provider settings. Check the AM Gateway log for more information.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-login.png" alt=""><figcaption><p>Sign in options</p></figcaption></figure>
