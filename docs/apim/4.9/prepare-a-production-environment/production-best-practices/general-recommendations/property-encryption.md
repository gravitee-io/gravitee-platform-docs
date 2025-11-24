---
description: Documentation about property encryption in the context of APIs.
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

You can find additional details about property encryption in [Properties](../../../create-and-configure-apis/apply-policies/v4-api-policy-studio.md#api-properties).
