# Creating and Managing Subscription Forms

Subscription forms allow administrators to collect structured metadata from API consumers during the subscription process. Forms are defined using Gravitee Markdown (GMD) tags and can include input fields, text areas, and validation rules.

### Accessing the subscription form editor

Navigate to [Portal Settings > Subscription Form](../../configure-and-manage-the-platform/manage-organizations-and-environments/developer-portal.md) in the Management Console. The menu item requires `environment-metadata-r` or `environment-metadata-u` permissions.

### Creating a subscription form

1. In the GMD form editor, define input fields using GMD tags. For example:
   ```markdown
   <gmd-input name="consumer_company_name" label="Company Name" required="true"/>
   <gmd-textarea name="consumer_use_case" label="Use Case" required="true"/>
   ```
2. Click **Save** to persist the form content. The save button is disabled when content is empty, unchanged, or contains configuration errors.
3. Toggle the **Enable** switch to make the form visible to API consumers in the Portal.

The form is automatically created for the environment on first save and updated on subsequent saves.

### Managing form state

The form editor validates content in real-time and displays configuration errors:

| Error Type | Severity | Description |
|:-----------|:---------|:------------|
| `emptyFieldKey` | error | Field name is missing or empty |
| `normalizedValue` | warning | Field value requires normalization |

The **Enable** toggle is disabled when:
- The user lacks `environment-metadata-u` permission
- Configuration errors are present

An unsaved changes guard prevents accidental navigation away from the editor. The browser prompts for confirmation if you attempt to leave with unsaved changes.

### Consumer subscription flow

When a consumer subscribes to an API with an enabled subscription form:

1. The form appears as step 4 (Checkout) in the subscription wizard, replacing the legacy "Add a comment" card.
2. The consumer fills out the required and optional fields defined in the GMD content.
3. The **Next** button is disabled until all required fields are valid.
4. On submission, form values are filtered to remove empty or whitespace-only entries, then attached to the subscription as metadata.

{% hint style="info" %}
If the plan security type is `KEY_LESS`, the form is skipped entirely regardless of configuration.
{% endhint %}

### Viewing subscription metadata

Subscription metadata appears in the Management Console:

- **No metadata**: Displays a dash (`-`)
- **Metadata present**: Displays a read-only Monaco editor with JSON content and a clipboard copy button

## Subscription entity schema

The `Subscription` entity includes a `metadata` field:

| Field | Type | Description |
|:------|:-----|:------------|
| `metadata` | `Record<string, string>` | Key-value pairs from subscription form submission |

Metadata is included in subscription creation when:
1. Subscription form exists and has `gmdContent`
2. Plan security is not `KEY_LESS`
3. Metadata object has at least one non-empty key-value pair after filtering
