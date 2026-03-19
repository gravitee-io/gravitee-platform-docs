# Subscription forms

{% hint style="info" %}
Subscription forms are available for v4 APIs and API Products. Plans with **Keyless** security type don't display subscription forms.
{% endhint %}

## Overview

Subscription forms let API publishers define custom input fields that API consumers fill out when subscribing to a plan in the Developer Portal. The form data is stored as key-value metadata on the subscription record and is accessible to both publishers and consumers after submission.

Subscription forms replace the legacy **Consumer must provide a comment when subscribing to a plan** toggle from the Classic Portal. The `comment_required` plan flag has no effect in the Next-Gen Portal.

Each environment has one subscription form. The form applies to all plans (except Keyless) across all APIs in that environment.

## Create a subscription form

1. In the Console, navigate to **Portal Settings > Subscription Form**.
2. Define input fields using Gravitee Markdown (GMD) tags in the editor. A live preview renders on the right side.
3. Click **Save** to persist the form content.
4. Toggle the **Enable** switch to make the form visible to API consumers in the Developer Portal.

{% hint style="warning" %}
The **Enable** toggle is disabled when configuration errors are present or when the user lacks the `ENVIRONMENT_METADATA` update permission.
{% endhint %}

An unsaved changes guard prompts for confirmation if you navigate away from the editor with unsaved changes.

### Supported form field types

The following GMD form components are available:

<table>
    <thead>
        <tr>
            <th width="200">Component</th>
            <th width="350">Description</th>
            <th>Example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>&lt;gmd-input&gt;</code></td>
            <td>Single-line text input. Supports <code>type</code> attribute for email, URL, and number variants.</td>
            <td><code>&lt;gmd-input name="company" label="Company" fieldKey="company" required="true"&gt;&lt;/gmd-input&gt;</code></td>
        </tr>
        <tr>
            <td><code>&lt;gmd-textarea&gt;</code></td>
            <td>Multi-line text input. Supports <code>minLength</code> and <code>maxLength</code> attributes.</td>
            <td><code>&lt;gmd-textarea name="useCase" label="Use case" fieldKey="use_case" required="true"&gt;&lt;/gmd-textarea&gt;</code></td>
        </tr>
        <tr>
            <td><code>&lt;gmd-select&gt;</code></td>
            <td>Dropdown selection. Define options as a comma-separated list.</td>
            <td><code>&lt;gmd-select name="team" label="Team" fieldKey="team" options="Engineering,Product,Other"&gt;&lt;/gmd-select&gt;</code></td>
        </tr>
        <tr>
            <td><code>&lt;gmd-radio&gt;</code></td>
            <td>Radio button group. Define options as a comma-separated list.</td>
            <td><code>&lt;gmd-radio name="env" label="Environment" fieldKey="env" options="Production,Staging,Dev"&gt;&lt;/gmd-radio&gt;</code></td>
        </tr>
        <tr>
            <td><code>&lt;gmd-checkbox&gt;</code></td>
            <td>Single checkbox for boolean or acknowledgment fields.</td>
            <td><code>&lt;gmd-checkbox name="terms" label="I accept the terms" fieldKey="accept_terms" required="true"&gt;&lt;/gmd-checkbox&gt;</code></td>
        </tr>
    </tbody>
</table>

GMD forms also support layout components (`gmd-grid`, `gmd-card`, `gmd-md`) and custom CSS styling. For a complete example, refer to the default template that appears when creating a new form.

### Example form

```markdown
<gmd-grid columns="1">
  <gmd-card>
    <gmd-card-title>Subscription request</gmd-card-title>
    <gmd-input name="appName" label="Application name" fieldKey="app_name" required="true"></gmd-input>
    <gmd-select name="team" label="Team" fieldKey="team" options="Engineering,Product,Data,Other"></gmd-select>
    <gmd-textarea name="useCase" label="Use case description" fieldKey="use_case" required="true" minLength="20" maxLength="500"></gmd-textarea>
    <gmd-checkbox name="terms" label="I confirm this information is accurate" fieldKey="confirm_accuracy" required="true"></gmd-checkbox>
  </gmd-card>
</gmd-grid>
```

## Consumer subscription experience

When a subscription form is enabled and the selected plan's security type isn't Keyless, the form appears in the **Review** step of the subscription wizard in the Developer Portal.

The consumer subscription flow works as follows:

1. The consumer selects a plan.
2. The consumer selects an application.
3. (Push plans only) The consumer configures the push consumer.
4. In the **Review** step, the subscription form renders below the subscription summary. The consumer fills in the required and optional fields.
5. The **Subscribe** button is disabled until all required form fields are valid.
6. On submission, empty or whitespace-only values are filtered out, and the remaining values are attached to the subscription as metadata.

{% hint style="info" %}
Form field validation (for example, required fields) is enforced in the Developer Portal UI only. Subscriptions created through the management API or the Console don't enforce the form schema.
{% endhint %}

## View subscription metadata

After a subscription is created with metadata, the metadata is visible in the following locations:

- **Console — API subscription detail:** Navigate to **APIs > [API] > Consumers > Subscriptions** and select a subscription. Metadata appears as read-only JSON.
- **Console — Application subscription detail:** Navigate to **Applications > [Application] > Subscriptions** and select a subscription. Metadata appears as read-only JSON.
- **Developer Portal:** Application owners see metadata on their subscription details.

When no metadata exists for a subscription, a dash (`-`) is displayed.

## Metadata validation rules

The management API enforces the following validation rules on subscription metadata:

<table>
    <thead>
        <tr>
            <th width="250">Rule</th>
            <th>Detail</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Key format</td>
            <td>Alphanumeric characters, hyphens, and underscores only. Regex: <code>^[A-Za-z0-9_-]{1,100}$</code></td>
        </tr>
        <tr>
            <td>Max value length</td>
            <td>1024 characters per value</td>
        </tr>
        <tr>
            <td>Max metadata entries</td>
            <td>25 key-value pairs per subscription</td>
        </tr>
        <tr>
            <td>HTML sanitization</td>
            <td>HTML tags are stripped from values to prevent XSS. Special characters (for example, <code>@</code>, <code>+</code>, <code>=</code>) are stored as-is.</td>
        </tr>
    </tbody>
</table>

## Limitations

* **One form per environment:** Each environment supports exactly one subscription form. The form applies to all non-Keyless plans.
* **Keyless plans excluded:** Subscription forms don't appear for plans with Keyless security type.
* **Schema isn't enforced for publishers:** The form schema defined for the Portal isn't enforced for API publishers creating or modifying subscriptions through the Console or the management API.
* **Metadata is read-only for consumers:** Application owners view their subscription metadata but can't modify it, including through the management API or Portal API.

## Permissions

<table>
    <thead>
        <tr>
            <th width="300">Permission</th>
            <th>Access</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>ENVIRONMENT_METADATA</code> — READ</td>
            <td>View the subscription form editor and form content</td>
        </tr>
        <tr>
            <td><code>ENVIRONMENT_METADATA</code> — UPDATE</td>
            <td>Edit form content, enable or disable the form</td>
        </tr>
    </tbody>
</table>
