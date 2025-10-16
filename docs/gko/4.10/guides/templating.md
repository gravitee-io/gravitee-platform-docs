# Templating

## Overview

GKO's templating mechanism provides a flexible way to inject values from Kubernetes Secrets and ConfigMaps into CRDs at runtime. You can use the templating language to:

* Store and inject sensitive parameters into Gravitee resources via Kubernetes Secrets
* Externalize a configuration into Kubernetes ConfigMaps and inject the parameters into Gravitee resources

To use the templating feature, replace the value of string parameters in any Gravitee-managed CRD with the templating syntax. GKO will invoke the templated values at runtime.

This guide includes:

* [Using templates with Kubernetes Secrets](templating.md#use-kubernetes-secrets)
* [Using templates with Kubernetes ConfigMaps](templating.md#use-kubernetes-configmaps)
* [An example of using a Kubernetes Secret to inject a GitHub personal access token into an API definition resource](templating.md#pass-a-github-personal-access-token-to-an-api-definition-from-a-secret)

{% hint style="info" %}
Templating can only be used with parameters of type `string`.
{% endhint %}

## Use Kubernetes Secrets

The example below shows how to load the API name from a Kubernetes Secret into an API definition resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: my-api
spec:
  name: "[[ secret `api-definition-secret/api-name` ]]"
  ...
```

In the code above, `api-definition-secret` is the name of the Kubernetes Secret and `api-name` is the name of the Secret key.

You can create a Kubernetes Secret that matches this template with the following command:

```bash
kubectl create secret generic api-definition-secret --from-literal=api-name=my-api
```

At runtime, when GKO reconciles this API definition, it will execute the templating engine and inject the referenced value.

## Use Kubernetes ConfigMaps

The example below shows how to load the API name from a Kubernetes ConfigMap into an API definition resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: my-api
spec:
  name: "[[ configmap `api-definition-cm/api-name` ]]"
  ...
```

In the code above, `api-definition-cm` is the name of the Kubernetes ConfigMap and `api-name` is the name of the key.

You can create a Kubernetes ConfigMap that matches this template with the following command:

```bash
kubectl create configmap api-definition-cm --from-literal=api-name=my-api
```

At runtime, when GKO reconciles this API definition, it will execute the templating engine and inject the referenced value.

## Pass a GitHub personal access token to an API definition from a Secret

In this example, we want to include a documentation page in an API definition that is loaded dynamically using a GitHub fetcher. We'll load the documentation page from a private GitHub repository, so we'll need to provide a GitHub personal access token (PAT) in our API definition as part of the fetcher's configuration. Because this token is sensitive, we don't want to store it in the YAML file. Instead, we'll load it from a Kubernetes Secret.

First, select the private GitHub repository you'd like to use and create a personal access token that can read your GitHub repositories.

Now you can create an API definition that includes a GitHub page fetcher and uses templating to reference a Kubernetes Secret for the personal access token:

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

You can create a matching Kubernetes Secret with the following command (make sure to insert the value of your own personal access token):

```bash
k create secret generic http-github-fetcher --from-literal=pat=<YOUR-TOKEN>
```

When you create this API, it will dynamically load the README.md Markdown file from the referenced GitHub repository and add it to your API as a page. You can use the Gravitee API Management Console to make sure it was created successfully. You should see both the contents of the page (first screenshot) and the configuration of the doc fetcher (second screenshot):

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

## Disable templating

When you disable templating the following actions occur:

* GKO stops watching Secrets or ConfigMaps, potentially across all namespaces.
* Custom resources remain clean. The resources containing templates are not affected.

To disable templating, add the following configuration to your Helm chart:

```yaml
manager:
  templating:
    enabled: false
```

### Verification&#x20;

Use the following steps to verify that you disabled templating:&#x20;

1.  If a resource contains a templating placeholder check it is not replaced: \


    ```bash
    kubectl get apiv4definitions myapi -o yaml
    ```
2. Check the logs for errors. You should see no errors in the logs after the resource have been applied.&#x20;
