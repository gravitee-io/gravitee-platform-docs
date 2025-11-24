---
description: Getting started with Quickstart.
---

# Quickstart guide

## Overview

Following this quickstart guide is the fastest way to start working with the Gravitee Kubernetes Operator (GKO). The sections below describe how to:

* [Install GKO](quickstart-guide.md#deploy-the-gko)
* [Create a Management Context](quickstart-guide.md#create-a-managementcontext)
* [Create an API Definition and invoke the API](quickstart-guide.md#create-an-apidefinition)

In this guide, we assume that Gravitee API Management is acting as the control plane for the Gravitee gateway. The gateway loads it's APIs from APIM's repository (e.g. MongoDB, or via a Bridge Gateway in a hybrid setup). GKO acts as a way to define and manage API's "as-code" rather than using the GUI. GKO synchronises all of its actions, such as creating APIs and managing their lifecycle, directly with Gravitee API management through the management API.

### Prerequisites

* A running instance of Gravitee API Management. It doesn't matter where this is running so long as you have access to credentials that can be used to connect GKO to this APIM instance.
* A Kubernetes cluster on which to install GKO

## Install GKO

{% hint style="info" %}
For comprehensive deployment details, see the [GKO Install Guide](installation/).
{% endhint %}

Use Helm to install GKO on your Kubernetes cluster:

{% code overflow="wrap" %}
```sh
helm repo add graviteeio https://helm.gravitee.io
helm install graviteeio-gko graviteeio/gko
```
{% endcode %}

## Create a ManagementContext

The [`ManagementContext` ](../overview/custom-resource-definitions/managementcontext.md)CRD is used to provide GKO with everything needed to invoke an APIM instance's management API. To fill out the CRD correctly, you'll need:

* the APIM management API URL
* credentials to authenticate GKO with the management API

If you're running APIM locally you can use the default admin account to authenticate (user: `admin`, password: `admin`).

Alternatively, you can head to your APIM instance and [created a dedicated service account and token](../guides/define-an-apim-service-account-for-gko.md) for GKO to use. Make sure to copy the token value to use in the step below.

Create a file called `management-context-1.yaml` and enter the following contents:

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

Be sure to replace the **baseUrl** and **bearerToken** with you values. If you're using the admin account or another user's credentials, you can use the following syntax:

<pre class="language-yaml"><code class="lang-yaml"><strong>spec:
</strong><strong>  auth:
</strong>    credentials:
      username: admin
      password: admin    
</code></pre>

Create the **ManagementContext** resource with the following command:

```
kubectl apply -f management-context-1.yaml
```

If the operation is successful, this line will appear in the CLI output:

```sh
managementcontext.gravitee.io/management-context-1 created
```

Now that we've defined a way for GKO to communicate with a Gravitee API Management instance, we can create our first GKO-managed API.

## Create an ApiDefinition

The [`ApiDefinition` ](../overview/custom-resource-definitions/apidefinition.md)CRD is used to created Gravitee v2 APIs, and contains all the parameters of a Gravitee API such as entrypoint, endpoint, plans, policies, groups & members, and documentation pages. The CRD also lets you control whether the API is started or stopped, and whether or not it is published to the developer portal.

Create a file called `echo-api.yaml` and enter the following contents:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: echo-api-declarative
spec:
  name: "Echo API Declarative"
  contextRef: 
    name: "management-context-1"
    namespace: "default"
  version: "1"
  state: "STARTED"
  lifecycle_state: "PUBLISHED"
  description: "Gravitee Kubernetes Operator sample"
  local: false
  plans:
    - name: "KEY_LESS"
      description: "FREE"
      security: "KEY_LESS"
  proxy:
    virtual_hosts:
      - path: "/echo-api"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
```

There are a few things worth mentioning about the above resource:

* this API definition references the ManagementContext we just created. This will tell GKO to sync this API definition with the APIM installation referenced in the ManagementContext
* The API definition specifies that the API should be created in a `STARTED` state (i.e. deployed), and `PUBLISHED` on the developer portal.
* The backend **target** for this API is a mock service hosted by Gravitee that echoes back information about the incoming call
* **local** is set to false, meaning the gateway will load this API through the usual central database (as opposed to a [local configMap](api-storage-and-control-options/configure-the-gateway-to-load-apis-from-local-configmaps.md))

Create the resource with the following command:

```
kubectl apply -f echo-api.yaml
```

If the operation is successful, this line will appear in the CLI output:

```sh
apidefinition.gravitee.io/basic-api-example created
```

You should now be able to open the APIM Console to view your newly created API. It will be labelled as "managed by GKO" and will be read-only in the APIM UI.

You can now also invoke your deployed API through the APIM Gateway. You'll need to update the example host name given below with your gateway's real address:

```sh
curl -i http://<your-gateway-host>/<your gateway path>/echo-api
```

{% hint style="success" %}
Congratulations, you did it!
{% endhint %}

## Next steps

To continue learning, there are many other example GKO resources available here: [https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/examples](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/examples)

Try creating some of these example APIs (v2 and v4), Resources (authentication providers, caches, ...), and Applications. **But remember** to add the following ManagementContext reference to the API definition and Application yaml files so that GKO knows which APIM installation to sync the APIs with:

```
spec:
  contextRef:
    name: "management-context-1"
    namespace: "default"
```
