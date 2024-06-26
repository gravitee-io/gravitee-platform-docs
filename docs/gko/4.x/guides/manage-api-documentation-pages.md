---
description: Documentation pages can be defined in the API definition CRDs
---

# Manage API documentation pages

## Overview

The `ApiV4Definition` and `ApiDefinition` CRDs both support the definition of documentation pages to be created along with the API. Generally speaking, the CRDs support all the documentation page types supported by Gravitee API Management:

* OpenAPI specifications (OAS), a.k.a. Swagger
* AsyncAPI definitions
* Markdown pages
* Asciidoc pages
* Folders

For page types other than folders, the pages can either be:

* [referenced from an external source](manage-api-documentation-pages.md#referencing-external-pages-with-fetchers), such a web page or Git repo, using a fetcher (recommended)
* [defined inline](manage-api-documentation-pages.md#inline-pages) in the yaml manifest

Both v4 and v2 API CRDs share the same syntax for specifying doc pages using a **pages** attribute at the root of the spec.&#x20;

```yaml
spec:
  pages:
    # [...]
```

{% hint style="info" %}
For APIs managed by GKO, you will not be able to add or modify documentation pages manually from the API management console&#x20;
{% endhint %}

## Referencing external pages with fetchers

The recommended approach for embedding large documentation pages into APIs managed by Gravitee Kubernetes Operator is to use a fetcher to load the page from an external source. Supported sources are Git, Bitbucket, Github, Gitlab, and Web.&#x20;

When an API definition resource containing a fetcher is created an pushed to Gravitee API Management, the platform will automatically fetch the documentation pages and store them as part of that API in APIM. You can also optionally pass a cron expression to determine how often new fetches should be performed. This avoids the need to define large documentation pages inline in an API CRD, and also provides the possibility to manage the lifecycle of those documentation pages outside of the Gravitee platform.&#x20;

Below is an example of a complete `ApiV4Definition` with an OAS documentation page referenced from an external http source, this page is nested in a folder:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-with-swagger-http-fetcher
  namespace: gravitee
spec:
  contextRef:
    name: dev-ctx
    namespace: gravitee
  name: api-with-swagger-http-fetcher
  version: 1.0
  description: An API V4 with a simple markdown page
  type: PROXY
  state: STARTED
  listeners:
    - type: HTTP
      paths:
        - path: /api-v4-with-swagger-http-fetcher
      entrypoints:
        - type: http-proxy
          qos: AUTO
  endpointGroups:
    - name: Default HTTP proxy group
      type: http-proxy
      endpoints:
        - name: Default HTTP proxy
          type: http-proxy
          inheritConfiguration: false
          configuration:
            target: https://api.gravitee.io/echo
          secondary: false
  flowExecution:
    mode: DEFAULT
    matchRequired: false
  plans:
    KeyLess:
      name: Free plan
      description: This plan does not require any authentication
      security:
        type: KEY_LESS
  pages:
    docs-folder:
      name: specifications
      type: FOLDER  
    swagger:
      name: pet-store
      type: SWAGGER
      parent:  docs-folder
      source:
        type: http-fetcher
        configuration:
          url: https://petstore.swagger.io/v2/swagger.json
          fetchCron: '0 1 * * *'
```

## Inline pages

Below is an example of a complete `ApiV4Definition` with an inline markdown page, the page is nested in a folder:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-with-markdown-page
  namespace: gravitee
spec:
  name: api-v4-with-markdown-page
  version: 1.0
  description: An API V4 with a simple markdown page
  type: PROXY
  state: STARTED
  listeners:
    - type: HTTP
      paths:
        - path: /api-v4-with-markdown-page
      entrypoints:
        - type: http-proxy
          qos: AUTO
  endpointGroups:
    - name: Default HTTP proxy group
      type: http-proxy
      endpoints:
        - name: Default HTTP proxy
          type: http-proxy
          inheritConfiguration: false
          configuration:
            target: https://api.gravitee.io/echo
          secondary: false
  flowExecution:
    mode: DEFAULT
    matchRequired: false
  plans:
    KeyLess:
      name: Free plan
      description: This plan does not require any authentication
      security:
        type: KEY_LESS
  pages:
    markdowns-folder:
      name: markdowns
      type: FOLDER
    markdown:
      name: hello-markdown
      type: MARKDOWN
      parent: markdowns-folder
      content: |
        Hello world!
        --
        This is markdown.
```

## Documentation page access controls

For v2 and v4 APIs, you can control the visibility of documentation pages, `PUBLIC` means any non-connected user in the portal will see the page, `PRIVATE` means any connected user can see the page. The default is `PUBLIC`.

```yaml
pages:
  markdown:
    name: hello-markdown
    type: MARKDOWN
    parent: markdowns-folder
    visibility: PUBLIC
    content: |
      Hello world!
      --
      This is markdown.
```

For v2 APIs, you can also [define access control settings](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/docs/api/reference.md#apidefinitionspecpageskeyaccesscontrolsindex) to determine which groups of users can or cannot access the documentation page.

