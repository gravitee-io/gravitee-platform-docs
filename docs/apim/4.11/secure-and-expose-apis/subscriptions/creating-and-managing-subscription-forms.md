# Creating and Managing Subscription Forms

## Gateway Configuration

## Creating Subscription Forms

1. Navigate to **Portal Settings > Subscription Form** in the Management Console.
2. Author form content using the Monaco editor with GMD syntax. The live preview pane displays the rendered form in real time.
3. Toggle the **Enabled** switch to make the form visible to API consumers in the Portal.
4. Click **Save** to persist changes.

The unsaved changes guard prevents accidental navigation away from unsaved edits. Forms are scoped to the environment level — each environment has one subscription form identified by `environment_id` (unique constraint).

## Managing Subscription Forms

### Updating Form Content

1. Edit the GMD content in the Monaco editor.
2. Click **Save** to persist changes.

### Enabling or Disabling Forms

Enable or disable the form using the toggle switch or by calling the following endpoints:

* `POST /environments/{envId}/subscription-forms/{id}/_enable`
* `POST /environments/{envId}/subscription-forms/{id}/_disable`

When a form is disabled, it remains accessible via Management API (`GET /environments/{envId}/subscription-forms`) but returns 404 from Portal API (`GET /subscription-form`).

### Viewing Subscription Metadata

Subscription metadata is displayed in subscription details pages (API subscriptions and application subscriptions) using a read-only JSON Monaco editor. If metadata is `undefined`, `null`, or an empty object, the viewer displays `-`.

## End-User Configuration

### Management API v2

#### GET `/environments/{envId}/subscription-forms`

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

#### PUT `/environments/{envId}/subscription-forms/{id}`

Updates the subscription form GMD content.

**Request Body:**

```json
{
  "gmdContent": "string"
}
```

**Response:** `SubscriptionForm` object

**Permissions:** `environment-metadata-u`

#### POST `/environments/{envId}/subscription-forms/{id}/_enable`

Enables the subscription form for API consumers.

**Response:** `SubscriptionForm` object with `enabled: true`

**Permissions:** `environment-metadata-u`

#### POST `/environments/{envId}/subscription-forms/{id}/_disable`

Disables the subscription form for API consumers.

**Response:** `SubscriptionForm` object with `enabled: false`

**Permissions:** `environment-metadata-u`

### Portal API

#### GET `/subscription-form`

Retrieves the subscription form for the current environment.

**Response:**

**Behavior:**

* Returns 200 with form content when form exists and `enabled = true`
* Returns 404 when form is not found or `enabled = false`

**Authentication:** Required
