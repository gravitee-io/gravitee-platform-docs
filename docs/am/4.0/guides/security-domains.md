---
description: Overview of URLs.
---

# Security Domains

## Overview

A _security domain_ gives you access to all AM resources such as applications, users, and identity providers. It exposes authentication and authorization URLs and provides analytics and reporting.

The security domain acts as the container for your applications.

The first task of setting up new authorization and authentication in AM is to create a security domain for your applications. AM comes with a default security domain.

## Create a security domain with AM Console

1. Log in to AM Console.
2.  From the user menu at the top right, click **Create domain**.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-create-domain.png" alt=""><figcaption><p>Create a domain</p></figcaption></figure>
3. Give your security domain a **Name** and a **Description** and click **CREATE**.
4.  Select **click here** link on the banner to enable the domain.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-enable-domain.png" alt=""><figcaption><p>Domain banner</p></figcaption></figure>

## Create a security domain with AM API

{% code overflow="wrap" %}
```sh
# create domain
$ curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{"name":"My First Security Domain","description":"My First Security Domain description"}' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains

# enable domain
$ curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X PATCH \
     -d '{"enabled": true}' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId
```
{% endcode %}

## What do I do next?

Once you have created your security domain, you can configure it using the **Settings** menu (for example, configure security, users, or identity providers) and add applications to it using the **Applications** menu. See the following sections for more details.
