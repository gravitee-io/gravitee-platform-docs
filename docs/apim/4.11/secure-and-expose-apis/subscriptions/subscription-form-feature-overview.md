# Subscription Form Feature Overview

## Overview

The Subscription Form feature enables API administrators to define custom forms that API consumers complete when subscribing to an API plan. Forms are built using Gravitee Markdown (GMD) syntax and collect structured metadata as key-value pairs stored with each subscription. This feature replaces the legacy comment-only subscription flow in the Classic Portal.

## Key Concepts

### Gravitee Markdown (GMD)

GMD is a markup language for defining interactive forms within subscription workflows. It supports five input types:

| Input Type | Description |
|:-----------|:------------|
| `gmd-input` | Single-line text fields |
| `gmd-textarea` | Multi-line text areas |
| `gmd-select` | Dropdown lists |
| `gmd-checkbox` | Checkboxes |
| `gmd-radio` | Radio button groups |

Each element supports attributes such as `name`, `label`, `required`, `minLength`, `maxLength`, and `pattern`. Forms are validated in real-time and rendered with live preview in the Console editor.

### Subscription Metadata

Metadata is a set of key-value pairs extracted from the subscription form and stored with each subscription. Empty values (empty strings, whitespace-only, `null`, or `undefined`) are automatically filtered out before submission. Metadata is displayed in the Console UI as read-only JSON with syntax highlighting.

Invalid metadata keys trigger a `400 Bad Request` error with the message "Invalid metadata key."

### Form Visibility

Subscription forms have an `enabled` flag that controls visibility to API consumers:

| Condition | Management API Behavior | Portal API Behavior |
|:----------|:------------------------|:--------------------|
| Form does not exist | Throws `SubscriptionFormNotFoundException` | Throws `SubscriptionFormNotFoundException` |
| Form exists, `enabled = false` | Returns form | Throws `SubscriptionFormNotFoundException` |
| Form exists, `enabled = true` | Returns form | Returns form |

Forms are displayed only for plans with security types other than `KEY_LESS`. For keyless plans, API access information is shown instead.

## Prerequisites

Before configuring a subscription form, ensure you have:

* Environment-level metadata read and update permissions (`environment-metadata-r`, `environment-metadata-u`)
* An API plan with a security type other than `KEY_LESS` (for form display)
* Access to the Gravitee API Management Console

## Creating a Subscription Form

1. Sign in to your APIM Console.
2. From the **Dashboard**, click **Settings**.
3. In the **Settings** menu, go to the **Portal** section, then click **Settings**.
4. In the **New Developer Portal** section, click **Open Settings**. The settings open in a new tab.
5. In the New Developer Portal settings menu, click **Subscription Form**.

The Form Builder displays with three areas:

* **Editor** – Where you write the form definition in GMD
* **Preview** – A live, interactive preview of the form
* **Validation panel** – Shows form validity status and field values

To define the form:

1. In the editor, enter GMD to define your form fields. For example:

 ```markdown
 <gmd-input name="consumer_company_name" label="Company Name" required="true"/>
 ```

2. Set a unique `fieldKey` attribute for each field whose value should be stored when a consumer submits the form.
3. Toggle the **Visible to API consumers** switch to control visibility.
4. Click **Save** to persist the form.

The form is stored per environment with a unique identifier and referenced by `environment_id`.

{% hint style="info" %}
GMD content must not be null, empty, or whitespace-only. If validation fails, a `GraviteeMarkdownContentEmptyException` is thrown.
{% endhint %}

{% hint style="info" %}
If the form has configuration errors (for example, a missing or duplicate `fieldKey`), **Save** is disabled until those issues are fixed.
{% endhint %}

## Subscribing with a Form

API consumers see the subscription form during the subscription workflow when:

* The form is enabled (`enabled = true`)
* The API plan has a security type other than `KEY_LESS`

When a consumer submits the form, metadata is extracted from the form fields and stored with the subscription. Empty values are automatically filtered out before submission.
