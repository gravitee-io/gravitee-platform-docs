# Creating and managing subscription forms

## Creating subscription forms

1. In the Management Console, click **Settings** in the left sidebar.

    <figure><img src="../../.gitbook/assets/pvdE8Owg__image.png" alt="Management Console dashboard with Settings highlighted"><figcaption><p>Click Settings in the left sidebar</p></figcaption></figure>

2. Scroll to the **New Developer Portal** section and click **Open Settings**.

    <figure><img src="../../.gitbook/assets/eB0pOpBE__image.png" alt="New Developer Portal section with Open Settings button"><figcaption><p>Click Open Settings in the New Developer Portal section</p></figcaption></figure>

3. In the portal settings sidebar, select **Subscription Form**.

    <figure><img src="../../.gitbook/assets/657dxh5i__Zrzut ekranu 2026-03-10 o 14.02.19.png" alt="Portal settings sidebar with Subscription Form highlighted"><figcaption><p>Select Subscription Form in the portal settings sidebar</p></figcaption></figure>

4. Write form content using the GMD form editor. The live preview pane displays the rendered form in real time.

    <figure><img src="../../.gitbook/assets/HnW9DAMW__Zrzut ekranu 2026-03-10 o 14.04.01.png" alt="GMD form editor with live preview"><figcaption><p>GMD form editor with live preview pane</p></figcaption></figure>

5. Toggle the **Visible to API consumers** switch to control whether the form appears in the Developer Portal.

    <figure><img src="../../.gitbook/assets/e768lrUA__Zrzut ekranu 2026-03-10 o 14.08.31.png" alt="Visible to API consumers toggle and Save button"><figcaption><p>Visible to API consumers toggle and Save button</p></figcaption></figure>

6. Click **Save** to persist changes.

An unsaved changes guard prevents accidental navigation away from unsaved edits. Forms are scoped to the environment level — each environment has one subscription form. The form editor enforces a 25-field maximum at save time and rejects forms that exceed this limit.

{% hint style="info" %}
Subscription forms aren't displayed for Keyless plans. The form only appears during the subscription checkout flow when the selected plan requires authentication (API Key, OAuth2, JWT, or mTLS).
{% endhint %}

The form editor validates GMD content in real time. Configuration errors, auto-corrected warnings, and field validation status appear in the validation panel below the editor. Saving is blocked when the editor reports critical errors, including:

- **Missing EL fallback** (`missingElFallback`) — EL expressions in `options` must include a fallback list after the `}:` separator.
- **Invalid EL syntax** (`invalidElSyntax`) — expressions in `options` must start with `{#`.

<figure><img src="../../.gitbook/assets/HsfV91lH__image.png" alt="Validation panel showing configuration errors and field status"><figcaption><p>Validation panel showing configuration errors, warnings, and field status</p></figcaption></figure>

## GMD form components

Use the following GMD components to build subscription forms:

- **`gmd-input`** — Single-line text input. Supports `minLength`, `maxLength`, and `pattern` validation.
- **`gmd-textarea`** — Multi-line text input. Supports `minLength`, `maxLength`, and configurable `rows`.
- **`gmd-select`** — Dropdown selection. Define choices with the `options` attribute.
- **`gmd-checkbox`** — Checkbox field.
- **`gmd-checkbox-group`** — Checkbox group field. Define choices with the `options` attribute using either a comma-separated list (for example, `"Authentication,Rate Limiting,Analytics"`) or an EL expression with a fallback list (for example, `"{#api.metadata['features']}:Authentication,Rate Limiting"`). Set `required="true"` to require at least one selection.
- **`gmd-radio`** — Radio button selection. Define choices with the `options` attribute.

All components support `fieldKey`, `name`, `label`, `value`, `required`, and `disabled` attributes. The `fieldKey` attribute determines the metadata key stored with the subscription.

{% hint style="info" %}
`minLength` and `maxLength` validation is only available on `gmd-input` and `gmd-textarea`. Dropdown, checkbox, checkbox group, and radio components don't support length validation.
{% endhint %}

For a complete attribute reference, see [Subscription form field attributes and validation constraints reference](subscription-form-field-attributes-and-validation-constraints-reference.md).

## Managing subscription forms

### Updating form content

1. Edit the GMD content in the form editor.
2. Click **Save** to persist changes.

### Enabling or disabling forms

Toggle the **Visible to API consumers** switch in the Console, or call the following Management API endpoints:

* `POST /environments/{envId}/subscription-forms/{subscriptionFormId}/_enable`
* `POST /environments/{envId}/subscription-forms/{subscriptionFormId}/_disable`

When a form is disabled, it remains accessible via Management API (`GET /environments/{envId}/subscription-forms`) but returns 404 from Portal API (`GET /subscription-form`).

### Subscription metadata

When an API consumer submits a subscription form, the form field values are stored as key-value pairs in the subscription's `metadata` property. Checkbox group selections are serialized as comma-separated strings (for example, `"Authentication,Analytics"`). Empty values (null, empty strings, whitespace-only) are filtered before storage.

Submissions are validated against the form's constraints before the subscription is created. Invalid submissions are rejected with field-level error messages.

Subscription metadata is displayed in the subscription details pages (both API subscriptions and application subscriptions) using a read-only viewer.

## Verification

To verify the subscription form is working as expected, follow these steps:

1. Enable the form using the **Visible to API consumers** toggle.
2. Click **Open Website** in the portal settings top bar to open the Developer Portal.

    <figure><img src="../../.gitbook/assets/yxZoykMa__Zrzut ekranu 2026-03-10 o 14.11.14.png" alt="Open Website button in the portal settings top bar"><figcaption><p>Click Open Website to preview the Developer Portal</p></figcaption></figure>

3. Navigate to an API and start a subscription. The custom form appears on the right side of the subscription checkout flow.

    <figure><img src="../../.gitbook/assets/Nsy6qPct__image.png" alt="Custom subscription form rendered in the Developer Portal checkout"><figcaption><p>Custom subscription form in the Developer Portal subscription checkout</p></figcaption></figure>

## Management API v2 reference

### GET `/environments/{envId}/subscription-forms`

Retrieves the subscription form for the environment, including disabled forms.

**Response:**

```json
{
  "id": "string",
  "gmdContent": "string",
  "enabled": true
}
```

**Permissions:** `environment-metadata-r`

### PUT `/environments/{envId}/subscription-forms/{subscriptionFormId}`

Updates the subscription form GMD content.

**Request body:**

```json
{
  "gmdContent": "string"
}
```

**Response:** `SubscriptionForm` object

**Permissions:** `environment-metadata-u`

### POST `/environments/{envId}/subscription-forms/{subscriptionFormId}/_enable`

Enables the subscription form for API consumers.

**Response:** `SubscriptionForm` object with `enabled: true`

**Permissions:** `environment-metadata-u`

### POST `/environments/{envId}/subscription-forms/{subscriptionFormId}/_disable`

Disables the subscription form for API consumers.

**Response:** `SubscriptionForm` object with `enabled: false`

**Permissions:** `environment-metadata-u`

### Portal API

#### GET `/subscription-form`

Retrieves the subscription form for the current environment. Only returns the form when it exists and is enabled — returns 404 otherwise. The Portal API response doesn't include the `id` or `enabled` fields.

**Response:**

```json
{
  "gmdContent": "string"
}
```

**Authentication:** Required (Portal auth)

#### GET `/apis/{apiId}/subscription-form`

Retrieves the subscription form for a specific API, including resolved dynamic options. Returns the GMD content and a `resolvedOptions` map containing the effective option lists for fields with EL expressions. The Portal UI merges resolved options into the GMD content before rendering, replacing static or fallback options with values resolved from API and environment metadata.

When an EL expression's API metadata key is missing, the fallback list is used instead. In the Console subscription form editor, EL expressions aren't resolved — only the fallback values are shown as a preview during form design.

**Response:**

```json
{
  "gmdContent": "string",
  "resolvedOptions": {
    "fieldKey": ["option1", "option2"]
  }
}
```

**Authentication:** Required (Portal auth)
