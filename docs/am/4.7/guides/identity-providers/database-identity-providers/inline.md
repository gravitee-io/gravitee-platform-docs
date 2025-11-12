# Inline

## Overview

Inline identity providers are based on in-memory user directories. They are useful for testing purposes or setting default accounts.

## Create an inline identity provider

To create an identity provider:

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **Inline** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings.
7. Click **Create**.

{% hint style="info" %}
If you want to register multiple users, click the **Add user** button before clicking on the **Create** button.
{% endhint %}

You can also create the identity provider with [AM API](docs/am/4.7/reference/am-api-reference.md).

{% code overflow="wrap" %}
```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{
           "type": "inline-am-idp",
           "name": "Inline IdP",
           "configuration": "{\"users\":[{\"firstname\":\"johndoe\",\"lastname\":\"John\",\"username\":\"Doe\",\"password\":\"johndoepassword\"}]}"
         }' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId/identities
```
{% endcode %}

You can choose how passwords are encoded or hashed with the following algorithms:

* `bcrypt`
* none (plain text)

{% hint style="warning" %}
If you decide to switch from `bcrypt` to none, you must update all password fields before saving.
{% endhint %}

## Test the connection

You can test your database connection using a web application created in AM.

1.  In AM Console, click **Applications** and select your inline identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select Inline IdP</p></figcaption></figure>
2.  Call the Login page (i.e `/oauth/authorize` endpoint) and try to sign in with the username/password form.

    If you are unable to authenticate your user, there may be a problem with the identity provider settings. Check the AM Gateway log and audit logs for more information.
