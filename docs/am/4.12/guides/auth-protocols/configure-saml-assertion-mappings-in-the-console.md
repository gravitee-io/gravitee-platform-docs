# Configure SAML Assertion Mappings in the Console

## Creating SAML assertion mappings

Navigate to the Application SAML Settings form and locate the Assertion Mapping section.

To configure a custom NameID:

1. Enter an Expression Language (EL) expression in the **NameID Mapping** field (e.g., `{#context.attributes['user'].username}`).
2. Leave the field empty to use the default internal user ID.

To define custom assertion attributes:

1. In the Custom Attributes table, enter an **Attribute Name** (e.g., `email`).
2. Enter a **Value** EL expression (e.g., `{#context.attributes['user'].email}`).
3. Click **ADD**.

The attributes table displays all configured mappings with delete actions available in edit mode. If no custom attributes are configured, the system displays a hint indicating the default attribute set will be emitted.

## Managing Assertion Attributes

To add multiple custom attributes, repeat the attribute creation process for each required mapping.

The UI prevents duplicate attribute names. If a duplicate is detected, a snackbar error displays: `"Attribute name already exists"`.

To remove a custom attribute, click the delete button (close icon) in the Actions column of the attributes table.

{% hint style="warning" %}
Configuring any custom attributes replaces the entire default set. To retain default attributes alongside custom ones, explicitly configure all desired attributes in the Custom Attributes table.
{% endhint %}


