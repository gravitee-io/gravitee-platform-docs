---
hidden: false
noIndex: false
---

# Edit your schema

Modify an existing schema to add entity types, attributes, relationships, or actions.

{% hint style="warning" %}
This feature is under active development and may not be available in all environments at this time.
<!-- GAP: Schema editing UI exists in SchemaPage.tsx (Edit button, Monaco editor, Save/Cancel, validation diagnostics), but the schema DSL syntax and advanced editing workflows need SME confirmation for documentation completeness. -->
{% endhint %}

## Editing workflow

1. Navigate to **Policy Structure → Schema**
2. On the **Code** tab, click **Edit**
3. The Monaco editor switches from read-only to editable mode
4. Make your changes to the GAPL schema
5. The editor validates your changes in real time — any errors appear in an alert below the toolbar
6. Click **Save** to publish the updated schema, or **Cancel** to discard changes

## Validation during editing

While editing, the console sends the draft schema to the backend's validation endpoint. Diagnostics are displayed in a destructive alert: "Schema could not be fully parsed" with a bulleted list of errors.

If the validation endpoint is unreachable, the console shows: "Validation unavailable — could not reach the schema validator, so this draft has not been checked. The server validates again on save."

## Permissions

| Action | Required permission |
|--------|-------------------|
| **Edit** | `ENVIRONMENT_AUTHZ_SCHEMA[UPDATE]` |
| **Delete** | `ENVIRONMENT_AUTHZ_SCHEMA[DELETE]` |

## Deleting a schema

Click **Delete** on the Schema page toolbar. This removes the published schema. Entity creation dialogs revert to using the default type presets.

## Next steps

* [Validate schema changes](validate-schema-changes.md) — Understand validation rules
* [Schema generation](schema-generation.md) — Schema structure reference
