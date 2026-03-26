---
description: Overview of JDBC.
---

# JDBC

## Overview

You can authenticate users in AM with the most common databases, including:

* PostgreSQL
* MySQL
* Microsoft SQL Server
* MariaDB

You do this by creating a new Java Database Connectivity (JDBC) identity provider.

{% hint style="info" %}
Before you begin, you need to ensure that your database has the appropriate fields to store user profile attributes, such as `id`, `username`, `email`, `password` and `metadata`.
{% endhint %}

## Create a SQL database identity provider

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **JDBC** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the database settings as required.
7. Click **Create**.

## Test the connection

You can test your database connection using a web application created in AM.

1.  In AM Console, click **Applications** and select your JDBC identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select JDBC IdP</p></figcaption></figure>
2.  Call the Login page (i.e `/oauth/authorize` endpoint) and try to sign in with the username/password form.

    If you are unable to authenticate your user, there may be a problem with the identity provider settings. Check the AM Gateway log and audit logs for more information.
