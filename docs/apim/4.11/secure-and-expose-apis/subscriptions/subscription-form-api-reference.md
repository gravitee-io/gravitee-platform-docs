# Subscription Form API Reference

## Consumer Subscription Flow

When a consumer subscribes to an API with an enabled subscription form, the form appears as step 4 (Checkout) in the subscription wizard, replacing the legacy "Add a comment" card. The consumer fills out the required and optional fields defined in the GMD content. The Next button is disabled until all required fields are valid. On submission, the form values are filtered to remove empty or whitespace-only entries, then attached to the subscription as metadata. If the plan security type is `KEY_LESS`, the form is skipped entirely regardless of configuration.

## API Endpoints

### Management API v2

**GET** `/environments/{envId}/subscription-forms` retrieves the subscription form for an environment, returning 404 if no form exists.

**PUT** `/environments/{envId}/subscription-forms/{id}` updates the `gmdContent` field.

Request:

```json
{
  "gmdContent": "string"
}
```

**POST** `/environments/{envId}/subscription-forms/{id}/_enable` enables the subscription form.

**POST** `/environments/{envId}/subscription-forms/{id}/_disable` disables the subscription form.

### Portal API

**GET** `/subscription-form` retrieves the subscription form only when it exists and is enabled, returning 404 otherwise. This endpoint requires `@RequirePortalAuth` and is called by the consumer subscription flow to determine whether to display the form.

Response (200):

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Subscription form identifier |
| `environmentId` | string | Environment identifier |
| `gmdContent` | string | GMD-formatted form content |
| `enabled` | boolean | Whether the form is enabled |
| `createdAt` | number | Creation timestamp |
| `updatedAt` | number | Last update timestamp |

## Subscription Entity Schema

The `Subscription` entity includes a new `metadata` field of type `Record<string, string>`. When creating a subscription via **POST** `/subscriptions`, include the optional `metadata` property in the request body:

```json
{
  "application": "app-id",
  "plan": "plan-id",
  "metadata": {
    "consumer_company_name": "Acme Corp",
    "consumer_use_case": "Internal analytics dashboard"
  }
}
```

## Metadata Display

Subscription metadata is visible in two locations: the API publisher's subscription management view and the application owner's subscription list. Both views use a read-only Monaco editor configured with JSON syntax highlighting, line wrapping, and a clipboard copy button. When metadata is `undefined`, `null`, or an empty object, a dash (`-`) is displayed instead of the editor.

## Restrictions

* Each environment can have exactly one subscription form (enforced by unique constraint on `environment_id`)
* GMD content must not be null, empty, or whitespace-only (validated on save)
* Subscription metadata keys must follow a valid format (invalid keys return `400 Bad Request` with message "Invalid metadata key.")
* Subscription forms do not appear for plans with `KEY_LESS` security type
