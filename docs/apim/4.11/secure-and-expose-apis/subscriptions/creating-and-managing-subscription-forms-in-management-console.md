# Creating and Managing Subscription Forms in Management Console

## Creating a Subscription Form

Navigate to **Portal Settings** → **Subscription Form** in the Management Console.

1. Write GMD form content in the editor using `<gmd-input>`, `<gmd-textarea>`, and other GMD components.
2. Review the live preview to verify field rendering.
3. Click **Save** to persist the form. This action requires the `environment-metadata-u` permission.
4. Toggle the enable switch to make the form visible to API consumers in the Portal.

The **Save** button is disabled when:
- Content is empty
- Content is unchanged from the saved state
- Configuration errors exist

The enable toggle is disabled when:
- Configuration errors exist
- The user lacks the `environment-metadata-u` permission

## Managing Subscription Forms

### Editing Form Content

1. Navigate to **Portal Settings** → **Subscription Form**.
2. Modify the GMD content in the editor.
3. Click **Save** to persist updates.

The **Save** button activates when changes are detected and content is valid. A browser warning appears if you navigate away with unsaved changes. The form version displayed to consumers updates immediately after save.

### Enabling and Disabling Forms

Use the enable toggle in the subscription form editor to control visibility.

- **When enabled**: The form appears during subscription checkout for all plans except `KEY_LESS` security types.
- **When disabled**: The form is hidden and metadata is not collected. The Portal API returns 404 for disabled forms.

The Management API returns the form regardless of enabled status.

## End-User Configuration

### Management API v2

#### GET `/environments/{envId}/subscription-forms`

Returns the subscription form for the environment. Returns the form regardless of `enabled` status.

**Response**: `SubscriptionForm`

```json
{
  "id": "string",
  "gmdContent": "string",
  "enabled": boolean
}
```

#### PUT `/environments/{envId}/subscription-forms/{formId}`

Updates the GMD content of the subscription form. Content must not be null, empty, or whitespace-only.

**Request**: `UpdateSubscriptionForm`

```json
{
  "gmdContent": "string"
}
```

**Response**: `SubscriptionForm`

#### POST `/environments/{envId}/subscription-forms/{formId}/_enable`

Enables the subscription form, making it visible to API consumers in the Portal.

**Response**: `SubscriptionForm` with `enabled: true`

#### POST `/environments/{envId}/subscription-forms/{formId}/_disable`

Disables the subscription form, hiding it from API consumers in the Portal.

**Response**: `SubscriptionForm` with `enabled: false`

### Portal API

#### GET `/subscription-form`

Returns the subscription form content when the form exists and is enabled. Returns 404 when no subscription form exists for the environment or when the form is disabled.

**Response** (200):

```json
{
  "gmdContent": "string"
}
```

**Example GMD Content**:

```markdown
# Subscription Information

<gmd-input name="consumer_company_name" label="Company Name" required="true"/>
<gmd-textarea name="consumer_use_case" label="Use Case" required="true"/>
```

**Error Responses**:
- `404`: Subscription form not found or disabled for the environment
- `500`: Internal server error
