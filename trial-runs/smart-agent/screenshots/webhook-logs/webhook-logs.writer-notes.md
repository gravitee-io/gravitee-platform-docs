# webhook logs.writer notes

## Clarifications needed

<details>

<summary>Screenshot placeholders</summary>

* The draft indicates "TODO: screenshot" for:
  * webhook logs list view
  * detailed log view with all options (retry, request, response)

The final article will need these screenshots added (placeholders currently referenced in the draft).

</details>

<details>

<summary>gravitee.yml configuration</summary>

* The draft mentions configuration in `gravitee.yml` and a Helm version for message-related settings, but does not provide the actual YAML syntax.
* Specific missing configuration examples needed:
  * Sampling strategy defaults and limits
  * `reporting.logging.max_size` setting

No YAML examples are provided in the draft; these must be supplied to complete the documentation.

</details>

<details>

<summary>Configure button location</summary>

* The draft states: "It is possible to configure this from the Webhook log page" and refers to a "top right button".
* This UI element location needs confirmation (screenshot and/or precise UI path).

</details>

<details>

<summary>License requirements</summary>

* The PRD mentions the feature is for enterprise customers (Relex commitment), but neither document specifies whether this feature requires an Enterprise Edition license.
* Clarify license requirements and any gating by edition.

</details>

<details>

<summary>Sampling strategy configuration UI</summary>

* The draft mentions sampling strategies but does not clarify:
  * Whether sampling strategies are configured per-API or globally
  * Whether there is a UI for sampling strategy configuration or if it's only configurable via `gravitee.yml`
* This needs confirmation.

</details>

<details>

<summary>Message logging vs webhook logging relationship</summary>

* The draft states webhook logging is "separate settings from message sampling", but the exact relationship is unclear.
* Clarify:
  * Where message logging is configured versus where webhook logging is configured
  * How webhook logging and message sampling interact (if at all)

</details>

## Image usage

* webhook-menu-navigation.png: Used for step 3 of enabling callback metrics (first provided image)
* callback-reporting-settings.png: Used for step 4 of enabling callback metrics (second provided image)
* A third image (Gravitee branding) was not used because it contains no documentation-relevant content

## Notes for the final article

* Add the missing screenshots where the draft has "TODO: screenshot".
* Provide explicit `gravitee.yml` (or Helm values) examples for:
  * Sampling strategy defaults and limits
  * `reporting.logging.max_size`
* Confirm the exact UI location and appearance of the configure button on the Webhook log page and update screenshots accordingly.
* Clarify license/edition requirements for the feature.
* Clarify scope and UI/CLI location for sampling strategy configuration (per-API vs global).
* Clarify relationship between message logging and webhook logging, including where each is configured.
