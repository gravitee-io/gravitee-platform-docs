# Subscription Form Feature Overview

## Overview

The Subscription Form feature enables API administrators to define custom forms that API consumers complete when subscribing to API plans. Forms are authored in Gravitee Markdown (GMD) and collect structured metadata stored with each subscription. This feature replaces the legacy comment field from the Classic Portal.

## Key Concepts

### Gravitee Markdown (GMD) Content

GMD is a structured markup language used to define form fields and layout. Form content is authored in the Management Console using a Monaco editor with live preview. Example GMD syntax:

```markdown
# Subscription Information
<gmd-input name="consumer_company_name" label="Company Name" required="true"/>
<gmd-textarea name="consumer_use_case" label="Use Case" required="true"/>
```

GMD content must not be null, empty, or whitespace-only. Validation throws `GraviteeMarkdownContentEmptyException` if this rule is violated.

### Subscription Metadata

Form field values submitted by API consumers are stored as key-value pairs in the subscription's `metadata` property. Empty values (null, empty strings, whitespace-only strings) are filtered before storage. Invalid metadata keys trigger `SubscriptionMetadataInvalidException` with HTTP 400 response.

### Form Visibility

Each environment has one subscription form with an `enabled` flag. When `enabled = true`, the form is visible to API consumers in the Portal. When `enabled = false`, the form is hidden from Portal API responses but remains accessible via Management API. If no form exists or the form is disabled, Portal API returns 404.

### Form Components

| Component | Purpose |
|:----------|:--------|
| `<gmd-form-host>` | Container for rendering GMD forms in Portal |
| `<gmd-viewer>` | Read-only GMD content renderer |
| `<gmd-form-editor>` | Live preview editor in Management Console |
| `SubscriptionMetadataViewerComponent` | Displays submitted metadata in subscription details (read-only JSON Monaco editor) |

## Prerequisites

- User must have `environment-metadata-r` permission to view subscription forms
- User must have `environment-metadata-u` permission to create or update subscription forms
- Portal authentication required to retrieve subscription forms via Portal API
- JDBC repository support required for persistence (schema version 08)

## Gateway Configuration

No gateway-level configuration is required for subscription forms.
