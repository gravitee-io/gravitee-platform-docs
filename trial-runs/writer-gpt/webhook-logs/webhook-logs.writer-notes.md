# webhook logs.writer notes

The source draft is an outline and does not contain UI labels, navigation paths, or configuration key hierarchies for sampling strategies. The generated article includes inline comments where the documentation cannot be completed without additional product details.

Below are the specific clarifications required to complete the Webhook logs documentation. Each item is expandable so you can provide details for each area.

<details>

<summary>APIM Console navigation and field labels</summary>

We need exact UI navigation and field labels for configuring logging and webhook entrypoint logging.

* Message logging configuration (including where sampling is configured)
* Webhook entrypoint logging configuration (toggles for request/response headers/bodies)
* Webhook logs page action that opens logging configuration

</details>

<details>

<summary>Sampling strategy enforcement</summary>

We need confirmation of semantics and enforcement location/behavior.

* Limit semantics
  * Confirm whether each "Limit" value represents a minimum or a maximum boundary.
* Enforcement location and override behavior
  * Confirm whether sampling is enforced in the UI, at the Gateway, or both.
  * Describe behavior when a sampling configuration is overridden (which source takes precedence, how conflicts are resolved).

</details>

<details>

<summary>`reporting.logging.max_size`</summary>

We need units, defaults, and Helm chart mapping.

* Units and default
  * Confirm the units for `reporting.logging.max_size` (bytes, KB, MB).
  * Provide the default value.
* Helm values path
  * Provide the exact path in the Gateway Helm chart `values.yaml` where `reporting.logging.max_size` is mapped.

</details>

<details>

<summary>Webhook delivery details</summary>

We need specifics on filters, retry policy naming/location, and DLQ configuration/surfacing.

* Filters
  * Confirm whether delivery filters include time range and subscription.
* Retry policy
  * Confirm the retry policy name and where it is configured (APIM Console, Gateway config, Helm, etc.).
* Dead-letter queue (DLQ)
  * Confirm how DLQ is configured and how it is surfaced in the log details (e.g., link to DLQ entry, DLQ status field).

</details>

<details>

<summary>Developer Portal: consumer-scoped webhook delivery history</summary>

We need navigation and visuals for consumers to view delivery history.

* Navigation path and screenshots
  * Provide the Developer Portal navigation path to consumer-scoped webhook delivery history and screenshots.

</details>

<details>

<summary>Screenshots requested</summary>

Please provide the following screenshots to complete the documentation:

* Webhook logs entry in API menu
* Webhook logs list with filters
* Delivery detail view with retry timeline and optional request/response data

</details>

Notes and constraints

* Do not add new product behavior or assumptions beyond what is clarified above.
* Keep all URLs and links exactly as provided (no changes to query parameters).
* Once these clarifications are provided, the draft can be converted into the full Webhook logs documentation with specific UI labels, configuration keys, examples, and screenshots.
