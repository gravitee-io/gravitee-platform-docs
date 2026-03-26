---
description: Overview of Account Management.
---

# Self-service Account Management

## Overview

AM self-service account management allows users to manage their accounts with the following capabilities :

* Read and manage their account information.
* List user activities.
* Request to change passwords.
* Manage Multi-factor Authentication (MFA) devices.
* Manage Passwordless credentials.

{% hint style="info" %}
By default, these actions are possible only during the login process, but in order to provide a **My Account** space for your end-users, AM includes a REST API to perform all these requests.
{% endhint %}

To access the online API reference, go to [the API reference](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/4.5.x/docs/self-service-account-api-descriptor.yml).

## Configure the self-service account management

By default, the self-service account management is **disabled** for every security domain.

{% hint style="info" %}
Self-service account API is deployed at `http(s)://AM_GW_HOST/{domain}/account/api/**` and secured with OAuth 2.0 protocol.
{% endhint %}

To configure the self-service account settings :

1. Log in to AM Console.
2. Select your security domain and click **Settings > Self-service account**.
3. Configure your settings and click **SAVE**.
