---
description: Portal-scoped documentation pages provide platform-level guides in the Developer Portal 4.13. Learn how each page is attached.
---

# Portal documentation

## Create portal documentation

Portal-scoped documentation pages provide platform-level guides and reference material. Each page attaches to a portal and appears at a specified location in the portal's navigation hierarchy, or serves as the portal's homepage. A page declares where it appears with `area`, and who sees it with `visibility`.

{% hint style="info" %}
When a documentation page references a `location` that does not exist yet in the portal's navigation, the page is created as an orphan and reconnects when the folder appears. Apply order does not matter.
{% endhint %}

{% hint style="warning" %}
`visibility` takes `PUBLIC` or `PRIVATE`. A page that omits it takes the visibility of its folder on every apply, including a page that was made private in the Console. Declare `visibility: PRIVATE` on every page that stays private. For more information, see [Visibility](README.md#visibility).
{% endhint %}

### Using the Automation API

1. Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations` with the documentation specification.
2. Specify the page's HRID, display name, type (Gravitee Markdown, OpenAPI, or AsyncAPI), content, location, and optionally its order, area, and visibility.
3. Retrieve a documentation page by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}`.
4. Delete a documentation page by sending a `DELETE` request to the same path.

**Example request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "getting-started",
  "name": "Getting Started",
  "type": "GRAVITEE_MARKDOWN",
  "content": "# Getting Started\nWelcome to the developer portal.",
  "location": "/projects/alpha",
  "order": 1,
  "visibility": "PUBLIC"
}
```
{% endcode %}

When `dryRun` validation fails, the response returns the errors under the `errors` field. The validation messages are:

| Field | Constraint | Validation message |
|:------|:-----------|:-------------------|
| `name` | Required | `name must not be blank` |
| `type` | Required: `GRAVITEE_MARKDOWN`, `OPENAPI`, or `ASYNCAPI` | `type must not be null` |
| `content` | Required | `content must not be null` |

When the portal navigation is re-synced, automation-managed portal documentation is updated to reflect parent folder changes.

For the full endpoint reference, see [Automation API endpoint reference](README.md#automation-api-endpoint-reference).

### Using Kubernetes CRDs

1. Define a `Documentation` resource with a reference to the parent portal.
2. Specify the page's name, type, content, location, and optionally its order, area, and visibility.
3. Apply the manifest with `kubectl apply -f portal-documentation.yaml`.

**Example Documentation custom resource (portal-scoped):**

{% code title="portal-documentation.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Documentation
metadata:
  name: getting-started
  namespace: gravitee
spec:
  name: "Getting Started"
  type: GRAVITEE_MARKDOWN
  content: |
    # Getting Started
    Welcome to the developer portal.
  portalRef:
    name: default-portal
  location: /projects/alpha
  order: 1
```
{% endcode %}

{% hint style="warning" %}
**Constraints:**

* The `portalRef` field is immutable after creation. Documentation cannot be moved to a different portal.
* Documentation cannot be reassigned from a portal to an API, or from an API to a portal, after creation.
* The GKO admission webhook validates the documentation before apply.
{% endhint %}

## Set the portal homepage

A portal page with `area: HOMEPAGE` is the homepage of the portal. The homepage isn't part of the navigation, so it takes no `location`. A portal has one homepage: applying the page replaces the homepage that was created in the Console or seeded with the environment, and a second automation-managed homepage with a different HRID fails with `409` and the message `Homepage already exists`, on an apply and on a dry run. Changing the `area` of an existing page removes its navigation entry and creates a new one in the target area. When you delete the homepage, consumers who open the portal land on the catalog.

To write the homepage in the Console instead, see [Customize the Homepage](../../customize-the-homepage.md).

### Using the Automation API

Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations` with `area` set to `HOMEPAGE`.

**Example request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "home",
  "name": "Home",
  "type": "GRAVITEE_MARKDOWN",
  "content": "# Welcome\nThis page is the developer portal homepage.",
  "area": "HOMEPAGE"
}
```
{% endcode %}

### Using Kubernetes CRDs

Define a `Documentation` resource with `area: HOMEPAGE` and a reference to the portal, and then apply it with `kubectl apply -f portal-homepage.yaml`.

**Example Documentation custom resource (homepage):**

{% code title="portal-homepage.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Documentation
metadata:
  name: portal-homepage
  namespace: gravitee
spec:
  name: "Home"
  type: GRAVITEE_MARKDOWN
  content: |
    # Welcome

    This page is the developer portal homepage.
  portalRef:
    name: default-portal
  area: HOMEPAGE
```
{% endcode %}
