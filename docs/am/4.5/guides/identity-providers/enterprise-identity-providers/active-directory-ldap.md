# Active Directory/LDAP

## Overview

You can authenticate and manage users in AM using Enterprise Active Directory or LDAP server.

## Create an Active Directory / LDAP identity provider

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **HTTP** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings.
7. Click **Create**.

You can also create the identity provider with [AM API.](../../../reference/am-api-reference.md)

{% code overflow="wrap" %}
```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{
           "type": "ldap-am-idp",
           "name": "LDAP IdP",
           "configuration": "{\"contextSourceUrl\":\"ldap://myserver.example.com:389\",\"contextSourceBase\":\"baseDN\",\"contextSourceUsername\":\"username\",\"contextSourcePassword\":\"password\",\"userSearchFilter\":\"uid={0}\",\"userSearchBase\":\"ou=users\",\"groupSearchBase\":\"ou=applications\",\"groupSearchFilter\":\"(uniqueMember={0})\",\"groupRoleAttribute\":\"cn\"}"
         }' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId/identities
```
{% endcode %}

## Test the connection

You can test your Active Directory/LDAP connection via your web applications created in AM.

1.  In AM Console, click **Applications** and select your Active Directory/LDAP identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Application IdP</p></figcaption></figure>
2.  Call the Login page (i.e. `/oauth/authorize` endpoint) and try to sign in with the username/password form.

    If you are unable to authenticate your user, there may be a problem with the identity provider settings. Check the AM Gateway log and audit logs for more information.
