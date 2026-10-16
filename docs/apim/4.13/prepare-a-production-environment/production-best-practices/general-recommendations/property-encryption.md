---
description: API Management 4.13 can store encrypted property values on an API. Learn how property encryption works and how to set it up.
metaLinks:
  alternates:
    - property-encryption.md
---

# Property Encryption

Gravitee allows attaching properties to an API and offers the capability to store encrypted property values. **You must change the default encryption secret** with a custom secret that can't be determined easily. You must consider the following when changing the secret:

* The secret must be **changed for both Management and Gateway** and have the same value.
* The secret must be **32 bytes in length**.
* The secret should ideally be generated with a password generation tool to enforce robustness.
* If you have several installations (e.g., one for dev, one for prod), make sure to **set up different secrets for each installation**.

```yaml
api:
  properties:
    encryption:
         secret: <32 byte length secret>
```

The same secret encrypts the values of encrypted dictionary properties. For more information, see [Dictionaries](../../../configure-and-manage-the-platform/gravitee-gateway/dictionaries.md#encrypt-dictionary-properties).

Encrypted dynamic API properties use the same secret. If the secret can't encrypt a value, for example because its length isn't valid, saving an encrypted property of a v4 API fails, and APIM doesn't store the value in plain text. When a fetch of dynamic properties can't encrypt a value, APIM keeps the stored value, or leaves out a new property, and logs an error. For more information, see [Encrypt dynamic properties](../../../create-and-configure-apis/apply-policies/v4-api-policy-studio.md#encrypt-dynamic-properties).

You can find additional details about property encryption in [Properties](../../../create-and-configure-apis/apply-policies/v4-api-policy-studio.md#api-properties).
