---
description: Access control for APIs in APIM
---

# Manage API and application groups and members

`ApiV4Definition`, `ApiDefinition`, and `Application` CRDs all support the configuration of user permissions. This means that you can define the groups and members that can or cannot access a specific API or application in APIM, and do this declaratively from a CRD.

## Configuring groups and members

The syntax is the same for `ApiV4Definition`, `ApiDefinition`, and `Application` CRDs, with groups and members attributes at the root of the spec:

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

Generally speaking, if a group or member referenced from an API or application does not exist in APIM, that group or member is simply ignored and not added to the resource in APIM.

{% hint style="info" %}
For APIs managed by GKO, you will not be able to add or modify groups or members manually from the API Management Console.
{% endhint %}
