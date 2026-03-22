# Subscribing to APIs with Subscription Forms

## Subscribing to an API with a Subscription Form

When an API consumer subscribes to an API plan in the Portal, the subscription form is displayed during checkout if the form exists, is enabled, and the plan security type is not `KEY_LESS`. The form renders using the GMD content defined by the administrator. Required fields are validated in real-time. The Subscribe button is disabled until all required fields are valid. Upon submission, form values are collected using `fieldKey` attributes and sent as subscription metadata. Empty or whitespace-only values are filtered out. 
The metadata is stored with the subscription entity and displayed in the [Management Console subscription detail views](../../../guides/api-exposure-plans-applications-and-subscriptions/subscriptions.md).


The Subscription Metadata Viewer displays collected metadata in subscription detail views (API and Application contexts). The viewer shows a dash (`-`) if metadata is `undefined`, `null`, or an empty object. When metadata exists, the viewer renders a read-only Monaco editor with JSON content. The viewer applies a `1px` border and `4px` border radius.
