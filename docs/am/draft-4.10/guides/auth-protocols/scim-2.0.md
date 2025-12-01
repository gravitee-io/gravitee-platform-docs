# SCIM 2.0

[The System for Cross-domain Identity Management (SCIM)](https://datatracker.ietf.org/doc/html/rfc7644) 2.0 is a standard for automating the exchange of user identity information between identity domains, or IT systems.

Since it is a standard, SCIM ensures interoperability and user data consistency that can be communicated across similar applications. SCIM enables to automate the provisioning/de-provisioning process and manage users and groups.

SCIM protocol endpoints are exposed by the AM Gateway following the [OpenAPI specification](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/4.6.x/docs/scim-api-descriptor.yml).

## Protocol

SCIM is a standard that defines schema and protocols for identity management.

It relies on REST APIs with endpoints exposing CRUD (Create, Read, Update, Delete) functionality for users and groups as well as search, discovery, and bulk features.

{% hint style="warning" %}
Groups are currently not manageable using Bulk operations.
{% endhint %}

## Custom attributes

Gravitee AM supports a custom System for Cross-Domain Identity Management (SCIM) `User` extension. With this extension, you can define extended attributes for your users.

{% hint style="info" %}
Custom attributes are stored in the `additionalInformation` map of the user.
{% endhint %}

The custom `User` extension is identified using the following schema URI: `urn:ietf:params:scim:schemas:extension:custom:2.0:User`

{% hint style="info" %}
For users migrations from an alternative OIDC provider to Access Management, you can define the `lastPasswordReset` attribute. This attribute ensures that a password policy with password expiry requests a password reset according to the value provided during the migration. This attribute is accepted only during user creation.

In the SCIM request, the `lastPasswordReset` attribute is expected to be a String using ISO-8601 representation to be aligned with other date attributes defined by the SCIM specification.

As it is specific information,you must use the following Gravitee schema extension `"urn:ietf:params:scim:schemas:extension:custom:2.0:User"` . Here is an example:\
\
"urn:ietf:params:scim:schemas:extension:custom:2.0:User": {\
"lastPasswordReset": "2024-10-27T04:56:22Z"\
}

You can also define two boolean parameters: `preRegistration` and `forceResetPassword`.\
When `preRegistration` is set to `true`, the user receives an email prompting them to confirm their profile and set a password.\
When `forceResetPassword` is set to `true`, the user is required to reset their password following their next successful login.
{% endhint %}

The following non-normative example shows how to create, update, and patch users by using the custom `User` extension in JSON format.

{% code overflow="wrap" %}
```sh
Create user

curl -L -X POST 'https://AM_GATEWAY/{domain}/scim/Users'

{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User", "urn:ietf:params:scim:schemas:extension:custom:2.0:User"],
  "externalId": "701985",
  "userName": "barbara@example.com",
  "name": {
    "formatted": "Ms. Barbara J Jensen, III",
    "familyName": "Jensen",
    "givenName": "Barbara",
    "middleName": "Jane",
    "honorificPrefix": "Ms.",
    "honorificSuffix": "III"
  },
  "displayName": "Babs Jensen",
  "nickName": "Babs",
  "profileUrl": "https://login.example.com/bjensen",
  "emails": [
    {
      "value": "bjensen@example.com",
      "type": "work",
      "primary": true
    },
    {
      "value": "babs@jensen.org",
      "type": "home"
    }
  ],
  "addresses": [
    {
      "type": "work",
      "streetAddress": "100 Universal City Plaza",
      "locality": "Hollywood",
      "region": "CA",
      "postalCode": "91608",
      "country": "USA",
      "formatted": "100 Universal City Plaza\nHollywood, CA 91608 USA",
      "primary": true
    },
    {
      "type": "home",
      "streetAddress": "456 Hollywood Blvd",
      "locality": "Hollywood",
      "region": "CA",
      "postalCode": "91608",
      "country": "USA",
      "formatted": "456 Hollywood Blvd\nHollywood, CA 91608 USA"
    }
  ],
  "phoneNumbers": [
    {
      "value": "555-555-5555",
      "type": "work"
    },
    {
      "value": "555-555-4444",
      "type": "mobile"
    }
  ],
  "ims": [
    {
      "value": "someaimhandle",
      "type": "aim"
    }
  ],
  "photos": [
    {
      "value":
        "https://photos.example.com/profilephoto/72930000000Ccne/F",
      "type": "photo"
    },
    {
      "value":
        "https://photos.example.com/profilephoto/72930000000Ccne/T",
      "type": "thumbnail"
    }
  ],
  "userType": "Employee",
  "title": "Tour Guide",
  "preferredLanguage": "en-US",
  "locale": "en-US",
  "timezone": "America/Los_Angeles",
  "active":true,
  "x509Certificates": [
    {
      "value":
       "MIIDQzCCAqygAwIBAgICEAAwDQ....1UEBhMCVVMx"
    }
  ],
  "urn:ietf:params:scim:schemas:extension:custom:2.0:User": {
      "customClaim": "customValue",
      "customClaim2": "customValue2
  }
}
```
{% endcode %}

{% code overflow="wrap" %}
```sh
Update user

curl -L -X PUT 'https://AM_GATEWAY/{domain}/scim/Users/{userId}'

{
     "schemas":["urn:ietf:params:scim:schemas:core:2.0:User", "urn:ietf:params:scim:schemas:extension:custom:2.0:User"],
     "userName":"bjensen",
     "externalId":"bjensen",
     "name":{
       "formatted":"Ms. Barbara J Jensen III",
       "familyName":"Jensen2",
       "givenName":"Barbara"
     },
     "urn:ietf:params:scim:schemas:extension:custom:2.0:User": {
       "customClaim": "customValue",
       "customClaim2": "customValue2,
       "customClaim3": "customValue3"
     }
}
```
{% endcode %}

```sh
Patch user

curl -L -X PATCH 'https://AM_GATEWAY/{domain}/scim/Users/{userId}'

{
     "schemas":["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
     "Operations": [{
        "op":"Add",
        "path":"urn:ietf:params:scim:schemas:extension:custom:2.0:User",
        "value": {
            "customClaim4": "customValue4"
        }
     }]
}
```
