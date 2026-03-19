# Subscription form API reference

## Management API v2

### Get subscription form

**GET** `/environments/{envId}/subscription-forms`

Retrieves the subscription form for the specified environment. Returns `404` if no form exists.

**Permission:** `ENVIRONMENT_METADATA` — READ

### Update subscription form content

**PUT** `/environments/{envId}/subscription-forms/{subscriptionFormId}`

Updates the GMD content of a subscription form.

**Permission:** `ENVIRONMENT_METADATA` — UPDATE

**Request body:**

```json
{
  "gmdContent": "<gmd-input name=\"company\" label=\"Company\" fieldKey=\"company\" required=\"true\"></gmd-input>"
}
```

### Enable subscription form

**POST** `/environments/{envId}/subscription-forms/{subscriptionFormId}/_enable`

Enables the subscription form, making it visible to consumers in the Developer Portal.

**Permission:** `ENVIRONMENT_METADATA` — UPDATE

### Disable subscription form

**POST** `/environments/{envId}/subscription-forms/{subscriptionFormId}/_disable`

Disables the subscription form. Consumers won't see the form during the subscription flow.

**Permission:** `ENVIRONMENT_METADATA` — UPDATE

## Portal API

### Get subscription form

**GET** `/subscription-form`

Retrieves the subscription form for the current environment. Returns `404` if no form exists or if the form is disabled. Requires Portal authentication.

**Response (200):**

<table>
    <thead>
        <tr>
            <th width="167">Field</th>
            <th width="120">Type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>id</code></td>
            <td>string</td>
            <td>Subscription form identifier</td>
        </tr>
        <tr>
            <td><code>environmentId</code></td>
            <td>string</td>
            <td>Environment identifier</td>
        </tr>
        <tr>
            <td><code>gmdContent</code></td>
            <td>string</td>
            <td>GMD-formatted form content</td>
        </tr>
        <tr>
            <td><code>enabled</code></td>
            <td>boolean</td>
            <td>Whether the form is enabled</td>
        </tr>
        <tr>
            <td><code>createdAt</code></td>
            <td>number</td>
            <td>Creation timestamp</td>
        </tr>
        <tr>
            <td><code>updatedAt</code></td>
            <td>number</td>
            <td>Last update timestamp</td>
        </tr>
    </tbody>
</table>

## Subscription metadata in requests

When creating a subscription through **POST** `/subscriptions`, include the optional `metadata` property in the request body:

```json
{
  "application": "app-id",
  "plan": "plan-id",
  "metadata": {
    "app_name": "My Integration",
    "team": "Engineering",
    "use_case": "Internal analytics dashboard"
  }
}
```

Metadata is stored as `Map<String, String>` on the subscription entity. For validation rules and constraints, see [Subscription forms — Metadata validation rules](subscription-forms.md#metadata-validation-rules).
