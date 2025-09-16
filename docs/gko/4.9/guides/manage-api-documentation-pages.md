---
description: Documentation pages can be defined in the API definition CRDs
---

# Manage API documentation pages

## Overview

The `ApiV4Definition` and `ApiDefinition` CRDs both allow documentation pages to be created alongside the API. Generally speaking, the CRDs support all of the documentation page types offered by Gravitee API Management: OpenAPI specifications (a.k.a. Swagger), AsyncAPI definitions, Markdown pages, AsciiDoc pages, and folders.

For page types other than folders, the pages can either be [referenced from an external source](manage-api-documentation-pages.md#referencing-external-pages-with-fetchers), such a web page or Git repo, using a fetcher (recommended), or [defined inline](manage-api-documentation-pages.md#inline-pages) in the YAML manifest. Referencing from an external source is recommended for two main reasons:

1. The YAML manifests can become unreadable with large inline documentation pages
2. The [default max value size](https://etcd.io/docs/v3.5/dev-guide/limit/) of etcd is set to 1.5MB, which could be surpassed with overly large manifests

Both v4 and v2 API CRDs share the same syntax for specifying documentation pages. This uses a `pages` attribute at the root of the spec:

```yaml
spec:
  pages:
    # [...]
```

{% hint style="info" %}
For APIs managed by GKO, you will not be able to add or modify documentation pages manually from the APIM Console.
{% endhint %}

In this guide, learn how to:

* [Reference external pages with fetchers](manage-api-documentation-pages.md#referencing-external-pages-with-fetchers)
* [Define inline pages](manage-api-documentation-pages.md#inline-pages)
* [Manage page access controls](manage-api-documentation-pages.md#documentation-page-access-controls)
* [Import multiple pages from a directory using a fetcher](manage-api-documentation-pages.md#using-a-fetcher-to-load-multiple-pages)

### Referencing external pages with fetchers

The recommended approach for embedding large documentation pages into APIs managed by Gravitee Kubernetes Operator is to use a fetcher to load the page from an external source. Supported sources are Git, Bitbucket, Github, Gitlab, and Web.

When an API definition resource containing a fetcher is created and pushed to Gravitee API Management, the platform automatically fetches the documentation pages and stores them as API assets in APIM. You can also optionally pass a cron expression to specify how often new fetches should be performed. This avoids the need to define large documentation pages inline in an API CRD, and also lets you manage the lifecycle of those documentation pages outside of the Gravitee platform.

Below is an example of a complete `ApiV4Definition` with an OAS documentation page referenced from an external HTTP source. This page is nested in a folder.

<pre class="language-yaml"><code class="lang-yaml">apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-with-swagger-http-fetcher
  namespace: gravitee
spec:
  contextRef: 
    name: "management-context-1"
  definitionContext:
    origin: KUBERNETES
    syncFrom: MANAGEMENT
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
<strong>          fetchCron: '*/10 * * * * *'
</strong></code></pre>

{% hint style="info" %}
The CRON syntax for page fetchers uses Spring scheduled tasks syntax, which includes six parameters, for example: `*/10 * * * * *`
{% endhint %}

{% hint style="warning" %}
Unix cron uses five parameters and will cause errors. An example of a Unix cron expression is `*/10 * * * *`
{% endhint %}

### Inline pages

Below is an example of a complete `ApiV4Definition` with an inline Markdown page. The page is nested in a folder.

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-with-markdown-page
  namespace: gravitee
spec:
  name: api-v4-with-markdown-page
  contextRef: 
    name: "management-context-1"
  definitionContext:
    origin: KUBERNETES
    syncFrom: MANAGEMENT
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

### Documentation page access controls

You can control the visibility of documentation pages for v2 and v4 APIs. `PUBLIC` means any non-connected user in the Developer Portal will see the page, while `PRIVATE` means any connected user can see the page. The default is `PUBLIC`.

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

The example below shows a documentation page SWAGGER fetcher that defines access controls:

```yaml
  pages:
    swagger:
      name: "pet-store"
      type: SWAGGER
      published: true
      visibility: PRIVATE
      source:
        type: 'http-fetcher'
        configuration:
          url: https://petstore.swagger.io/v2/swagger.json
      excludedAccessControls: false
      accessControls:
      - referenceId: "developers"
        referenceType: "GROUP"
```

In the above example, a group called `developers` is referenced in `accessControls`. `excludedAccessControls` is set to `false` (default), which means this group will be the only one allowed to view this page. If `excludedAccessControls` was set to **true**, this would mean that the `developers` group is excluded from accessing this page.

For an example of how to store secrets for accessing a private external source, such as a private Github repository, please refer to the [guide on templating](templating.md).

{% hint style="warning" %}
**Known limitation:** Referencing roles in access controls is not currently supported by GKO. We recommend using groups.
{% endhint %}

### Using a fetcher to load multiple pages

Gravitee API Management supports importing multiple documentation pages from a repository using a single fetcher (please refer to the APIM docs for more details). You can either replicate the repository's same file structure and naming in the Gravitee API's documentation section, or change the structure using the descriptor file described in the [guide on templating](templating.md).

{% hint style="warning" %}
Loading multiple files is only supported with the GitLab and GitHub fetchers.
{% endhint %}

GKO also supports this capability by defining a page of type `ROOT` that will point to a folder in a repository.

The below example illustrates this in an `ApiDefinition` resource:

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiDefinition"
metadata:
  name: "github-multifile-fetcher"
spec:
  name: "github-multifile-fetcher"
  contextRef:
    name: management-context-1
  version: "1"
  description: "fetch documentation pages from a github repository root"
  local: false
  pages:
    repository-root:
      type: "ROOT"
      published: true
      visibility: "PRIVATE"
      source:
        type: "github-fetcher"
        configuration:
          githubUrl: "https://api.github.com"
          owner: "jmcx"
          branchOrTag: "main"
          repository: "gko-multifile-doc-example"
          filepath: "/"
          username: "jmcx"
          personalAccessToken: "[[ secret `http-github-fetcher/pat` ]]"
          fetchCron: "5 * * * * *"
          autoFetch: true
      excludedAccessControls: true
      accessControls:
      - referenceId: "developers"
        referenceType: "GROUP"
  plans:
    - name: "KEY_LESS"
      description: "FREE"
      security: "KEY_LESS"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```

This single `ROOT` page configuration creates multiple documentation pages for the API. In this example, the public repository that is used contains a Markdown file and a Swagger file at the root, and each of which will create a new page.

All access control settings, such as `published`, `visibility`, `excludedAccessControls`, and `accessControl groups`**,** will be propagated to all created pages.
