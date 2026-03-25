# Subscribing to APIs with Subscription Forms (Portal End-User Guide)

## Subscribing with Metadata

{% hint style="info" %}
You must be authenticated in the Portal to subscribe to APIs.
{% endhint %}

API consumers view the subscription form in the Portal during the subscription checkout process. The form appears when the plan security type is not `KEY_LESS` and the form exists and is enabled.

To subscribe with metadata:

1. Complete the form fields. Required fields must have values. Validation rules (e.g., `minLength`, `maxLength`, `type`) are enforced.
2. Click **Subscribe** to submit the subscription request. The button is disabled if the form is invalid.

The Portal extracts field values using the `fieldKey` attributes and sends them as a `metadata` object in the `POST /subscriptions` request. Empty or whitespace-only values are filtered out. The metadata is stored with the subscription and displayed in the Console's subscription details view as read-only JSON.

{% hint style="info" %}
Subscription forms are not displayed for `KEY_LESS` plan security types.
{% endhint %}


<!-- KNOWN GAP: End-user configuration details pending SME input -->


