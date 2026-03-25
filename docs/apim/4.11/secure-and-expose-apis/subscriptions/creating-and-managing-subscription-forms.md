# Creating and managing subscription forms

## Prerequisites

Before creating or managing subscription forms, ensure you have the following:

* `environment-metadata-r` permission to view subscription forms in the Console
* `environment-metadata-u` permission to create, update, enable, or disable subscription forms
* Portal authentication to retrieve subscription forms via Portal API
* One of the following database backends: JDBC (PostgreSQL, MySQL, SQL Server) or MongoDB

## Creating subscription forms

1. Navigate to **Portal Settings > Subscription Form** in the Management Console.
2. Write form content using the GMD form editor. Include a `fieldKey` attribute on each component to map the field value to a metadata key. For example: `<gmd-input name="company" label="Company Name" fieldKey="company_name" required="true"/>`.
3. Review the live preview pane, which displays the rendered form in real time.
4. Click **Save** to persist changes. The **Save** button is disabled when content is empty, invalid, or unchanged.
5. Toggle the **Visible to API consumers** switch to control whether the form appears in the Developer Portal.

An unsaved changes guard prevents accidental navigation away from unsaved edits. Forms are scoped to the environment level — each environment has one subscription form stored with a unique `environment_id` constraint. GMD content must not be null, empty, or whitespace-only — violations throw `GraviteeMarkdownContentEmptyException`.

{% hint style="info" %}
Tooltips display "Fix configuration errors before continuing." when validation fails or "You do not have permission to change this." when the user lacks `environment-metadata-u` permission.
{% endhint %}

{% hint style="info" %}
Subscription forms aren't displayed for Keyless plans. The form only appears during the subscription checkout flow when the selected plan requires authentication (API Key, OAuth2, JWT, or mTLS).
{% endhint %}

{% hint style="info" %}
Plan comment fields are deprecated and labeled "Classic Portal only" in the Console.
{% endhint %}

## GMD form components

Use the following GMD components to build subscription forms:

- **`gmd-input`** — Single-line text input. Supports `minLength`, `maxLength`, and `pattern` validation.
- **`gmd-textarea`** — Multi-line text input. Supports `minLength`, `maxLength`, and configurable `rows`.
- **`gmd-select`** — Dropdown selection. Define choices with the `options` attribute.
- **`gmd-checkbox`** — Checkbox field.
- **`gmd-radio`** — Radio button selection. Define choices with the `options` attribute.

All components support `fieldKey`, `name`, `label`, `value`, `required`, and `disabled` attributes. The `fieldKey` attribute determines the metadata key stored with the subscription.

{% hint style="info" %}
`minLength` and `maxLength` validation is only available on `gmd-input` and `gmd-textarea`. Dropdown, checkbox, and radio components don't support length validation.
{% endhint %}

For a complete attribute reference, see [Subscription form feature overview](subscription-form-feature-overview.md#supported-form-components).

## Managing subscription forms

### Updating form content

1. Edit the GMD content in the form editor.
2. Click **Save** to persist changes.

### Enabling or disabling forms

Toggle the **Visible to API consumers** switch in the Console, or call the following Management API endpoints:

* `POST /environments/{envId}/subscription-forms/{subscriptionFormId}/_enable`
* `POST /environments/{envId}/subscription-forms/{subscriptionFormId}/_disable`

When a form is disabled, it remains accessible via Management API (`GET /environments/{envId}/subscription-forms`) but returns 404 from Portal API (`GET /subscription-form`). The Console displays disabled forms to users with `environment-metadata-r` permission.

Enabling a form displays the success message "Subscription form has been enabled successfully." Disabling a form displays "Subscription form has been disabled successfully."

### Subscription metadata

When an API consumer submits a subscription form, the form field values are stored as key-value pairs in the subscription's `metadata` property. Empty values (null, empty strings, whitespace-only) are filtered before storage. Metadata keys are validated — no spaces or special characters are allowed. Invalid metadata keys return a `400 Bad Request` error with the message "Invalid metadata key."

Form state is managed by the GMD form store. Field values are extracted and sent as `metadata` in the subscription request.

Subscription metadata is displayed in the subscription details pages (both API subscriptions and application subscriptions) using a read-only viewer.

## Subscribe to API checkout

The Portal checkout step displays the subscription form when the plan security type is not `KEY_LESS` and a form exists and is enabled. The Subscribe button is disabled if the form is invalid.

## Management API v2 reference

### GET `/environments/{envId}/subscription-forms`

Retrieves the subscription form for the environment, including disabled forms.

**Permissions:** `environment-metadata-r` or `environment-metadata-u`

**Response:**

* `200 OK` with `SubscriptionForm` object containing `id`, `gmdContent`, and `enabled` fields
* `404 Not Found` if the form does not exist

**Example response:**

```json
{
  "id": "string",
  "gmdContent": "string",
  "enabled": true
}
```

### PUT `/environments/{envId}/subscription-forms/{subscriptionFormId}`

Updates the subscription form GMD content.

**Permissions:** `environment-metadata-u`

**Request body:**

```json
{
  "gmdContent": "string"
}
```

**Response:**

* `200 OK` with updated `SubscriptionForm` object
* `400 Bad Request` if GMD content is null, empty, or whitespace-only
* `404 Not Found` if the form does not exist

### POST `/environments/{envId}/subscription-forms/{subscriptionFormId}/_enable`

Enables the subscription form for API consumers.

**Permissions:** `environment-metadata-u`

**Response:** `200 OK` with updated `SubscriptionForm` object (`enabled: true`)

**Success message:** "Subscription form has been enabled successfully."

### POST `/environments/{envId}/subscription-forms/{subscriptionFormId}/_disable`

Disables the subscription form for API consumers.

**Permissions:** `environment-metadata-u`

**Response:** `200 OK` with updated `SubscriptionForm` object (`enabled: false`)

**Success message:** "Subscription form has been disabled successfully."

## Portal API reference

### GET `/subscription-form`

Retrieves the enabled subscription form for the current environment. Only returns the form when it exists and is enabled — returns 404 otherwise. The Portal API response doesn't include the `id` or `enabled` fields.

**Authentication:** Required (Portal auth)

**Response:**

* `200 OK` with `SubscriptionForm` object containing only `gmdContent` if the form exists and `enabled` is `true`
* `404 Not Found` if the form does not exist or is disabled

**Example response:**

```json
{
  "gmdContent": "# Subscription Information\n<gmd-input name=\"company\" label=\"Company Name\" required=\"true\"/>"
}
```

### POST `/subscriptions`

Creates a subscription with optional metadata from the form.

**Request body:**

```json
{
  "application": "app-id",
  "plan": "plan-id",
  "metadata": {
    "company": "Acme Corp",
    "use_case": "Internal API integration"
  }
}
```

**Behavior:**

* Metadata is extracted from GMD form field values
* Empty or whitespace-only metadata values are filtered out before submission
* Metadata keys are validated (no spaces or special characters allowed)

**Response:**

* `400 Bad Request` with error message "Invalid metadata key." if validation fails
