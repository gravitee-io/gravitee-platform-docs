# Subscription Form Management API Reference

## Management API Endpoints

### GET `/environments/{envId}/subscription-forms`

Retrieves the subscription form for the environment. Returns the form regardless of the `enabled` flag.

**Response (200 OK)**:

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `id` | string | Subscription form identifier | `"subscription-form-id"` |
| `gmdContent` | string | GMD form content | `"<gmd-input name=\"name\" label=\"Name\" fieldKey=\"name\" required=\"true\"></gmd-input>"` |
| `enabled` | boolean | Whether form is visible to consumers | `false` |

### PUT `/environments/{envId}/subscription-forms/{formId}`

Updates the subscription form content. The request body must include the `gmdContent` property.

**Request Body**:

```json
{
 "gmdContent": "# Updated Form\n\n<gmd-input name=\"email\" label=\"Email\" fieldKey=\"email\" required=\"true\"></gmd-input>"
}
```

**Response (200 OK)**: Same as GET response.

{% hint style="warning" %}
Updating a non-existent subscription form throws `TechnicalException` with message `"Subscription form not found with id [id]"`.
{% endhint %}

### POST `/environments/{envId}/subscription-forms/{formId}/_enable`

Enables the subscription form, making it visible to API consumers. Returns the updated form with `enabled: true`.

**Response (200 OK)**: Updated subscription form with `enabled: true`.

### POST `/environments/{envId}/subscription-forms/{formId}/_disable`

Disables the subscription form, hiding it from API consumers. Returns the updated form with `enabled: false`.

**Response (200 OK)**: Updated subscription form with `enabled: false`.
