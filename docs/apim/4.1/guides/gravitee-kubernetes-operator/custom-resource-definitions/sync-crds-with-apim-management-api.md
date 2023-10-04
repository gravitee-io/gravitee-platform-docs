# Sync CRDs with API Management API

## How to synchronize your API CRDs with an existing Management API

The following examples of creating a Management Context custom resource and an API referencing it assume that a Management API has already been deployed in a namespace called `apim-example`. The connection to that Management API uses the default in-memory credentials.

### Example: Creating a Management Context resource for an existing Management API

```sh
cat <<EOF | kubectl apply -f -
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: apim-example-context
  namespace: apim-example
spec:
  baseUrl: http://acme-apim3-api.apim-example.svc:83
  environmentId: DEFAULT
  organizationId: DEFAULT
  auth:
    credentials:
      username: admin
      password: admin
EOF
```

### Example: Creating an API referencing an existing Management Context resource

```sh
cat <<EOF | kubectl apply -f -
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
  namespace: apim-example
spec:
  name: gko-example
  contextRef:
    name: apim-example-context
    namespace: apim-example
  version: "1.0.0"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
EOF
```

{% hint style="warning" %}
By default, the service account created for the Gateway does not have a cluster role. Therefore, to sync a CRD with a Management API:

* Your definitions must sit in the same namespace (e.g., `apim-example`)
* The name of the context must match the reference in the API definition (e.g., the names of `ManagementContext` and `contextRef` above are both`apim-example-context`)

Alternatively, you can configure the [Helm Chart](../../../getting-started/install-guides/install-on-kubernetes/configure-helm-chart.md) to use a custom role.
{% endhint %}

## Using an APIM export endpoint to create an API definition from an existing API

The Management API feature provides an [export endpoint](https://docs.gravitee.io/apim/3.x/management-api/3.20/index.html#tag/APIs/operation/exportApiCRD) that allows you to export an API as an API Definition resource.

This allows you to easily create an API Definition from a given environment by calling the endpoint and piping the result to a `kubectl` command. For example:

{% code overflow="wrap" %}
```sh
curl -s -H "Authorization: Bearer $TOKEN" "https://apim-example-api.team-gko.gravitee.xyz/management/organizations/DEFAULT/environments/DEFAULT/apis/$API_ID/crd" | kubectl apply -f -
```
{% endcode %}

## Starting and stopping your API

By default, the API will start automatically. To stop it (or just create an API definition in "stop mode"), set the `state` property value to `STOPPED`:

```sh
cat <<EOF | kubectl apply -f -
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
  namespace: apim-example
spec:
  name: gko-example
  contextRef:
    name: apim-example-context
    namespace: apim-example
  version: "1.0.0"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  state: "STOPPED"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
EOF
```

To start the API again, change the `state` property value back to `STARTED`.

## Updating your API

Follow the example below to update the API name, path, and endpoint target of the API:

```sh
cat <<EOF | kubectl apply -f -
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
  namespace: apim-example
spec:
  name: gko-example-updated
  contextRef:
    name: apim-example-context
    namespace: apim-example
  version: "1.0.0"
  description: "Basic api managed by Gravitee Kubernetes Operator"
  proxy:
    virtual_hosts:
      - path: "/k8s-basic-updated"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/whattimeisit"
EOF
```

## Deleting your API

The following executes a simple deletion of the API definition:

```sh
kubectl -n apim-example delete apidefinitions.gravitee.io basic-api-example
```
