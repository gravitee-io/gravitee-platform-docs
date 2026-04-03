# CAS

## Overview

The Central Authentication Service (CAS) protocol is a simple and powerful ticket-based protocol.

It involves one or many clients and one server. Clients are embedded in CASified applications (called "CAS services") and the CAS server is a standalone component:

* The CAS server is responsible for authenticating users and granting access to applications.
* The CAS clients protect the CAS applications and retrieve the identity of the granted users from the CAS server.

The key concepts are:

* **TGT (Ticket Granting Ticket)**: the TGT is stored in the TGC cookie and represents a SSO session for a user.
* **ST (Service Ticket)**: the ST is transmitted as a GET parameter in a URL. It stands for the access granted by the CAS server to the CASified application for a specific user.

CAS specifies a Browser Single-Signon sequence diagram involving a CAS server, an application (CAS Service), and a principal wielding an HTTP user agent (a browser) which is used by AM to create a bridge between your applications and a CAS Server.

{% hint style="info" %}
In this scenario, the AM CAS identity provider acts as a CAS service between your application and the CAS server.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-cas.png" alt=""><figcaption><p>AM CAS flow</p></figcaption></figure>

## Get your CAS Server metadata

To connect your applications to a CAS, you need at least the following information:

* **Login URL**: location of the CAS server login URL
* **Service Validate URL**: CAS service validate URL

{% hint style="info" %}
Before you begin, obtain this information from your CAS server administrator and make a note of it for later use.
{% endhint %}

## Create a CAS connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **CAS** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings (Login URL, Service Validate URL)
7. Click **Create**.

{% hint style="info" %}
Make a note of the URL in **1. Configure the Redirect URI** to the right of the page. This is the CAS service URL you need to provide to the CAS server to register your Access Management instance.
{% endhint %}

## Test the connection

You can test your CAS connection using a web application created in AM.

1.  In AM Console, click **Applications > App > Identity Providers** and select your CAS connector.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select CAS IdP</p></figcaption></figure>
2.  Call the Login page (the `/oauth/authorize` endpoint). If the connection is working you will see a **Sign in with CAS** button.

    If the button is not visible, there may be a problem with the identity provider settings. Check the AM Gateway log for more information.
3.  Click **Sign in with CAS**. You will be redirected to your CAS Server login page to authenticate your users.

    If your user is already connected (SSO session), the user will be automatically redirected to your application with an OAuth 2.0 access token and Open ID Connect ID token, if requested.
