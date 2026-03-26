---
description: Configuration guide for Manage users.
---

# Users

## Manage users

### List users

1. Log in to AM Console.
2.  Search for users by clicking **Settings > Users** and entering the username in the search field.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-search-users.png" alt=""><figcaption><p>Search for users</p></figcaption></figure>

You can also list users with the AM API `/users` endpoint.

{% hint style="info" %}
You can only list users created with AM API or the SCIM protocol and external users who have already logged in.
{% endhint %}

#### **List Users with a query (q)**

Finds users who match the specified query (standard search mode).

The value of `q` is matched against `username`, `email`, `displayName`, `firstName` or `lastName`.

{% hint style="info" %}
In AM Console, you do not need to specify the `q` parameter, only the query value (for example `john doe`).
{% endhint %}

The list operation performs a `startsWith` match query; you do not need to specify `firstName`, `lastName` or `email` attribute name.

**Request example**

{% code overflow="wrap" %}
```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X GET \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/:domain/gravitee/users?q=gravitee*&page=0&size=25
```
{% endcode %}

**Response example**

```json
{
   "data":[
      {
         "id":"c5c22ed3-6a43-44c3-822e-d36a4324c3db",
         "externalId":"5cf3527b-3aac-497a-b352-7b3aacf97a04",
         "username":"gravitee.user@mail.com",
         "email":"gravitee.user@mail.com",
         "displayName":"Gravitee User",
         "firstName":"Gravitee",
         "lastName":"User",
         "accountNonExpired":true,
         "accountNonLocked":true,
         "credentialsNonExpired":true,
         "enabled":true,
         "internal":true,
         "preRegistration":false,
         "registrationCompleted":true,
         "referenceType":"domain",
         "referenceId":"gravitee",
         "source":"Default Identity Provider",
         "loginsCount":0,
         "webAuthnRegistrationCompleted":false,
         "additionalInformation":{

         },
         "createdAt":1603037060752,
         "updatedAt":1603037060752
      }
   ],
   "currentPage":0,
   "totalCount":1
}
```

#### **List users with a filter (filter)**

Lists all users that match the filter criteria (advanced search mode).

When searching for users, you can create queries using [SCIM 2.0 query syntax](https://tools.ietf.org/html/rfc7644#section-3.4.2.2) to refine your search. The search query must contain at least one valid expression with an attribute name followed by an attribute operator and an optional value.

{% hint style="info" %}
In AM Console, you do not need to specify the `filter` parameter, only the query value (for example `displayName eq "john doe"`).
{% endhint %}

Multiple expressions may be combined using the logical operators (`and` / `or`). Operators `[`, `]` and `not` are not supported.

By default only the `id`, `externalId`, `username`, `email`, `displayName`, `firstName` and `lastName` fields are indexed in the database. This operation also supports searching the `additionalInformation` attributes of your users, but you need to create the correct indexes first. If you are using RDBMS backends, please refer to the underlying section `Add new filter fields for RDBMS backends` for more details.

The following operators are supported :

| Operator | Description              | Behavior                                                                                                                                                                                                                                                                       |
| -------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| eq       | equal                    | The attribute and operator values must be identical for a match.                                                                                                                                                                                                               |
| ne       | not equal                | The attribute and operator values are not identical.                                                                                                                                                                                                                           |
| co       | contains                 | The entire operator value must be a substring of the attribute value for a match.                                                                                                                                                                                              |
| sw       | starts with              | The entire operator value must be a substring of the attribute value, starting at the beginning of the attribute value. This criterion is satisfied if the two strings are identical.                                                                                          |
| ew       | ends with                | The entire operator value must be a substring of the attribute value, matching at the end of the attribute value. This criterion is satisfied if the two strings are identical.                                                                                                |
| pr       | present                  | If the attribute has a non-empty or non-null value, or if it contains a non-empty node for complex attributes, there is a match.                                                                                                                                               |
| gt       | greater than             | If the attribute value is greater than the operator value, there is a match. The actual comparison is dependent on the attribute type. For string attribute types, this is a lexicographical comparison, and for DateTime types, it is a chronological comparison.             |
| ge       | greater than or equal to | If the attribute value is greater than or equal to the operator value, there is a match. The actual comparison is dependent on the attribute type. For string attribute types, this is a lexicographical comparison, and for DateTime types, it is a chronological comparison. |
| lt       | less than                | If the attribute value is less than the operator value, there is a match. The actual comparison is dependent on the attribute type. For string attribute types, this is a lexicographical comparison, and for DateTime types, it is a chronological comparison.                |
| le       | less than or equal to    | If the attribute value is less than or equal to the operator value, there is a match. The actual comparison is dependent on the attribute type. For string attribute types, this is a lexicographical comparison, and for DateTime types, it is a chronological comparison.    |

The following examples give guidance on how to use this feature. All the attribute names are based on the user model provided by [AM API.](../../reference/am-api-reference.md)

```
List disabled users
-> enabled eq false

List users updated after 06/01/2019 but before 01/01/2020
-> updatedAt gt "2019-06-01T00:00:00.000Z" and updatedAt lt "2020-01-01T00:00:00.000Z"

List users by first name
-> firstName co "john"
```

#### **Add new filter field for RDBMS backends**

When you are using an RDBMS backend, you will have to execute additional SQL statements to allow searching on `additionalInformation` fields that are not managed by default by AM.

For PostgreSQL, as `additionalInformation` is a JSON field you may have to create additional indexes.

{% code overflow="wrap" %}
```sql
CREATE INDEX idx_users_additional_info_custom ON users USING BTREE (reference_id, reference_type, ((additional_information->>'custom_field')))
```
{% endcode %}

For MySQL, MariaDB, and SQLServer, you will have to create a new column with the value coming from the user `additionalInformation` and create an index.

**MySQL**

{% code overflow="wrap" %}
```sql
ALTER TABLE users ADD additional_information_custom VARCHAR(320) AS (JSON_UNQUOTE(additional_information->"$.custom"));
CREATE INDEX idx_users_additional_information_custom ON users(reference_id, reference_type, additional_information_custom);
```
{% endcode %}

**MariaDB**

{% code overflow="wrap" %}
```sql
ALTER TABLE users ADD additional_information_custom VARCHAR(320) AS (JSON_VALUE(additional_information, "$.custom_field"));
CREATE INDEX idx_users_additional_information_custom ON users(reference_id, reference_type, additional_information_custom);
```
{% endcode %}

**SQLServer**

{% code overflow="wrap" %}
```sql
ALTER TABLE users ADD additional_information_custom AS JSON_VALUE(additional_information, '$.custom_field');
CREATE INDEX idx_users_additional_information_custom ON users(reference_id, reference_type, additional_information_custom);
```
{% endcode %}

### Create a new user

You create users in a security domain.

1. Log in to AM Console.
2. Click **Settings > Users**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Give your user a **First name**, a **Last name**, an **Email** and a **Username** and click **SAVE**.
5. (Optional) You can also add/modify specific attributes relating to the user. This user metadata will be available in the user’s profile.
6.  You will be redirected to the created user’s page.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-create-user.png" alt=""><figcaption><p>New user creation page</p></figcaption></figure>

{% hint style="info" %}
You can choose to enable `Pre-Registration`, to allow users to finish registering their own account. An email will be sent to the user with instructions.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-pre-registration-mail.png" alt=""><figcaption><p>New user registration email</p></figcaption></figure>

### Update the username

You can update the username of your user. Updating the username is only available via the console and the management-api.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-user-update-usename.png" alt=""><figcaption><p>Update username</p></figcaption></figure>

1. Log in to AM Console.
2. Click **Settings > Users**
3. Select your user
4. Input the new username
5. Click on the **Update Username** button

{% hint style="warning" %}
Updating the username will automatically update it in the user’s identity provider that support direct update of the user: HTTP Provider, JDBC, MongoDB and Inline. Other IDPs are not supported.
{% endhint %}

### User roles

You can assign roles directly from the user profile, or from the identity provider role mapping feature.

{% hint style="info" %}
If you are using both user roles and the identity provider role mapper feature, the two roles will be in two different places, you can see the different roles in **Settings > Users > "Your User" > Roles**.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-user-assigned-dynamic-roles.png" alt=""><figcaption><p>User roles overview</p></figcaption></figure>

By default, users are stored in the pre-defined `Default Identity Provider`, which is available by default for each security domain. You can apply role mapping to your users.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-user-role-mapping.png" alt=""><figcaption><p>Default IdP</p></figcaption></figure>
