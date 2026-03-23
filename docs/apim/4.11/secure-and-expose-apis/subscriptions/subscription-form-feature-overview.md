# Subscription form feature overview

## Overview

The subscription form feature enables API publishers to define a custom form that API consumers complete when subscribing to API plans. Forms are authored in Gravitee Markdown (GMD) and collect structured metadata stored with each subscription. This feature replaces the legacy comment field from the Classic Portal.

## Key concepts

### Gravitee Markdown (GMD) content

GMD is a structured markup language used to define form fields and layout. Form content is authored in the Management Console using a form editor with live preview. Supported form components include `gmd-input`, `gmd-textarea`, `gmd-select`, `gmd-checkbox`, and `gmd-radio`.

### Subscription metadata

When an API consumer submits a subscription form, the form field values are stored as key-value pairs in the subscription's `metadata` property. Empty values (null, empty strings, whitespace-only) are filtered before storage.

{% hint style="info" %}
Metadata belongs to the subscription, not to the form itself. Each subscription stores its own metadata based on the form field values submitted at subscription time.
{% endhint %}

### Form visibility

Each environment has one subscription form. The **Visible to API consumers** toggle in the Console controls whether the form appears in the Developer Portal. When disabled, the form remains accessible via Management API but returns 404 from the Portal API.

Subscription forms aren't displayed for Keyless plans. In the Portal checkout flow, the form only renders when the selected plan requires authentication (API Key, OAuth2, JWT, or mTLS).

## Prerequisites

- `environment-metadata-r` permission to view subscription forms
- `environment-metadata-u` permission to create, update, enable, or disable subscription forms
- Portal authentication required to retrieve subscription forms via Portal API
