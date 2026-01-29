# SCIM 2.0

[The System for Cross-domain Identity Management (SCIM)](https://datatracker.ietf.org/doc/html/rfc7644) 2.0 is a standard for automating the exchange of user identity information between identity domains, or IT systems.

Since it is a standard, SCIM ensures interoperability and user data consistency that can be communicated across similar applications. SCIM enables to automate the provisioning/de-provisioning process and manage users and groups.

SCIM protocol endpoints are exposed by the AM Gateway following the [OpenAPI specification](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/4.6.x/docs/scim-api-descriptor.yml).

## Protocol Overview

SCIM defines schemas and protocols for identity management.\
It relies on REST APIs that provide the following capabilities:\
&#x9;•	CRUD operations for Users and Groups\
&#x9;•	Search and filtering capabilities\
&#x9;•	Bulk APIs (with limitations)

{% hint style="warning" %}
Bulk operations for Groups are not currently supported.
{% endhint %}

## Custom attributes

Gravitee Access Management supports a custom **System for Cross-Domain Identity Management (SCIM)** User extension, enabling you to define additional user attributes beyond the standard SCIM specification.

The extension is identified by the following schema URI:

```
urn:ietf:params:scim:schemas:extension:custom:2.0:User
```

You can send **any** attributes inside this extension. However, Gravitee Access Management gives **special behavior** only to a specific subset of attributes as described in the following table. All other attributes are simply stored as-is in `additionalInformation` and can be used, for example, in templates or policies.

### Attributes With Special Behaviour

<table><thead><tr><th width="181.421875">Attribute</th><th width="116.84765625">Type</th><th>Effect on user</th><th>Validation / Notes</th></tr></thead><tbody><tr><td><strong>lastPasswordReset</strong></td><td>String (ISO-8601)</td><td>Sets the user’s <code>lastPasswordReset</code> date, which is used by password expiry policies. This is useful when migrating from an alternative OIDC provider.</td><td>Only evaluated during user creation. Must be a valid ISO-8601 timestamp, and The timestamp cannot be in the future. If parsing fails or the value is in the future, the request is rejected. Example date: <code>2025-12-11T21:37:00Z</code></td></tr><tr><td><strong>preRegistration</strong></td><td>Boolean</td><td>When <code>true</code>, marks the user as pre-registered and clears the password so the user receives an email to set their password.</td><td>Must be a boolean. If the value is not a boolean, the request is rejected. After processing, this field is removed from <code>additionalInformation</code>.</td></tr><tr><td><strong>forceResetPassword</strong></td><td>Boolean</td><td>When <code>true</code>, sets <code>forceResetPassword</code> on the user so they must change their password after their next successful login.</td><td>Must be a boolean. If the value is not a boolean, the request is rejected. After processing, this field is removed from <code>additionalInformation</code>.</td></tr><tr><td><strong>client</strong></td><td>String (client ID or client UID)</td><td>Assigns the user to a specific OAuth client during creation by setting the user’s <code>client</code> property. When used with <code>preRegistration: true</code>, it also controls which email template is used for the registration email.</td><td>Must be a string. If the value is not a string, the request is rejected. After processing, this field is removed from <code>additionalInformation</code>.</td></tr></tbody></table>

### Other Custom Attributes

Any other attributes are handled by Gravitee Access Management in the following ways:

* **not interpreted** by Gravitee Access Management logic
* stored as-is in `user.additionalInformation`.

You can still use these custom attributes in templates andpolicies. But they do not trigger any built-in behavior. &#x20;

### Example

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
      "customClaim2": "customValue2",
      "client": "client-id",
      "preRegistration": true
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
