---
description: Overview of Kerberos.
---

# Kerberos

## Overview

Kerberos is a computer-network authentication protocol that works on the basis of _tickets_ to allow nodes communicating over a non-secure network to prove their identity to one another in a secure manner.

AM supports Kerberos authentication via the SPNEGO (Simple and Protected GSSAPI Negotiation Mechanism) protocol.

SPNEGO is used to authenticate users transparently through the web browser after they have been authenticated locally (in their Microsoft Windows or Kerberos session).

{% hint style="info" %}
Kerberos is widely used in Windows environments. It is also known as Integrated Windows Authentication (IWA).
{% endhint %}

## Get your Kerberos server metadata

To connect your applications to a Kerberos server, you need at least the following information:

* Realm: Kerberos realm used for connecting to the Kerberos server
* Keytab file: Path to the keytab file available on the AM server
* Principal: Name of the principal identified by the keytab

{% hint style="info" %}
You can also configure an LDAP server to fetch additional information on the current Kerberos principal (such as your application’s end-user).
{% endhint %}

## Create a Kerberos connector

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **Kerberos** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings (realm, keytab and principal).
7. Click **Create**.

## Test the connection

You can test your Kerberos connection using a web application created in AM.

1.  In AM Console, click **Applications** and select your Kerberos connector in the **Identity Providers** tab.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select Kerberos IdP</p></figcaption></figure>

{% hint style="info" %}
Once Kerberos is selected, the Kerberos connection will be established before displaying the login page, making it invisible to end users.
{% endhint %}

2. Call the Login page (i.e `/oauth/authorize` endpoint) and you will be automatically redirected to your application with either an `authorization_code` or an `access_token`. If you are unable to authenticate your user, there may be a problem with the identity provider settings. Check the AM Gateway log and audit logs for more information.
