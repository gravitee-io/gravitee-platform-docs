---
description: An overview about create an application.
metaLinks:
  alternates:
    - create-an-application.md
---

# Create an Application

## Overview

This guide explains how to use the APIM Console to create an application.

{% hint style="info" %}
Before a consumer can create an application, an admin must define the types of applications that API consumers are allowed to create.
{% endhint %}

## Create an application

1. Log in to your APIM Console
2. Select **Applications** from the left nav
3.  Click **+ Add Application**

    <figure><img src="../../.gitbook/assets/00 groups added to applications (1).png" alt=""><figcaption></figcaption></figure>
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
