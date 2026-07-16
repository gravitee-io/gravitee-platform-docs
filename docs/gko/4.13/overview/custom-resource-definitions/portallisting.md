# PortalListing

The `PortalListing` custom resource publishes one or more APIs to specific locations in a portal's navigation tree. Each listing references a parent portal and an array of API entries with target locations and display order.

## Overview

A PortalListing resource declares which APIs appear at which locations in the portal navigation. The GKO controller reconciles this resource by calling the Automation API's listing endpoints. On apply, API entries are materialized in the portal's navigation tree. On delete, all navigation entries owned by the listing are removed.

## Example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: PortalListing
metadata:
  name: alpha-apis
  namespace: gravitee
spec:
  portalRef:
    name: default-portal
  apis:
    - ref:
        name: pets-api
        kind: ApiV4Definition
      location: /projects/alpha
      order: 1
    - ref:
        name: orders-api
      location: /projects/alpha
      order: 2
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.portalRef` | Reference to the parent `Portal` resource. Immutable after creation. |
| `spec.apis` | Array of API entries to publish |
| `spec.apis[].ref` | Reference to an `ApiV4Definition` resource. `kind` defaults to `ApiV4Definition` when omitted. |
| `spec.apis[].location` | Path in the portal's navigation where the API appears |
| `spec.apis[].order` | Display order relative to siblings at the same location (optional) |

## Validation

The GKO admission webhook validates that:

* All referenced APIs resolve to existing `ApiV4Definition` resources in the cluster
* All referenced APIs share the portal's management context
* Only v4 APIs are referenced
* Deletion is blocked when portals or APIs are referenced by active listings

{% hint style="info" %}
For full usage documentation, including Automation API examples, see the [Portal automation](https://documentation.gravitee.io/apim/4.12/developer-portal/new-developer-portal/customize-the-navigation/portal-automation) guide.
{% endhint %}
