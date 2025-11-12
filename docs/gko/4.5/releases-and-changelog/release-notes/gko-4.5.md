# GKO 4.5

## Gravitee Kubernetes Operator 4.5 release notes

With the release of Gravitee 4.5, we have pushed some important updates to the Gravitee Kubernetes Operator (GKO):

* New admission webhook that provides immediate feedback about syntactic or semantic problems in Gravitee resources before they are reconciled.
* For more complete functionality, simplicity, and consistency, we have updated the Application CRD, which includes breaking changes.&#x20;
* Updates to how primary owners are handled by GKO.
* In the contextRef attribute that references a ManagementContext from a Gravitee resource, Namespace becomes optional.
* Improved compatibility with ArgoCD & FluxCD

{% hint style="info" %}
GKO 4.5 must be used with APIM 4.5.
{% endhint %}

## New admission webhook

We have improved the developer experience for GKO users. With this update, GKO provides more detailed feedback about configuration issues in your APIs, and it provides that feedback earlier in the process.

We have implemented many other checks to all five supported CRDs that either cause the operation to fail or simply warn you of potential issues. You receive this feedback directly from kubectl, or in the logs of your CI/CD tool.&#x20;

Here are some other examples of validation checks that GKO perform with this update:

* Returns an error if an API includes a **context path** that is already used by another API in the same environment.
* Returns a warning if an API references a member, group, or category does not exist in API Management (APIM).
* Returns a warning if an API has no plans because if there is no plan, the API cannot be deployed or invoked on the gateway.
* Returns an error you if try to set an API's state to `started` and it has no plans.
* returns an error if the credentials provided to a Management Context are not valid.
* Returns an error if the API is missing any required parameters.
* Returns an error if you try to change the **type** of an application using the Application CRD.

To complete these validation checks, we have implemented an admission webhook for GKO,. The webhook validates any desired configuration changes before they are applied. We can now perform syntactic and semantics validation of your resources.

## Updated Application CRD

With this update, GKO's Application CRD is ready for widespread adoption.

We have made changes, which include breaking changes, to future proof this CRD for the next set of GKO improvements, including the upcoming addition of a Subscription CRD.&#x20;

We have made the following improvements:

* Added members support for the Application CRD
* GKO-managed applications are now read-only in APIM
* More consistent attribute names for the CRD
* Removed unnecessary parameters from the CRD

## Changes to primary owner management with GKO

Before this update, the primary owner of the APIs in Gravitee API Management (APIM) could transfer the ownership of the API from one user to another. You completed this action with GKO, which cause problems for users.

With this update, you cannot change the primary owner of the API with GKO. If you convert a UI-managed API into a GKO-managed API by exporting the CRD, and then applying it to the same environment, the primary ownership of the API changes to the account used by the GKO. To complete this action, use a service sccount. For more information about service accounts, see [Define an APIM service account for GKO](docs/gko/4.5/guides/define-an-apim-service-account-for-gko.md).

## Optional namespace in contextRef

Before this update, when referencing a Management Context from an API or Application CRD, you had to provide a namespace name even if the resource was in the same namespace as the Management Context. Here is an example:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
spec:
  name: "GKO Basic"
  version: "1.1"
  contextRef:
    name: "management-context-1"
    namespace: gravitee
  ...
```

With this update, this namespace reference is optional, and the namespace used in the current context Kubernetes is  used by the operator. Here is an example:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: basic-api-example
spec:
  name: "GKO Basic"
  version: "1.1"
  contextRef:
    name: "management-context-1"
  ...
```
