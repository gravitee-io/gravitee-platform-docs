---
description: Access control for APIs in APIM
---

# Manage API Groups and Members

`ApiV4Definition` and `ApiDefinition` CRDs both allow for managing access control to APIs in Gravitee APIM. This means that you can define the groups and members that can or cannot access a specific API in APIM declaratively from a CRD.&#x20;

## Configuring Groups and Members

The syntax is the same for both `ApiV4Definition` and `ApiDefinition` CRDs, with groups and members attributes at the root of the spec:

```yaml
 spec:
  groups:
    - developers
    - users
  members:
    - source: gravitee
      sourceId: my.name@bestproducts.com
      role: USER
    - source: gravitee
      sourceId: another.name@amce.com
      role: WRITER
  # [...]
```

Generally speaking, if a group or member referenced from an API definition does not exist in APIM, that group or member is simply ignored and not added to the API in APIM.&#x20;

There is **one exception** to the above rule: with `ApiDefinition`, if a referenced group doesn't exist, then the group is created in APIM and assigned to the API.

{% hint style="info" %}
For APIs managed by GKO, you will not be able to add or modify groups or members manually from the API management console.
{% endhint %}
