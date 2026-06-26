# Documentation

The `Documentation` custom resource creates documentation pages for the next-gen Developer Portal. Pages can be scoped to a portal (platform-level guides) or to an API (API-specific reference material). Supported content types are Gravitee Markdown, OpenAPI, and AsyncAPI.

## Overview

A Documentation resource declares the desired state of a documentation page. The GKO controller reconciles this resource by calling the Automation API's documentation endpoints. Portal-scoped pages appear at the specified location in the portal's navigation. API-scoped pages appear under every published instance of the referenced API.

## Portal-scoped documentation example

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

## API-scoped documentation example

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Documentation
metadata:
  name: pets-api-overview
  namespace: gravitee
spec:
  name: "API Overview"
  type: GRAVITEE_MARKDOWN
  content: |
    # Pets API
    This API manages pet records.
  apiRef:
    name: pets-api
    kind: ApiV4Definition
  location: /docs
  order: 1
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.name` | Display name of the documentation page |
| `spec.type` | Content type: `GRAVITEE_MARKDOWN`, `OPENAPI`, or `ASYNCAPI` |
| `spec.content` | Content of the documentation page |
| `spec.portalRef` | Reference to a `Portal` resource (for portal-scoped docs). Mutually exclusive with `apiRef`. |
| `spec.apiRef` | Reference to an `ApiV4Definition` resource (for API-scoped docs). Mutually exclusive with `portalRef`. |
| `spec.location` | Path in the navigation hierarchy where the page appears (optional) |
| `spec.order` | Display order relative to siblings at the same location (optional) |

## Constraints

* `portalRef` and `apiRef` are immutable after creation. Documentation cannot be moved between portals and APIs.
* Only v4 APIs are supported for API-scoped documentation.
* An API referenced by active documentation pages cannot be deleted until those pages are removed.

{% hint style="info" %}
For full usage documentation, including Automation API examples and validation messages, see the [Portal automation](https://documentation.gravitee.io/apim/4.12/developer-portal/new-developer-portal/customize-the-navigation/portal-automation) guide.
{% endhint %}
