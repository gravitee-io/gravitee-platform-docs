---
description: Overview of Group Mapping.
---

# User, Role and Group Mapping

## Overview

You can bind some identity provider attributes to an AM _user profile_ with attribute mapping. Using this method, AM clients can receive additional attributes through your identity provider.

{% hint style="info" %}
We advise you to read [get user profile information](../../getting-started/tutorial-getting-started-with-am/get-user-profile-information.md) first.
{% endhint %}

User profile attributes can be retrieved either by calling the **UserInfo** endpoint or, if you specify an `openid` scope for your application, by parsing the claims in the `id_token`.

## User mappers

In the identity provider **User mappers** tab, you can add mappings between user attributes to be returned by the identity provider, with custom attributes that will be stored within the _User Profile_.

With an LDAP identity provider, if you don’t define any mappings, the following attributes are returned by default:

| LDAP attribute                       | OIDC attribute      |
| ------------------------------------ | ------------------- |
| displayname                          | name                |
| givenname                            | given\_name         |
| sn                                   | family\_name        |
| mail                                 | email               |
| the username typed in the login form | preferred\_username |

The user name is also the attribute used to look up the user in LDAP, as defined per the default pattern: `uid={0}`

{% hint style="info" %}
Once you start using the **User Mapper** feature, the default claims listed above will no longer appear in the user profile. Instead, only the declared mappings will apply.\
The same applies when the client starts using scopes other than `openid`.
{% endhint %}

### Example

Let’s imagine a client application wants to retrieve the `telephoneNumber` attribute present in the LDAP identity provider. You can do this by configuring the identity provider as follows:

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Select your LDAP identity provider and click the **User mappers** tab.
4.  Map your LDAP (raw) attribute `telephoneNumber` to a new user attribute named `telephone_number`.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-idp-user-mappers-phoneno.png" alt=""><figcaption><p>LDAP user mappers</p></figcaption></figure>
5. Get the User Profile information via the UserInfo Endpoint and you will see that the new user attribute is present.

{% code overflow="wrap" %}
````
```sh
curl -X GET http://GRAVITEEIO-AM-GATEWAY-HOST/:securityDomainPath/oidc/userinfo -H 'Authorization: Bearer :accessToken'
```
````
{% endcode %}

````
If it is working correctly, you will see something like this:

```sh
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
{
    "uid": "johndoe",
    "given_name": "John",
    "family_name": "Doe"
    "telephone_number: "202-555-0105"
}
```
````

The same principle applies to any identity provider.

### OIDC scopes and claims

According to the [OpenID Connect core specification](https://openid.net/specs/openid-connect-core-1_0.html#ScopeClaims), using scopes such as `profile`, `phone`, `email` or `address` will retrieve sets of specific claims.\
For example, using the `profile` scope will return the following claims, if available: `name`, `family_name`, `given_name`, `middle_name`, `nickname`, `preferred_username`, `profile`, `picture`, `website`, `gender`, `birthdate`, `zoneinfo`, `locale`, and `updated_at`.\
You can see their [definitions here](https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims).

## Role mapper and dynamic OAuth2 scopes

AM allows you to create roles and permissions for your users. You can map these roles to your identity provider user attributes or groups.

Defining roles in AM helps you to centralize AM for all clients in a given _domain_.

In addition, when it comes to fine-grained authorization management, it is considered good practice to use OAuth _scopes_.

The goal is to dynamically add scopes to the `access_token`, depending on the role associated with the user when authenticating.

{% hint style="info" %} When the roles are updated via SCIM, the roles already applied via Role Mappers won’t be persisted as an assigned role. This ensures that it can be safely removed when the mapper rule does not match anymore. For more about SCIM, click [here](../auth-protocols/scim-2.0.md). {% endhint %}

### Example

In the following example, we will map a role named `administrator` to users who are members of the `IT_DEVELOPERS_TEAM` LDAP group.\
We will then dynamically add the `admin` scope to the `access_token`. The client will provide this scope when accessing an API via an API Manager, and the API Manager will check for the scope before granting access to the upstream API.

1. Log in to AM Console.
2. Click **Settings > Scopes**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) and create an `admin` scope.
4. Click **Settings > Roles**.
5. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) and create an `administrator` role. Select the `admin` scope permission.
6. Go to the `Providers` section
7. Click **Settings > Providers** and select your LDAP identity provider.
8. Click the **Role mappers** tab.
9.  Set the user’s role configuration:

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-idp-role-mappers.png" alt=""><figcaption><p>LDAP role mapper</p></figcaption></figure>
10. When the client requests the _Token_ endpoint, the new scope representing the user roles will be used.
11. Ensure you enable the _"Enhance scopes"_ option for your client (**OAuth** tab).

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-user-guide-mapping-idp-enhance-scopes.png" alt=""><figcaption><p>Enhance scopes</p></figcaption></figure>

The same principle applies to all identity providers.

## Group mapper

AM allows you to create groups for your users. You can map these groups to your identity provider user attributes.

Defining groups in AM helps you to assign roles more efficiently for the domain users.

The goal of the Group Mapper is to dynamically add groups to the user profile based on the user information when authenticating.

<figure><img src="../../.gitbook/assets/image (2)-1.png" alt=""><figcaption><p>Assign ADMIN group to all user profile with memberOf equals administrators</p></figcaption></figure>
