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

If a role is omitted or cannot be found (e.g., due to a typo), the member will be assigned the default role for that specific scope (API or Application). If no default role is defined in the organization settings for that scope, the system will return an error.

{% hint style="info" %}
For APIs managed by GKO, you will not be able to add or modify groups or members manually from the API Management Console.
{% endhint %}

## Limitations

In the Gravitee API Management Console, there are environment-level settings that you can use to automatically assign groups to every new API or application that a user creates. These settings are shown in the following screenshot.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

Starting from 4.7.4, this feature has been made available for APIs and applications managed by the Kubernetes Operator as well.

However, the operator handles resources declaratively. If you disable automatic associations in the management UI, groups added to APIs or applications by this feature are removed whenever the Kubernetes resource is updated. To avoid this issue, add the group to the resource before performing the update.
