# SAML Assertion Attribute Mapping Concepts

## Overview

SAML Assertion Attribute Mapping enables administrators to customize the NameID and assertion attributes emitted in SAML responses using Expression Language (EL) expressions. Instead of the fixed default attribute set, applications can map SAML attributes to user profile fields, additional information, or computed values.

## Key Concepts

### NameID Mapping

The NameID element in a SAML response identifies the authenticated user to the service provider. By default, the internal user ID is used. The **NameID Mapping** field accepts an EL expression that resolves to a custom identifier (e.g., `{#context.attributes['user'].username}`).

**NameID format precedence:**

| Condition | NameID Value |
|:----------|:-------------|
| SP requests `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` format | User's email address (ignores **NameID Mapping** configuration) |
| **NameID Mapping** is configured and evaluates successfully | Result of EL expression evaluation |
| **NameID Mapping** evaluation fails or returns null/empty | User's internal ID |
| **NameID Mapping** is null/empty | User's internal ID (default) |

**Supported NameID formats:**

The SAML 2.0 IdP protocol plugin currently documents support for `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`. All other NameID formats use the **NameID Mapping** expression or the default internal user ID.

### Assertion Attributes

Assertion attributes are name-value pairs embedded in the SAML response that convey user profile information to the service provider. When no custom mappings are configured, the default attribute set is emitted:

| Attribute Name | Source |
|:---------------|:-------|
| `sub` | User ID |
| `preferred_username` | Username |
| `email` | Email address |
| `given_name` | First name |
| `family_name` | Last name |
| `name` | Display name |

Custom assertion attributes replace the default set entirely. Each mapping consists of an **Attribute Name** (the SAML attribute name) and a **Value** (an EL expression). If an expression resolves to null or fails, the attribute is omitted from the response.

Omitting assertion attribute mappings causes the default attribute set to be returned (backward compatible with AM 4.11).

### Expression Language Context

EL expressions are evaluated against an execution context containing the authenticated user object and additional request attributes. Common expressions include:

* `{#context.attributes['user'].email}` — User's email address
* `{#context.attributes['user'].username}` — Username
* `{#context.attributes['user'].additionalInformation['dept']}` — Custom user field (e.g., department)

For additional EL examples, see [Expression Language](../expression-language.md).


## Creating SAML Assertion Mappings

To configure custom SAML assertion mappings:

1. Log in to AM Console.
2. Select your security domain.
3. Click **Applications**.
4. Select the application to configure.
5. Click **Settings**.
6. Click **SAML 2.0**.
7. Locate the **Assertion Mapping** section.
8. (Optional) Enter an EL expression in the **NameID Mapping** field to customize the NameID value (e.g., `{#context.attributes['user'].username}`). Leave empty to use the default internal user ID.
9. To add custom assertion attributes:
   1. Enter an **Attribute Name** (e.g., `custom_email`).
   2. Enter a **Value** EL expression (e.g., `{#context.attributes['user'].email}`).
   3. Click **ADD**.
10. Repeat step 9 for each attribute mapping.
11. To remove an attribute, click the delete button in the attribute table.
12. Click **SAVE**.

When no custom attributes are configured, the hint text confirms that the default attribute set will be emitted. Custom attributes replace the default set entirely.

{% hint style="info" %}
Additional configuration examples and troubleshooting guidance will be added in a future release.
{% endhint %}
