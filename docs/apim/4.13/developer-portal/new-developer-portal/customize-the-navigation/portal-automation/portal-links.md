---
description: Declare links to external sites in the New Developer Portal navigation or under an API as code with the Automation API. Learn where each link appears and what is validated.
---

# Automate portal and API links

## Overview

A link is a navigation entry that opens a URL. It has no content of its own. A link belongs to a portal or to an API, and the endpoint you create it on decides which:

* A portal link appears in the portal's top navigation bar, at its `location` or at the top level.
* An API link belongs to an API and appears under the API wherever the API is listed, in every portal. Its `location` is resolved inside the API's own documentation tree, the one declared with `portalNavigation`. Without `location`, the link sits at the root of that tree.

A link can't move between a portal and an API, or between two portals or two APIs. To move a link, delete it and create it on the other endpoint.

| Property     | Description                                                                                                                                                  | Example                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| `hrid`       | Human-readable ID of the link. Required. It sets the link's segment in the navigation.                                                                        | `external-docs`            |
| `name`       | Display name of the link. Required.                                                                                                                          | `External Docs`            |
| `href`       | The URL the link opens. Required, and an absolute URL.                                                                                                       | `https://docs.example.com` |
| `location`   | Path in the navigation hierarchy where the link appears: a portal path for a portal link, or a `portalNavigation` path for an API link. Optional.           | `/projects/alpha`          |
| `order`      | Display order relative to siblings at the same location. Optional integer.                                                                                   | `1`                        |
| `visibility` | `PUBLIC` or `PRIVATE`. Optional. For more information, see [Visibility](README.md#visibility).                                                              | `PRIVATE`                  |

The request is validated before anything is stored. When a check fails, the response returns `400`, nothing changes, and the message is listed under `errors.severe`:

* `href` that isn't an absolute URL: `Provided url is invalid`.
* A portal link whose portal doesn't exist: `the portal to attach the link to does not exist in this environment`.
* A link whose segment is already used by another item under the same parent: `Link entry at [<location>] cannot be materialized: another item under the same parent already uses this path segment`.
* A public link under a private folder: `Parent item with id <id> must be PUBLIC to create a public child item.`

{% hint style="info" %}
When a link references a `location` that doesn't exist yet in the portal's navigation or in the API's documentation tree, the link is created as an orphan and reconnects when the folder appears. Apply order doesn't matter.
{% endhint %}

## Create a portal link

### Using the Automation API

1. Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/links` with the link specification.
2. Specify the link's HRID, display name, and URL, and optionally its location, order, and visibility.
3. Retrieve a link by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/links/{hrid}`.
4. Delete a link by sending a `DELETE` request to the same path.

**Example request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portals/{portalHrid}/links?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "external-docs",
  "name": "External Docs",
  "href": "https://docs.example.com",
  "location": "/projects/alpha",
  "order": 1,
  "visibility": "PUBLIC"
}
```
{% endcode %}

These endpoints require the `ENVIRONMENT_PORTAL` permission. For the full endpoint reference, see [Automation API endpoint reference](README.md#automation-api-endpoint-reference).

### Using Kubernetes CRDs

1. Define a `PortalLink` resource with a `portalRef` to the parent portal.
2. Specify the link's name and URL, and optionally its location, order, and visibility.
3. Apply the manifest with `kubectl apply -f portal-link.yaml`.

**Example PortalLink custom resource (portal-scoped):**

{% code title="portal-link.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: PortalLink
metadata:
  name: external-docs
  namespace: gravitee
spec:
  portalRef:
    name: default-portal
  name: "External Docs"
  href: "https://docs.example.com"
  location: /projects/alpha
  order: 1
```
{% endcode %}

### Using Terraform

Declare an [`apim_portal_link`](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/resources/portal_link) resource with the portal HRID, and the link's HRID, display name, and URL, and optionally its location, order, and visibility. Then run `terraform apply`.

**Example Terraform configuration:**

{% code title="portal-link.tf" %}
```hcl
resource "apim_portal_link" "external-docs" {
  portal_hrid = apim_portal.default-portal.hrid
  hrid        = "external-docs"
  name        = "External Docs"
  href        = "https://docs.example.com"
  location    = "/projects/alpha"
  order       = 1
  visibility  = "PUBLIC"
}
```
{% endcode %}

## Create an API link

### Using the Automation API

1. Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/links` with the link specification.
2. Specify the link's HRID, display name, and URL, and optionally its location relative to the API's documentation tree, order, and visibility.
3. Retrieve a link by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/apis/{apiHrid}/links/{hrid}`.
4. Delete a link by sending a `DELETE` request to the same path.

**Example request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/apis/pets-api/links?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "status-page",
  "name": "Status page",
  "href": "https://status.example.com",
  "location": "/docs",
  "order": 2
}
```
{% endcode %}

These endpoints require the `API_DOCUMENTATION` permission. For the full endpoint reference, see [Automation API endpoint reference](README.md#automation-api-endpoint-reference).

### Using Kubernetes CRDs

1. Define a `PortalLink` resource with an `apiRef` to the parent API.
2. Specify the link's name and URL, and optionally its location relative to the API's documentation tree, order, and visibility.
3. Apply the manifest with `kubectl apply -f api-link.yaml`.

**Example PortalLink custom resource (API-scoped):**

{% code title="api-link.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: PortalLink
metadata:
  name: pets-api-status-page
  namespace: gravitee
spec:
  apiRef:
    name: pets-api
    kind: ApiV4Definition
  name: "Status page"
  href: "https://status.example.com"
  location: /docs
  order: 2
```
{% endcode %}

{% hint style="warning" %}
**Constraints:**

* A `PortalLink` sets exactly one of `portalRef` and `apiRef`. A resource that sets both, or neither, is rejected.
* `portalRef` and `apiRef` are immutable after creation. A link can't be moved to a different portal or API.
* Only v4 APIs are supported. The `kind` of `apiRef` defaults to `ApiV4Definition` when omitted, and any other kind is rejected.
* The referenced `Portal` or `ApiV4Definition` carries the management context the link is synced with, so it needs a `contextRef`.
* The GKO admission webhook validates the link before apply using the `dryRun` endpoint.
* A `Portal` referenced by a `PortalLink` can't be deleted until the link is removed.
{% endhint %}

### Using Terraform

Declare an [`apim_api_link`](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/resources/api_link) resource with the API HRID, and the link's HRID, display name, and URL, and optionally its location relative to the API's documentation tree, order, and visibility. Then run `terraform apply`.

**Example Terraform configuration:**

{% code title="api-link.tf" %}
```hcl
resource "apim_api_link" "pets-api-status-page" {
  api_hrid = apim_apiv4.pets-api.hrid
  hrid     = "status-page"
  name     = "Status page"
  href     = "https://status.example.com"
  location = "/docs"
  order    = 2
}
```
{% endcode %}
