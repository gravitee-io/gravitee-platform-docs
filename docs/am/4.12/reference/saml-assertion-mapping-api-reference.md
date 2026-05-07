# SAML Assertion Mapping API Reference

## Managing Assertion Mappings via API

### Application SAML Settings API

Use the Management API to patch application SAML settings programmatically. The **Name Id Mapping** property accepts an EL expression string or null. The **Assertion Attributes** property accepts an array of objects with `name` and `value` properties, or null/empty array to reset to default behavior.

**PATCH Endpoint:**

```
PATCH /management/domains/{domainId}/applications/{appId}/settings/saml
```

**Request Body Schema:**

The request body follows the `PatchApplicationSAMLSettings` schema. The `nameIdMapping` and `assertionAttributes` properties are optional.

| Property | Type | Description |
|:---------|:-----|:------------|
| `nameIdMapping` | String (EL expression) or null | EL expression for the `<NameID>` value. Set to null to use the default internal user ID. |
| `assertionAttributes` | Array of `SAMLAssertionAttribute` or null/empty array | Custom SAML assertion attribute mappings. Set to null or empty array to use the default attribute set. |

**SAMLAssertionAttribute Object:**

| Property | Type | Required | Description |
|:---------|:-----|:---------|:------------|
| `name` | String | Yes | SAML attribute name emitted in the `<Attribute Name="...">` element |
| `value` | String (EL expression) | Yes | EL expression whose resolved string value becomes the attribute value |

**Example: Set custom NameID and attributes**

```json
PATCH /management/domains/{domainId}/applications/{appId}/settings/saml
{
  "nameIdMapping": "{#context.attributes['user'].username}",
  "assertionAttributes": [
    {
      "name": "custom_email",
      "value": "{#context.attributes['user'].email}"
    },
    {
      "name": "department",
      "value": "{#context.attributes['user'].additionalInformation['dept']}"
    }
  ]
}
```

**Example: Reset to default behavior**

```json
PATCH /management/domains/{domainId}/applications/{appId}/settings/saml
{
  "nameIdMapping": null,
  "assertionAttributes": []
}
```

## Restrictions

* EL expressions are validated only at runtime during SAML response generation; invalid expressions trigger fallback behavior and log warnings server-side
* When the service provider requests EMAIL format for NameID, the user's email is always used and the **NameID Mapping** configuration is ignored
* Custom assertion attributes whose EL expressions resolve to null or empty strings are silently omitted from the SAML response
* Expression evaluation failures are logged server-side but not surfaced to end users; administrators must monitor logs to detect misconfigured mappings
* The UI prevents duplicate attribute names, but the backend does not enforce uniqueness; duplicate names in the database result in multiple SAML `<Attribute>` elements with the same name
* Changes to application SAML settings may take up to 60 seconds to propagate to the gateway after API updates
* EL evaluation requires an execution context with a configured template engine; if unavailable, expressions cannot be evaluated and fallback behavior applies

## Related Changes

The application SAML settings form now includes an **Assertion Mapping** section with fields for **NameID Mapping** and a table for managing custom assertion attributes. The **ADD** button is disabled when attribute name or value is empty. A duplicate attribute name triggers a snackbar error message. The Management API schema for `ApplicationSAMLSettings` and `PatchApplicationSAMLSettings` now includes **Name Id Mapping** (string) and **Assertion Attributes** (array of `SAMLAssertionAttribute` objects). The `SAMLAssertionAttribute` schema requires `name` and `value` properties. MongoDB schema changes add **Name Id Mapping** and **Assertion Attributes** fields to the `ApplicationSAMLSettingsMongo` document; existing applications without these fields continue to use default behavior.
