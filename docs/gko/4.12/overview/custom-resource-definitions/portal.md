# Portal

The `Portal` custom resource declares a next-gen Developer Portal instance bound to an environment. It manages the portal's name, navigation hierarchy, and top-level folder structure through the Automation API.

## Overview

A Portal resource defines the desired state of a Developer Portal, including its navigation tree. The GKO controller reconciles this resource by calling the Automation API's portal endpoints. Admission webhooks validate the resource before apply using the `dryRun` endpoint.

In APIM 4.12, only one portal instance is supported per environment. All portal operations must target the HRID `default-portal`. Multi-portal support is planned for a future release.

## Example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Portal
metadata:
  name: default-portal
  namespace: gravitee
spec:
  contextRef:
    name: "apim-context"
  name: "Default Portal"
  navigation:
    - path: /projects/alpha
      displayName: Alpha
      order: 1
    - path: /projects/alpha/docs
    - path: /projects/beta
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.contextRef` | Reference to a `ManagementContext` resource |
| `spec.name` | Display name of the portal |
| `spec.navigation` | Array of navigation path entries defining the folder hierarchy |
| `spec.navigation[].path` | Slash-separated path, starting with `/` |
| `spec.navigation[].displayName` | Human-friendly label for the navigation node (optional) |
| `spec.navigation[].order` | Display order relative to siblings (optional) |

## Validation

Navigation paths must:

* Start with `/`
* Not contain `//` or `..`
* Not end with `/` (except root)

Intermediate folders not listed explicitly are created automatically.

{% hint style="info" %}
For full usage documentation, including Automation API examples and navigation path normalization, see the [Portal automation](https://documentation.gravitee.io/apim/4.12/developer-portal/new-developer-portal/customize-the-navigation/portal-automation) guide.
{% endhint %}
