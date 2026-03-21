# Portal API: Subscription Form and Subscription Creation

## Portal API

### GET `/subscription-form`

Returns the subscription form content when the form exists and is enabled. Returns 404 when no subscription form exists for the environment or when the form is disabled.

**Response** (200):

```json
{
  "gmdContent": "string"
}
```

**Error Responses**:

* `404`: Subscription form not found or disabled for the environment
* `500`: Internal server error

### POST `/subscriptions`

Creates a new subscription. The `metadata` field is optional and only sent when a subscription form exists and the plan security type is not `KEY_LESS`.

**Request**: `SubscriptionInput`

```json
{
  "application": "string",
  "plan": "string",
  "request": "string",
  "metadata": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

**Metadata Filtering**:

* Empty string values are removed before submission
* Null values are removed before submission

**Metadata Keys**:

Metadata keys must correspond to the `name` attribute of GMD form fields (e.g., `<gmd-input name="consumer_company_name"/>`). Invalid keys result in a `400 Bad Request` error.

## Related Changes

### Subscription Entity

The subscription entity includes an optional `metadata` field in Management API responses:

### Subscription Detail View

Subscription metadata is displayed as read-only JSON in the subscription detail view. The view shows `-` when metadata is `null`, `undefined`, or an empty object.

### Comment Field Deprecation

The comment field in subscription checkout is deprecated. The plan configuration UI now labels this field as "Classic Portal only."
