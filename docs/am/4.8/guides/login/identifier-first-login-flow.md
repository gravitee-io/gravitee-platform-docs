---
description: Identifier-first login splits Access Management 4.8 sign-in into two steps, username then credential. Follow the steps to activate it.
---

# Identifier-first Login Flow

## Overview

Identifier-first login authentication enables the login flow to be split into two steps:

* The first step consists in a page containing a single form field where you can input your username

<figure><img src="../../.gitbook/assets/graviteeio-am-userguide-login-identifier-first-first-page-flow.png" alt="The first step of the identifier-first login flow, asking only for a username, with links to register or to sign in with a fingerprint, device, or security key."><figcaption><p>Split login first step</p></figcaption></figure>

* Regarding the input submitted, the user gets redirected to the login form and is asked to input your password
* If the username is an email, the user gets redirected to an external provider matching your domain based on a whitelist

<figure><img src="../../.gitbook/assets/graviteeio-am-userguide-login-identifier-first-second-page-flow.png" alt="The second step of the identifier-first login flow, with the username carried over and a password field, above a Back to login link."><figcaption><p>Split login second step</p></figcaption></figure>

## Activate Identifier-first Login

To activate Identifier-first login Flow:

1. Log in to AM Console.
2. Go to **Settings > Login** or **Application > "Your app" > Settings > Login**.
3. Switch on **Identifier-first login** and click **SAVE**.

<figure><img src="../../.gitbook/assets/graviteeio-am-userguide-login-identifier-first-settings.png" alt="The application Login settings with Identifier-first login switched on and the Hide login form option disabled."><figcaption><p>Enable identifier-first login</p></figcaption></figure>

## Identity providers allowed domain list

External Identity providers now enable you to enter domain whitelists so that if the username submitted is an email and its domain does not match the whitelisted domains after a login attempt, they won’t be allowed to login.

If you don’t input any domain however, everyone will be able to login.

1. Go to **Settings > Providers**.
2. Create a new provider or Edit an existing one
3. Enter the domains you wish to allow
4. Complete the provider’s form and click **SAVE**.

<figure><img src="../../.gitbook/assets/graviteeio-am-userguide-login-identifier-first-identity-provider-domain-whitelist.png" alt="The Settings step of the New provider wizard with a domain whitelist entry that triggers identifier-first redirection, above empty client ID and secret fields."><figcaption><p>Add provider to domain list</p></figcaption></figure>
