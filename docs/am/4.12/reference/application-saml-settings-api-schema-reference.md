
# Application SAML Settings API Schema Reference

The `ApplicationSAMLSettings` schema includes the following properties:


| Property | Type | Required | Description |
|:---------|:----:|:--------:|:------------|
| **Name Id Mapping** | String | No | EL expression resolved to produce the NameID value in the SAML response. When null or empty, the default behavior applies: the internal user ID is used, or the user's email when the service provider requests EMAIL format. |
| **Assertion Attributes** | Array of `SAMLAssertionAttribute` | No | Custom SAML assertion attribute mappings. When non-empty, replaces the default fixed attribute set. |
| `entityId` | String | No | Existing SAML setting. |
| `certificate` | String | No | Existing SAML setting. |
| `responseBinding` | String | No | Existing SAML setting. |
| `singleLogoutServiceUrl` | String | No | Existing SAML setting. |
| `attributeConsumeServiceUrl` | String | No | Existing SAML setting. |

### SAMLAssertionAttribute Schema

The `SAMLAssertionAttribute` schema defines custom attribute mappings:

| Property | Type | Required | Description |
|:---------|:-----|:---------|:------------|
| `name` | String | Yes | SAML attribute name emitted in the `<Attribute Name="...">` element. |
| `value` | String | Yes | EL expression whose resolved string value becomes the attribute value. |

### Examples

**Name Id Mapping:**

```
{#context.attributes['user'].username}
```

**Assertion Attributes:**

```json
[
 {
 "name": "email",
 "value": "{#context.attributes['user'].email}"
 }
]
```

### OpenAPI Schema

The OpenAPI schema for `ApplicationSAMLSettings` and `PatchApplicationSAMLSettings` includes the `nameIdMapping` and `assertionAttributes` properties. The `SAMLAssertionAttribute` schema is defined as a separate component with required `name` and `value` fields.

## Restrictions

- When NameID Mapping or Assertion Attributes EL expressions fail to evaluate, the failure is logged as a warning and the system falls back to default behavior (user ID for NameID, attribute skipped for assertion attributes). The error is not surfaced to the end user or service provider.
- The EMAIL NameID format always uses the user's email address, ignoring any NameID Mapping configuration.
- Custom assertion attributes completely replace the default set; there is no merge behavior. Administrators must explicitly list all desired attributes.
- EL expressions are evaluated at response generation time; invalid expressions are detected only at runtime, not at configuration time.
- The UI does not validate EL expression syntax; administrators must ensure expressions are well-formed.
