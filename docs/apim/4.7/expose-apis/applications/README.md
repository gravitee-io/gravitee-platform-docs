---
description: An overview about applications.
---

# Applications

## Overview

To access Gravitee APIs, consumers must register an application and subscribe to a published API plan. Applications act on behalf of the user to request tokens, provide user identity information, and retrieve protected resources from remote services and APIs.

The sections below describe how to use the APIM Console to create an application.

{% hint style="info" %}
Before a consumer can create an application, an admin must define the types of applications that API consumers are allowed to create. Refer to [this](./) documentation for more information.
{% endhint %}

## Create an application

1. Log in to your APIM Console
2. Select **Applications** from the left nav
3.  Click **+ Add Application**

    <figure><img src="../../.gitbook/assets/1 app 1 (1).png" alt=""><figcaption></figcaption></figure>
4. Enter a name for your application and give it a description. These fields require values.
5. Enter a domain for your application.
6.  Select an application type:

    **Simple**

    * Enter a value for the type.
    * Enter the client ID. This is required to subscribe to certain API plans (OAuth2, JWT).
    * Enter the client certificate for PEM. This is required to subscribe to certain mTLS plans.

    **SPA**

    * (Required) Select the allowed grant types you require for security. Available selections are **Authorization Code** and **Implicit**.
    * (Required) Enter the URIs to which the authorization server will send OAuth responses.
    * Enter additional client metadata as key-value pairs.
    * Enter the client certificate for PEM. This is required to subscribe to certain mTLS plans.

    **Web**

    * (Required) Select the allowed grant types you require for security. **Authorization Code** is mandatory. **Refresh Token** and **Implicit (Hybrid)** are optional.
    * (Required) Enter the URIs to which the authorization server will send OAuth responses.
    * Enter additional client metadata as key-value pairs.
    * Enter the client certificate for PEM. This is required to subscribe to certain mTLS plans.

    **Native**

    * (Required) Select the allowed grant types you require for security. **Authorization Code** is mandatory. **Refresh Token**, **Resource Owner Password**, and **Implicit (Hybrid)** are optional.
    * (Required) Enter the URIs to which the authorization server will send OAuth responses.
    * Enter additional client metadata as key-value pairs.
    * Enter the client certificate for PEM. This is required to subscribe to certain mTLS plans.

    **Backend to backend**

    * (Required) Select the allowed grant types you require for security. **Client Credentials** is required and the only option.
    * Enter additional client metadata as key-value pairs.
    * Enter the client certificate for PEM. This is required to subscribe to certain mTLS plans.
7. Click **Create**.

Once you've created your application, the inner left nav separates the application management and configuration into several categories:

<figure><img src="../../.gitbook/assets/1 app 2 1 (1).png" alt=""><figcaption></figcaption></figure>

The screen for each category selection includes a row of headers from which you can manage your application and its parameters. Click on the cards below to learn more about each configuration category.

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><a href="global-settings.md">Global settings</a></td><td></td><td></td></tr><tr><td><a href="user-and-group-access.md">User and group access</a></td><td></td><td></td></tr><tr><td><a href="metadata.md">Metadata</a></td><td></td><td></td></tr><tr><td><a href="../subscriptions.md">Subscriptions</a></td><td></td><td></td></tr><tr><td><a href="notifications.md">Notifications</a></td><td></td><td></td></tr></tbody></table>
