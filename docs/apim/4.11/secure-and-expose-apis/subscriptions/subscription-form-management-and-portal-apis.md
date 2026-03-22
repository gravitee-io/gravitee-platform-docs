# Subscription Form Management and Portal APIs

## End-User Configuration

### GMD Component Attributes

Configure form fields using GMD component attributes. All components support `name` (metadata key), `label` (display label), `fieldKey` (internal identifier), and `required` (boolean validation).


| Component | Additional Attributes | Example |
|:----------|:---------------------|:--------|
| `<gmd-input>` | `type`, `placeholder`, `minLength`, `maxLength`, `pattern` | `<gmd-input name="company" label="Company Name" required="true" minLength="3"/>` |
