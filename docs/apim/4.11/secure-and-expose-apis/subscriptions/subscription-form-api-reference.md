# Subscription Form API Reference

# Subscription Information
<gmd-input name="consumer_company_name" label="Company Name" required="true"/>
<gmd-textarea name="consumer_use_case" label="Use Case" required="true"/>
```

### Subscription Creation with Metadata

When creating a subscription, the following properties are supported:

| Property | Type | Description |
|:---------|:-----|:------------|
| `application` | string | Application identifier |
| `plan` | string | Plan identifier |
| `request` | string (optional) | Legacy comment field (Classic Portal only) |
| `configuration` | object (optional) | Consumer-specific configuration |
| `metadata` | Record<string, string> (optional) | Key-value pairs from subscription form |

The `request` field is labeled "Classic Portal only" and is deprecated in favor of subscription forms.

## Related Changes

The subscription form feature deprecates the legacy "comment required" field in favor of structured metadata collection through GMD forms.
