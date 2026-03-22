# Creating and Managing Subscription Forms in Console

## Creating a Subscription Form

Navigate to **Settings > Subscription Form** in Console.

1. Enter GMD form content in the editor using available components (`<gmd-input>`, `<gmd-textarea>`, `<gmd-select>`, `<gmd-checkbox>`, `<gmd-radio>`, `<gmd-card>`, `<gmd-grid>`).
2. Preview the form in real-time to verify layout and validation.
3. Click **Save** to persist the form. The button is disabled if content is empty, unchanged, or has configuration errors.
4. Toggle **Visible to API consumers** to enable the form. This requires `environment-metadata-u` permission and no configuration errors. If unsaved changes exist when enabling, a dialog prompts to save and enable in one action.

## Managing Subscription Metadata

Subscription metadata is collected automatically when consumers submit the subscription form in Portal. In Console, view metadata in subscription detail pages under **API Subscriptions** or **Application Subscriptions**. Metadata displays as read-only JSON in a Monaco editor with line numbers and highlighting disabled. If no metadata exists, a dash (`-`) appears. Metadata keys must be valid; invalid keys return HTTP 400 with message `"Invalid metadata key."` Empty string and null values are filtered out before submission.

### Management API

Use the Management API v2 to retrieve, update, enable, and disable subscription forms programmatically.

**GET** `/environments/{envId}/subscription-forms` — Returns the subscription form for the environment, including `id`, `gmdContent`, and `enabled` flag. Returns forms regardless of enabled state.

**PUT** `/environments/{envId}/subscription-forms/{id}` — Updates form content.

**POST** `/environments/{envId}/subscription-forms/{id}/_enable` — Enables the form (sets `enabled: true`).

**POST** `/environments/{envId}/subscription-forms/{id}/_disable` — Disables the form (sets `enabled: false`).
