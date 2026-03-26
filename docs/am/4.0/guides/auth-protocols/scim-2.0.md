---
description: Overview of Protocol.
---

# SCIM 2.0

[The System for Cross-domain Identity Management (SCIM)](https://datatracker.ietf.org/doc/html/rfc7644) 2.0 is a standard for automating the exchange of user identity information between identity domains, or IT systems.

Since it is a standard, SCIM ensures interoperability and user data consistency that can be communicated across similar applications. SCIM enables to automate the provisioning/de-provisioning process and manage users and groups.

SCIM protocol endpoints are exposed by the [AM API](https://raw.githubusercontent.com/gravitee-io/gravitee-docs/master/am/current/scim/swagger.yml).

## Protocol

SCIM is a standard that defines schema and protocols for identity management.

It relies on REST APIs with endpoints exposing CRUD (Create, Read, Update, Delete) functionality for users and groups as well as search, discovery, and bulk features.

## Custom attributes

Gravitee AM supports a custom SCIM (system for cross-domain identity management) `User` extension that enables you to define extended attributes for your users.

{% hint style="info" %}
Custom attributes are stored in the `additionalInformation` map of the user.
{% endhint %}

The custom `User` extension is identified using the following schema URI: `urn:ietf:params:scim:schemas:extension:custom:2.0:User`

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
