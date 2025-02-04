---
description: >-
  An end-to-end guide for managing JWT subscriptions with GKO, without the need
  for an external identity provider.
---

# Manage JWT subscriptions with GKO

## Overview

This guide takes you step-by-step through managing JWT subscriptions with GKO. It **does not** rely on an external identity provider, such as Gravitee Access Management, Ping Federate, or Auth0. Instead, it will guide you through how to create your own public and private key pair that you can use to sign and verify JWT tokens.

## Before you begin

* You must have an Gravitee Kubernetes Operator running on your system.
* You must have a Gravitee API Management and Gravitee Gateway instance running on your system.

## Procedure

To set up a subscription, complete the following steps:

* [#generate-a-public-key](manage-jwt-subscriptions-with-gko.md#generate-a-public-key "mention")
* [#store-the-public-key](manage-jwt-subscriptions-with-gko.md#store-the-public-key "mention")
* [#configure-the-json-web-token-plan](manage-jwt-subscriptions-with-gko.md#configure-the-json-web-token-plan "mention")
* [#configure-the-application-resource](manage-jwt-subscriptions-with-gko.md#configure-the-application-resource "mention")
* [#configuring-the-subscription-resource](manage-jwt-subscriptions-with-gko.md#configuring-the-subscription-resource "mention")
* [#applying-the-resource](manage-jwt-subscriptions-with-gko.md#applying-the-resource "mention")
* [#retrieving-a-token](manage-jwt-subscriptions-with-gko.md#retrieving-a-token "mention")

### Generate a public key

You can use a hardcoded public key to configure the plan. To Generate the the public key, use the following command:

```bash
ssh-keygen -t rsa -b 4096 -m PEM -f pki/private.key
openssl rsa -in jwt-demo.key -pubout -outform PEM -out pki/public.key
```

### Store the public key

Store the public key in a secret using the following command:

```
kubectl create secret generic jwt --from-file=pki/public.key --dry-run=client -o yaml > resources/jwt-key.yml
```

### Configure the JSON Web Token plan

Configure the JSON Web Token (JWT) plan in the API Definition. Here is an example of an API definition that is configured with a JSON Web Token plan:

{% code lineNumbers="true" %}
```bash
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "jwt-demo"
spec:
  contextRef:
    name: dev-ctx
  definitionContext:
    syncFrom: MANAGEMENT
  name: "jwt-demo"
  version: "1"
  type: "PROXY"
  description: "JWT subscription demo API"
  listeners:
    - type: HTTP
      paths:
        - path: "/jwt-demo"
      entrypoints:
        - type: http-proxy
          qos: AUTO
  endpointGroups:
  - name: "Default HTTP proxy group"
    type: "http-proxy"
    endpoints:
    - name: "Default HTTP proxy"
      type: "http-proxy"
      configuration:
        target: "https://api.gravitee.io/echo"
      inheritConfiguration: false
      secondary: false
  analytics:
    enabled: true
  plans:
    JWT:
      name: "jwt"
      security:
        type: "JWT"
        configuration:
          signature: "RSA_RS256"
          publicKeyResolver: "GIVEN_KEY"
          resolverParameter: '[[ secret `jwt/public.key` ]]'
          userClaim: "sub"
          clientIdClaim: "client_id"
      status: "PUBLISHED"
```
{% endcode %}

### Configure the application resource

* Configure the application resource based on your setup. The client\_Id must match the client ID of the token.

Here is an example of the client resource:

{% code lineNumbers="true" %}
```
apiVersion: gravitee.io/v1alpha1
kind: Application
metadata:
  name: echo-client
spec:
  contextRef:
    name: "dev-ctx"
  name: "echo-client"
  description: "echo API client"
  settings:
    app:
      type: WEB
      clientId: echo-client
```
{% endcode %}

### Configuring the subscription resource

For a subscription to be valid, it must have the following elements:

* Reference a valid API using the APIs name and an optional namespace. If you do not provide a namespace, the namespace of the subscription is used.
* Reference a valid plan key defined in the API.
* Reference a valid application and an optional namespace.

{% hint style="info" %}
If your API reference point to a v2 API, you must add the `kind` property with the `ApiDefinition` value to your API reference.
{% endhint %}

Here is an example of a subscription resource:

```
apiVersion: gravitee.io/v1alpha1
kind: Subscription
metadata:
  name: echo-client-subscription
spec:
  api:
    name: jwt-demo
  application: 
    name: echo-client
  plan: JWT
```

### Applying the resource

{% hint style="warning" %}
* Only resources with a management context reference are supported.
* The management context must be configured to your setup. To configure the management context, use the management API URL and credentials.
{% endhint %}

To apply the resource, use the following commands:

```
kubectl apply -f resources/management-context.yml
kubectl apply -f resources/jwt-key.yml
kubectl apply -f resources/api.yml
kubectl apply -f resources/application.yml
kubectl apply -f resources/subscription.yml
```

### Retrieving a token

Forge a token using the JWT debugger. For more information about the JWT debugger, go to [jwt.io](https://jwt.io/).

Set the algorithm to `RS256` and sign your token with the provided keys and the following claims:

```json
{
  "sub": "echo-client",
  "client_id": "echo-client",
  "iat": 1516239022
}
```

Alternatively, if you are following this guide on macOS or Linux, you can get a token by running this [get\_token.sh](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/examples/usecase/subscribe-to-jwt-plan/pki/get_token.sh) bash script.

```sh
export TOKEN=$(bash pki/get_token.sh)
```

### Invoke the API

You can now call your API using the following command:

```
GW_URL=<GATEWAY_URL>
curl -H "Authorization: Bearer $TOKEN" "$GW_URL/jwt-demo"
```

Replace \<GATEWAY\_URL> with your Gateway's URL.

### Close the subscription

Deleting the subscription resource results in the subscription being closed. Which means the client id associated with your token will be rejected with a 401 status on subsequent calls to the gateway.

```
kubectl delete -f resources/subscription.yml
```
