# Subscription Form Restrictions and Validation Rules

## Restrictions

Subscription forms enforce the following limits and validation rules:

- **Field count limit**: Subscription forms are limited to 25 fields. Exceeding this limit triggers `SubscriptionFormDefinitionValidationException` at save time.
- **Metadata entry limit**: Subscription submissions are limited to 25 metadata entries. Exceeding this limit triggers `SubscriptionFormValidationException` at submit time.
- **Character caps**: Input fields are capped at 256 characters; textarea fields at 1024 characters. User-defined `maxLength` values above these caps are clamped with a `normalizedValue` warning.
- **EL syntax requirements**: EL expressions must start with `{#`. Expressions starting with `#{` or `{` (without `#`) trigger `invalidElSyntax` config error.
- **EL fallback requirement**: EL expressions in `options` must include fallback values after `}:`. If omitted, the component reports a `missingElFallback` config error.
- **Mutual exclusion**: A field cannot define both static `options` and `dynamicOptions`. The schema constructor throws `IllegalArgumentException` if both are present.
- **Readonly attribute**: The GMD components `gmd-select` and `gmd-checkbox-group` do not support the `readonly` attribute.
- **Portal API visibility**: The Portal API endpoint `GET /apis/{apiId}/subscription-form` enforces portal navigation visibility rules. If the API is not visible to the user (e.g., `PRIVATE` visibility), the endpoint returns 404.
- **Error severity**: Only severity `error` config errors block save; `warning` (e.g., normalized lengths) does not.


