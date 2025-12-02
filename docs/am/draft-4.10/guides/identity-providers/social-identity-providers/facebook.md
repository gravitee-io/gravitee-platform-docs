# Facebook

## Overview

You can authenticate users with Facebook. Before you begin, you need to sign up for a [Facebook Developer account](https://www.facebook.com/r.php?next=https%3A%2F%2Fdevelopers.facebook.com%2F\&locale=en_US\&display=page).

## Steps

To connect your application to Facebook, you will:

* Register a new application in Facebook
* Create a Facebook identity provider in AM
* Set up the connection in Facebook
* Test the connection

## Register a new application in Facebook

1. [Add a New App](https://developers.facebook.com/apps/) from the Facebook for Developers Portal.
2. For **How are you using your app?**, select **For everything else**.
3. Give your application a name.
4. Click **Create**.

{% hint style="info" %}
Facebook will generate an App ID and App Secret for your application. Make a note of these for later use.
{% endhint %}

## Create a Facebook identity provider

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Choose the Facebook identity provider type and click **Next**.

{% hint style="info" %}
Ensure you have the generated App ID and App Secret from Facebook the application to hand.
{% endhint %}

5. Give your identity provider a name.
6. Enter your Facebook application App ID and App Secret.
7.  Click **Create**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-facebook.png" alt=""><figcaption><p>Create Facebook IdP</p></figcaption></figure>

{% hint style="info" %}
On the right side of the screen under **1. Configure the Redirect URI**, copy the value of the URL. You will use it to update your Facebook application settings.
{% endhint %}

{% hint style="info" %}
HTTP client settings apply whether or not HTTP/2 is enabled, but they may affect different request characteristics. In particular, the `HTTP Client max pool size` setting limits the number of concurrent connections, but allows a higher number of concurrent requests with multiplexed HTTP/2 connections. See also [Configure HTTP clients](../../../getting-started/configuration/configure-am-gateway/README.md#configure-http-clients).
{% endhint %}

## Set up the connection

Go to your Facebook application settings and add **Facebook Login** to the application as a Product.

Configure the following settings:

1. Enable **Client OAuth Login**.
2. Enable **Web OAuth Login**
3. Add a **Valid OAuth Redirect URIs** with the Redirect URI created in the previous step.
4. Click **Save Changes**.

## Test the connection

You can test your Facebook connection using a web application created in AM.

1.  i.e.In AM Console, click **Applications** and select your social identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select Facebook IdP</p></figcaption></figure>
2.  Call the Login Page (i.e. `/oauth/authorize` endpoint). If the connection is working you will see a **Sign in with …​** button.

    If the button is not visible, there may be a problem with the identity provider settings. Check the AM Gateway log for more information.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-login.png" alt=""><figcaption><p>Sign in Options</p></figcaption></figure>
