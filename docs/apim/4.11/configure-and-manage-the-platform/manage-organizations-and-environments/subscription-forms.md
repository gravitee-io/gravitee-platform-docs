# Creating and Managing Subscription Forms

## Creating and Managing Subscription Forms

### Navigate to Subscription Form Settings

1. In the Management Console, navigate to **Settings > Subscription Form**.

### Edit Form Content

1. Enter GMD form content in the editor using available form components.
2. The live preview pane displays the rendered form.

### Save Changes

1. Click **Save** to persist changes.

{% hint style="info" %}
The save button is disabled when content is empty, unchanged, or contains configuration errors.
{% endhint %}

### Enable or Disable the Form

1. Toggle **Visible to API consumers** to enable the form.

{% hint style="warning" %}
The toggle is disabled when configuration errors exist or when you lack `environment-metadata-u` permission.
{% endhint %}

### Unsaved Changes Warning

The browser warns you of unsaved changes if you attempt to navigate away with pending edits.

### Example GMD Form

```html
<gmd-grid columns="2">
  <gmd-card>
    <gmd-card-title>Applicant Information</gmd-card-title>
    <gmd-input name="fullName" label="Full name" fieldKey="full_name" required="true"></gmd-input>
    <gmd-input name="email" label="Email address" fieldKey="email" type="email" required="true"></gmd-input>
    <gmd-select name="country" label="Country" fieldKey="country" required="true" options="United States,Canada,United Kingdom"></gmd-select>
  </gmd-card>
</gmd-grid>
```
