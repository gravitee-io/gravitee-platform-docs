---
description: The Group custom resource creates a group in an API Management environment through the Gravitee Kubernetes Operator 4.13. Follow its validation rules.
---

# Group

The `Group` custom resource allows to create a group in a given APIM environment. Groups created using this resource can be later on either referenced as kubernetes object references (i.e. using the group metadata name and an optional namespace), or using their name as it was already possible for groups created from the API management console.

## Create a `Group`

Because groups are only relevant for a given APIM environment, group resource *must* reference an existing management context object.

The example below shows a simple `Group` custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Group
metadata:
  name: developers
spec:
  contextRef:
    name: "dev-ctx"
  name: "developers"
  notifyMembers: false
  members:
  - source: memory
    sourceId: api1
    roles:
      API: OWNER
      APPLICATION: OWNER
      INTEGRATION: USER
```

## Validation and defaults

The rule for validation and defaults are the same as already in place for API and Application members. This means that

  - Unknown members added to a group will result in a warning being issued and the member being discarded
  - Role scope that are not defined will result in the default role for that scope being applied when the group is created in APIM
  - Unknown role names will result in a warning being issued and the default role for the scope being applied.

## Set default roles for new members

The `defaultMemberRoles` field sets the role that a user receives when they join the group, for each kind of resource the group gives access to. This includes users who log in through an identity provider that maps them to the group. The field requires APIM 4.14.0 or later, and APIM 4.13 ignores it.

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Group
metadata:
  name: developers
spec:
  contextRef:
    name: "dev-ctx"
  name: "developers"
  defaultMemberRoles:
    api: USER
    application: USER
    apiProduct: USER
  members: []
```

| Field         | Sets the default role on                        |
| ------------- | ----------------------------------------------- |
| `api`         | The APIs that the group gives access to         |
| `application` | The applications that the group gives access to |
| `apiProduct`  | The API Products that the group gives access to |

Each value is the name of a role that your organization defines for that scope, such as `USER`, `OWNER`, or a custom role. In the Console, these roles are the group's **Default API Role**, **Default Application Role**, and **Default API Product Role**. The keys differ from the keys of `roles` in a `members` entry, which are `API`, `APPLICATION`, and `INTEGRATION`.

GKO applies the field as follows:

* When `defaultMemberRoles` is omitted, APIM keeps the group's default roles as they are. Omit it when you set the default roles in the Console.
* When `defaultMemberRoles` is declared, it sets all three default roles. A scope that the field doesn't list loses its default role.
* `defaultMemberRoles: {}` removes all three default roles.

The following rules apply to the role names:

* `PRIMARY_OWNER` can't be a default role. A group that sets it isn't created or updated, and GKO returns an error that includes `setting primary owner as default api role is not allowed`.
* A role name that doesn't exist in your organization returns a warning such as `default api role [<name>] doesn't exist`, and that scope is left without a default role.

For more information about how GKO returns errors and warnings, see [Admission validation](../admission-validation.md).

## Leave the members to APIM

To let APIM manage the members of a group, set the `gravitee.io/ignore-members` annotation to `"true"`. GKO then doesn't add or remove members. Users who join the group in APIM stay in it, such as users who log in through an identity provider that maps them to the group. The annotation requires APIM 4.14.0 or later. APIM 4.13 ignores it, so GKO still removes the members that `members` doesn't list.

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Group
metadata:
  name: developers
  annotations:
    gravitee.io/ignore-members: "true"
spec:
  contextRef:
    name: "dev-ctx"
  name: "developers"
  defaultMemberRoles:
    api: USER
    application: USER
    apiProduct: USER
  members: []
```

With the annotation set to `"true"`, the following rules apply:

* GKO still applies the other fields of the group, including `notifyMembers` and `defaultMemberRoles`.
* The `members` field is still required, so set it to an empty list. If it lists members, GKO accepts the manifest with the warning `spec.members is not applied while gravitee.io/ignore-members is true`.

To manage the members from the manifest again, remove the annotation or set it to `"false"`. When you apply the change, GKO removes the members that `members` doesn't list. With `members: []`, that removes the members who joined the group in APIM.

## Group settings managed in the Console

Starting with APIM 4.14.0, an update from GKO applies the `name`, `notifyMembers`, `defaultMemberRoles`, and `members` of a group, and the following settings keep the values set in the Console:

* **Allow Group Admin to change default API role**, **Allow Group Admin to change default API Products role**, and **Allow Group Admin to change default application role**
* **Automatically add group to new APIs**, **Automatically add group to new API Products**, and **Automatically add group to new applications**
* **Max Number Of Members**, **Allow adding members via user search**, and **Allow sending invitations to users via email**

With APIM 4.13, each update from GKO resets these settings.

## Referencing a group from an ApiDefinition

With the addition of the Group custom resources, there are two ways of adding a group to an ApiDefinition.

### Using group names

```yaml
 spec:
  groups:
    - developers
```

### Using group references

```yaml
 spec:
  groupRefs:
    - name: developers
  # [...]
```

In that case, if the group reference cannot be resolved, the group will be simply discarded the same way as it is if an unknown group name is added to the previous example.

## The `Group` lifecycle

The following workflow is applied when a new `Group` resource is added to the cluster:

1. The GKO listens for `Group` resources.
2. The GKO resolves any references to external sources such as ConfigMaps or Secrets.
3. The GKO performs required changes, such as adding default settings.
4. The GKO converts the data to JSON format.
5. The GKO compares the definition to the existing definition. If something has changed, the GKO pushes the definition to the Management API.

Events are added to the resource as part of each action performed by the operator. To view these events, ensure that the CRD creation steps described above are completed, then run the following command:

```sh
kubectl describe -n gravitee group.gravitee.io developers
```

Example output:

```bash
Name:         developers
Namespace:    gravitee
[...]
Events:
  Type    Reason          Age   From                      Message
  ----    ------          ----  ----                      -------
  Normal  AddedFinalizer  73s   group-controller        Added Finalizer for the Group
  Normal  Creating        73s   group-controller        Creating Group
  Normal  Created         72s   group-controller        Created Group
```

{% hint style="info" %}
**For more information:**

* The `Group` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/group_types.go).
* The `Group` CRD API reference is documented [here](../../reference/api-reference.md).
{% endhint %}
