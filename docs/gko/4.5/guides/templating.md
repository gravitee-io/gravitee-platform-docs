---
description: Overview of Templating.
---

# Templating

## Overview

GKO has a templating mechanism that provides a flexible way to inject values into CRDs at runtime from Kubernetes secrets and configMaps. You can use this language to do things like:

* Use Kubernetes secrets to store and inject sensitive parameters into Gravitee resources
* Externalise configuration into Kubernetes configMaps and inject the parameters into Gravitee resources

To use this feature, you can use the templating syntax in place of the value of string parameters in any Gravitee-managed CRD, and GKO will instantiate the templated values at runtime.

This guide includes the following topics:

* [Using templates with Kubernetes secrets](templating.md#use-kubernetes-secrets)
* [Using templates with Kubernetes configMaps](templating.md#use-kubernetes-configmaps)
* [Example of using a Kubernetes secret to inject a GitHub personal access token into an API definition resource](templating.md#pass-a-github-personal-access-token-to-an-api-definition-from-a-secret)

{% hint style="info" %}
Templating only works for parameters of type `string`.
{% endhint %}

## Use Kubernetes secrets

The example below shows how to load the API name from a Kubernetes secret in an API definition resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: my-api
spec:
  name: "[[ secret `api-definition-secret/api-name` ]]"
  ...
```

In this example, `api-definition-secret` is the name of the Kubernetes secret, `api-name` is the name of the secret key.

You can create a Kubernetes secret that matches this template with the following example command:

```bash
kubectl create secret generic api-definition-secret --from-literal=api-name=my-api
```

At runtime, when GKO reconciles this API definition, it will execute the templating engine and inject the referenced value.

## Use Kubernetes configMaps

The example below shows how to load the API name from a Kubernetes configMap in an API definition resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: my-api
spec:
  name: "[[ configmap `api-definition-cm/api-name` ]]"
  ...
```

In this example, `api-definition-cm` is the name of the Kubernetes configMap, `api-name` is the name of the key.

You can create a Kubernetes configMap that matches this template with the following example command:

```bash
kubectl create configmap api-definition-cm --from-literal=api-name=my-api
```

At runtime, when GKO reconciles this API definition, it will execute the templating engine and inject the referenced value.

## Pass a GitHub personal access token to an API definition from a secret

In this example, we want to include a documentation page as part of an API definition that is loaded dynamically using a GitHub fetcher. We'll load the documentation page from a private GitHub repository, so we'll need to provide a GitHub personal access token (PAT) in our API definition as part of the fetcher's configuration. Because this token is sensitive, we don't want to store it in the yaml file but want to instead load it from a Kubernetes secret.

First of all, pick a private GitHub repository you'd like to use and create a personal access token that can read your GitHub repositories.

Now you can create an API definition that includes a GitHub page fetcher, and that uses templating to reference a Kubernetes secret for the personal access token:

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiDefinition"
metadata:
  name: "gko-doc-fetcher-api"
spec:
  name: "GitHub doc fetcher example"
  contextRef:
    name: management-context-1
    namespace: default
  version: "0.1.0"
  description: "An API that fetches its docs from a private GitHub repository."
  pages:
    gitHubMarkdownPage:
      name: "My fetched markdown page"
      type: "MARKDOWN"
      source:
        type: "github-fetcher"
        configuration:
          githubUrl: "https://api.github.com"
          owner: "jmcx"
          repository: "am_lambda_authorizer"
          filepath: "README.md"
          username: "jmcx"
          personalAccessToken: "[[ secret `http-github-fetcher/pat` ]]"
  proxy:
    virtual_hosts:
    - path: "/my-docs-fetcher-api/"
    groups:
    - name: "default-group"
      endpoints:
      - name: "default"
        target: "https://corporatebs-generator.sameerkumar.website/"
        type: "http"
```

You can create a matching Kubernetes secret with the following command, make sure to insert the value of your own personal access token:

```bash
k create secret generic http-github-fetcher --from-literal=pat=<YOUR-TOKEN>
```

Now when you create this API, it will dynamically load the README.md markdown file from the referenced GitHub repository, and add it as a page in your API. You can check in the Gravitee API Management console to make sure it was created successfully. You'll see both the contents of the page (first screenshot) as well as the configuration of the doc fetcher (second screenshot):

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>
