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
* The `Group` CRD API reference is documented [here](docs/gko/4.10/reference/api-reference.md).
{% endhint %}
