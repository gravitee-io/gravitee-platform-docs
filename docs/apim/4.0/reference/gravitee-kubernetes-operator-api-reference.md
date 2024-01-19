# Gravitee Kubernetes Operator API Reference

## Overview

The Gravitee Kubernetes Operator (GKO) API reference documentation is automatically generated and updated in the [GKO repository](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/docs/api). As of Gravitee 4.2, there are two active versions:

* [GKO 0.x.x CRD reference (deprecated)](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/docs/api/reference.md)
* [GKO 1.x.x CRD reference](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/beta/docs/api/reference.md)

### Comparison table

<table><thead><tr><th width="313.66666666666663">Supported</th><th data-type="checkbox">GKO 0.x.x</th><th data-type="checkbox">GKO 1.x.x</th></tr></thead><tbody><tr><td><a href="../overview/gravitee-api-definitions-and-execution-engines/reactive-execution-engine.md">Legacy execution engine</a> (v2 APIs)</td><td>true</td><td>true</td></tr><tr><td><a href="../overview/gravitee-api-definitions-and-execution-engines/reactive-execution-engine.md">Reactive execution engine</a> (v4 APIs)</td><td>false</td><td>true</td></tr><tr><td><a href="../guides/gravitee-kubernetes-operator/custom-resource-definitions/apidefinition-crd.md"><code>ApiDefintion</code></a></td><td>true</td><td>true</td></tr><tr><td><a href="../guides/gravitee-kubernetes-operator/custom-resource-definitions/apiresource-crd.md"><code>ApiResource</code></a></td><td>true</td><td>true</td></tr><tr><td><a href="../guides/gravitee-kubernetes-operator/custom-resource-definitions/application-crd.md"><code>Application</code></a></td><td>true</td><td>false</td></tr><tr><td><a href="../guides/gravitee-kubernetes-operator/custom-resource-definitions/managementcontext-resource.md"><code>ManagementContext</code></a></td><td>true</td><td>false</td></tr><tr><td><a href="../guides/gravitee-kubernetes-operator/gravitee-as-an-ingress-controller.md">Gravitee Ingress</a></td><td>true</td><td>true</td></tr><tr><td>Import <code>ApiDefinition</code> into APIM</td><td>true</td><td>false</td></tr></tbody></table>

## CRD references

### GKO 0.x.x

The [GKO 0.x.x CRD reference](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/docs/api/reference.md) is compatible with the legacy execution engine (v2 APIs) only and has been deprecated. It supports the `ApiDefinition`, `ApiResource`, `Application`, and `ManagementContext` resources, as well as the Gravitee Ingress. The `ApiDefinition` can be imported into APIM.

### GKO 1.x.x

The [GKO 1.x.x CRD reference](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/beta/docs/api/reference.md) is a newer version of the GKO 0.x.x CRD reference that is compatible with both the legacy and reactive execution engines to support both v2 and v4 APIs. It also supports the `ApiDefinition` and `ApiResource` resources and the Gravitee Ingress.&#x20;

Due to a missing endpoint, the `ManagementContext`, and therefore `Application`, resources are not supported, and `ApiDefinition` cannot be imported into APIM.&#x20;

Planned enhancements will promote `ManagementContext` and `Application` to GKO 1.x.x and enable support for importing `ApiDefintion`.

Refer to the [GKO 1.x.x changelog](https://github.com/gravitee-io/gravitee-kubernetes-operator/releases/tag/1.0.0-beta.1) to track breaking changes.
