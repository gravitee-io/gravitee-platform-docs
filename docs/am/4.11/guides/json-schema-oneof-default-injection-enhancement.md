# JSON Schema oneOf Default Injection Enhancement

## JSON Schema oneOf Default Injection

The JSON schema validator now detects when the underlying everit-json-schema library has already injected default values into the target object during oneOf validation. If all required properties and const constraints of the selected subschema are satisfied, the validator skips manual default injection. This prevents duplicate defaults when the validator mutates the object in-place.

The selection algorithm first checks for discriminator properties matching const values, then falls back to the first subschema if no discriminator is present.

{% hint style="warning" %}
oneOf default injection relies on undocumented everit-json-schema behaviors: non-fail-fast allOf validation and in-place mutation. Future everit versions may break this behavior without compile-time signals.
{% endhint %}

### Detection Logic

The validator checks whether all required properties and const constraints of the selected subschema are already satisfied by the target JSON object. If satisfied, manual default injection is skipped.

**Validation method:**

```java
/**
 * Checks whether all required properties and const constraints of the given subschema
 * are already satisfied by the target JSON object — without injecting any defaults.
 */
private boolean validatorPrefilledDefaults(ObjectSchema matchingSubschema, JSONObject targetObject) {
 if (!matchingSubschema.getRequiredProperties().stream().allMatch(targetObject::has)) {
 return false;
 }
 return matchingSubschema.getPropertySchemas().entrySet().stream()
 .allMatch(e -> {
 Schema unwrapped = unwrapSchema(e.getValue());
 if (!(unwrapped instanceof ConstSchema)) {
 return true;
 }
 Object constVal = ( unwrapped).getPermittedValue();
 return targetObject.has(e.getKey()) && constVal.equals(targetObject.get(e.getKey()));
 });
}
```

### Selection Algorithm

The validator selects a oneOf subschema using the following order:

1. **Discriminator detection**: If input contains a property matching a const in a subschema, that subschema is selected.
2. **Validator pre-filling fallback**: Checks whether all required properties and const constraints of a subschema are already satisfied by the target JSON object (without injecting defaults).
3. **Default fallback**: If no discriminator is found, the first subschema is selected.
4. **Default injection**: Missing const values and missing required properties with defaults are injected from the selected subschema.

### Example Behavior

**Schema:**

```json
{
 "type": "object",
 "properties": {
 "partyType": {
 "type": "string",
 "default": "COMPANY",
 "enum": ["COMPANY", "NATURAL"]
 },
 "name": {
 "type": "string",
 "default": "ACME"
 }
 },
 "oneOf": [
 {
 "properties": {
 "partyType": {
 "const": "NATURAL"
 }
 },
 "required": ["partyType"]
 },
 {
 "properties": {
 "partyType": {
 "const": "COMPANY"
 }
 },
 "required": ["partyType", "name"]
 },
 {
 "not": {
 "required": ["partyType"]
 },
 "required": ["name"]
 }
 ]
}
```

**Behavior:**

- Input: `{"partyType": "NATURAL"}` → Output: `{"name":"ACME","partyType":"NATURAL"}`
- Input: `{}` → Output: `{"name":"ACME","partyType":"COMPANY"}`

## Prerequisites

Before using oneOf default injection, upgrade the gravitee-plugin-validator dependency from 2.0.2 to 2.3.0.
