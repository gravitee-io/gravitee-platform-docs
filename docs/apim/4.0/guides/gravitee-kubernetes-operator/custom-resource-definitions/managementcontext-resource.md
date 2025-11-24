---
description: Tutorial on ManagementContext Resource.
---

# ManagementContext Resource

## How to use the Management Context (`ManagementContext`) custom resource

To enable the synchronization of CRDs with a remote Management API, you need to create a Management Context custom resource that refers to an existing [organization and environment](../../administration/administering-organizations-and-environments.md).

You can create multiple Management Context custom resources, each targeting a specific environment and defined in a specific organization of a Management API instance.

A Management Context custom resource can authenticate to your Management API instance via either basic authentication or a bearer token. Authentication credentials may either be added inline in the Management Context CRD or referenced from a Kubernetes Secret.

{% hint style="info" %}
If both credentials and a bearer token are defined in your custom resource, the bearer token will take precedence.
{% endhint %}

## Examples

The custom resource created in the example below refers to a Management API instance exposed at `https://gravitee-api.acme.com`. It targets the `dev` environment of the `acme` organization using the `admin` account and basic authentication credentials defined in a Kubernetes Secret. To achieve this:

Create a Secret to store the credentials:

```sh
kubectl create secret generic management-context-credentials \
  --from-literal=username=admin \
  --from-literal=password=admin \
  --namespace graviteeio
```

Define a Management Context custom resource referencing the Secret:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: apim-example-context
  namespace: graviteeio
spec:
  baseUrl: https://gravitee-api.acme.com
  environmentId: dev
  organizationId: acme
  auth:
    secretRef:
      name: management-context-credentials
```

If no namespace has been specified for the Secret reference, the Management Context resource namespace will be used to resolve the Secret.

{% hint style="info" %}
To target another environment on the same API instance, add and configure another Management Context resource.
{% endhint %}

Although Kubernetes Secrets should be the preferred way to store credentials, you can also add credentials inline in the Management Context custom resource definition:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: apim-example-context
  namespace: graviteeio
spec:
  baseUrl: https://gravitee-api.acme.com
  environmentId: dev
  organizationId: acme
  auth:
    credentials:
      username: admin
      password: admin
```

The example below uses a `bearerToken` to authenticate the requests. Note that the token must have been generated for the admin account beforehand:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: apim-example-context
spec:
  baseUrl: https://gravitee-api.acme.com
  environmentId: staging
  organizationId: acme
  auth:
    bearerToken: xxxx-yyyy-zzzz
```

Alternatively, here is how to use a Kubernetes secret to store the token:

```sh
kubectl create secret generic management-context-credentials \
  --from-literal=bearerToken=xxxx-yyyy-zzzz \
  --namespace graviteeio
```

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: apim-example-context
spec:
  baseUrl: https://gravitee-api.acme.com
  environmentId: staging
  organizationId: acme
  auth:
    secretRef:
      name: management-context-credentials
```
