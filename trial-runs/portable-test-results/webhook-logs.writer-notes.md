# Writer Notes: webhook-logs

## Clarifications Required

1. **New webhook logs list view**: The draft references a "new screen" for viewing webhook logs with TODO markers. The provided screenshots do not include this view. A screenshot of the actual webhook logs list is needed to complete the "View webhook logs" section.

2. **Configuration from logs page**: The draft mentions the ability to configure logging from the Webhook log page with a button in the top right. This UI element is not shown in the provided screenshots. Confirmation of this workflow and a supporting screenshot are needed.

3. **Helm configuration**: The draft mentions providing Helm equivalents for the `gravitee.yml` settings but does not include the actual Helm values. The Helm chart property paths for `reporting.logging.max_size` and sampling settings are needed.

4. **Sampling strategy configuration UI**: The draft lists sampling strategies with default and limit values but does not explain how users configure these in the UI. Clarification is needed on where these settings appear and how users interact with them.

5. **DLQ (Dead Letter Queue) configuration**: The log details mention DLQ status, but the draft does not explain how to configure DLQ for webhooks. Confirm if this should be covered in this article or linked to a separate article.

## Uncertainties

- The exact behavior when sampling settings are configured in `gravitee.yml` vs. UI is stated to make UI settings "read-only," but the specific UI indication of this state is not described.

- The relationship between message logging and webhook logging is mentioned as separate, but the draft suggests they may share some configuration. The exact relationship needs clarification.

## Unused Screenshot

- `screenshots/image_3.jpg` (Gravitee branding) was not used as it does not contain documentation-relevant content.