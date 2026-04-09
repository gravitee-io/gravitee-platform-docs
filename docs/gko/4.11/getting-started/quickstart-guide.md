# Quickstart Guide

## Overview

Following this quickstart guide or the video tutorial is the fastest way to start working with the Gravitee Kubernetes Operator (GKO). These resources describe how to complete the following actions:

* [#install-gko](quickstart-guide.md#install-gko "mention")
* [#create-a-managementcontext](quickstart-guide.md#create-a-managementcontext "mention")
* [#create-an-apidefinition](quickstart-guide.md#create-an-apidefinition "mention")

In this guide, we assume that Gravitee API Management is acting as the control plane for the Gravitee Gateway. The Gateway loads its APIs from APIM's repository (e.g., MongoDB, or via a Bridge Gateway in a hybrid setup). GKO lets you define and manage API's "as-code" rather than using the GUI. Additionally, GKO synchronizes all of its actions, such as creating APIs and managing their lifecycle, directly with Gravitee API Management through the Management API.

## Prerequisites

* A running instance of Gravitee API Management. It doesn't matter where this is running, so long as you have access to credentials that can be used to connect GKO to this APIM instance.
* A Kubernetes cluster on which to install GKO.

### Video tutorial: Installing GKO

{% embed url="https://youtu.be/QBAJ1xjDLyM?feature=shared" %}

## Install GKO

{% hint style="info" %}
For comprehensive deployment details, see the GKO Install Guide.
{% endhint %}

Use Helm to install GKO on your Kubernetes cluster:

{% code overflow="wrap" %}
```bash
helm repo add graviteeio https://helm.gravitee.io
helm install graviteeio-gko graviteeio/gko
```
{% endcode %}

## Create a `ManagementContext`

The `ManagementContext` CRD is used to provide GKO with everything needed to invoke an APIM instance's Management API.

The configuration depends on your deployment type:

{% tabs %}
{% tab title="Self-Hosted APIM" %}
**Prerequisites**

To fill out the CRD correctly, you'll need:

* The APIM management API URL
* Credentials to authenticate GKO with the Management API

If you're running APIM locally, you can use the default admin account to authenticate (user: `admin`, password: `admin`).

Alternatively, you can head to your APIM instance and create a dedicated service account and token for GKO to use. Make sure to copy the token value to use in the step below.

**Configuration**

Create a file called `management-context-1.yaml` with the following contents:

**Option 1: Using a Bearer Token (Recommended)**

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: "management-context-1"
spec:
  baseUrl: <APIM management API URL>
  environmentId: DEFAULT
  organizationId: DEFAULT
  auth:
    bearerToken: xxxx-yyyy-zzzz
```

Be sure to replace the **baseUrl** and **bearerToken** with your values.

**Option 2: Using Username/Password**

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: "management-context-1"
spec:
  baseUrl: <APIM management API URL>
  environmentId: DEFAULT
  organizationId: DEFAULT
  auth:
    credentials:
      username: admin
      password: admin
```

Replace **baseUrl**, **username**, and **password** with your actual values.
{% endtab %}

{% tab title="NextGen Cloud" %}
**Prerequisites**

To connect GKO to Gravitee NextGen Cloud, you'll need:

* A [Cloud Token](quickstart-guide.md#obtain-a-cloud-token) for authentication

**Obtain a Cloud Token**

For detailed instructions, see: [Generate a Cloud Token](https://documentation.gravitee.io/gravitee-cloud/guides/cloud-tokens)

**Configuration**

Create a file called `management-context-1.yaml` with the following contents:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: "management-context-1"
spec:
  cloud:
    token: <your-cloud-token>
```

Fields (like **baseUrl**, **environmentId**, and **organizationId**) are not needed as they are automatically included in the Cloud Token from NextGen Cloud.

Full documentation for the ManagementContext is available [here](../overview/custom-resource-definitions/managementcontext.md).
{% endtab %}
{% endtabs %}

### Apply the Configuration

Create the `ManagementContext` resource with the following command:

```bash
kubectl apply -f management-context-1.yaml
```

If the operation is successful, this line will appear in the CLI output:

```bash
managementcontext.gravitee.io/management-context-1 created
```

Now that you've defined a way for GKO to communicate with a Gravitee API Management instance, you can create your first GKO-managed API.

### Create an ApiV4Definition

The `ApiV4Definition` CRD is used to create modern Gravitee v4 APIs (for all types of APIs, including HTTP, Event APIs, and AI Agentic services). It contains all of the parameters of a Gravitee API such as the entrypoint, endpoint, plans, policies, groups & members, and documentation pages. The CRD also lets you control whether the API is started or stopped, and whether or not it is published to the Developer Portal.

Create a file called `echo-api.yaml` and enter the following contents:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: echo-api-declarative-v4
  namespace: default
spec:
  contextRef:
    name: "management-context-1"
  name: "Echo API Declarative"
  description: "API v4 managed by Gravitee Kubernetes Operator"
  version: "1.0"
  type: "PROXY"
  state: "STARTED"
  lifecycleState: "PUBLISHED"
  visibility: "PUBLIC"
  listeners:
    - type: HTTP
      paths:
        - path: "/echo-v4"
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
      name: "Free plan"
      description: "This plan does not require any authentication"
      security:
        type: "KEY_LESS"
```

There are a few things worth mentioning about the above resource:

* This API definition references the `ManagementContext` we just created. This tells GKO to sync this API definition with the APIM installation referenced in the `ManagementContext`.
* The API definition specifies that the API should be created in a `STARTED` state (i.e., deployed), and `PUBLISHED` on the Developer Portal with `PUBLIC` visibility.
* The backend target (or "endpoint") for this API is a mock service hosted by Gravitee that echoes back information about the incoming call.

Create the resource with the following command:

```bash
kubectl apply -f echo-api.yaml
```

If the operation is successful, this line will appear in the CLI output:

```bash
apiv4definition.gravitee.io/echo-api-declarative-v4 created
```

You will now be able to view your newly created API within the Gravitee API Management Console. It will be labeled as "Kubernetes Origin" and will be read-only (as the _source of truth_ is now your CRD file).

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

You can now also invoke your deployed API through the APIM Gateway. You'll need to update the example host name given below with your Gateway's real address:

```bash
curl -i http://{your-gateway-host}/echo-v4
```

{% hint style="success" %}
Congratulations, you did it!
{% endhint %}

To make changes to your API defintion, simply modify the CRD file and re-apply the CRD (with `kubectl apply ...`).

To delete the API, simply delete the resource using `kubectl delete -f echo-api.yaml`

### Next steps

To continue learning, there are many other example GKO resources available here: [https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/examples](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/examples)

Try creating some of these example APIs, resources (authentication providers, caches), and applications & subscriptions.

{% hint style="warning" %}
Remember to add the following `ManagementContext` reference to the API definition and application YAML files so that GKO knows which APIM installation to sync the APIs with:

```yaml
spec:
  contextRef:
    name: "management-context-1"
    namespace: "default"
```
{% endhint %}
