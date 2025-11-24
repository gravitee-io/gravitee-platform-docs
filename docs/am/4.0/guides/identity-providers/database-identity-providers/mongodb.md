---
description: Step‑by‑step tutorial for MongoDB.
---

# MongoDB

## Overview

You can authenticate users in AM using your own MongoDB database.

## Create a MongoDB identity provider

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **MongoDB** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings.
7. Click **Create**.

## Test the connection

You can test your database connection using a web application created in AM.

1.  In AM Console, click **Applications** and select your MongoDB identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select MongoDB IdP</p></figcaption></figure>
2.  Call the Login page (i.e `/oauth/authorize` endpoint) and try to sign in with the username/password form.

    If you are unable to authenticate your users, there may be a problem with the identity provider settings. Check the AM Gateway log and audit logs for more information.
