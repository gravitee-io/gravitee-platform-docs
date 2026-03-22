# Subscription Form Technical Implementation Reference

## Related Changes

The subscription form feature introduces a new navigation menu item in Environment Settings with the label "Subscription Form" and route `subscription-form`. Permissions were updated from `environment-settings-r/u` to `environment-metadata-r/u`. The Console UI now displays subscription metadata in a read-only Monaco editor with JSON syntax highlighting, hidden when metadata is empty. A new JDBC table `subscription_forms` stores form content with columns `id`, `environment_id`, `gmd_content`, and `enabled`. The feature depends on the `@gravitee/gravitee-markdown` Angular library for form editing, viewing, and state management, and uses Angular Material components (`MatSlideToggleModule`, `MatButtonModule`, `MatTooltipModule`) for UI controls.
