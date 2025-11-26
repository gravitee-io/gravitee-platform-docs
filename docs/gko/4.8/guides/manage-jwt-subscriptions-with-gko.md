---
description: >-
  An end-to-end guide for managing JWT subscriptions with GKO, without the need
  for an external identity provider.
---

# Manage JWT subscriptions with GKO

## Overview

This is a step-by-step guide for how to manage JWT subscriptions with GKO. It **does not** rely on an external identity provider, such as Gravitee Access Management, Ping Federate, or Auth0. Instead, it shows you how to create your own public and private key pair that you can use to sign and verify JWT tokens.

{% hint style="info" %}
GKO-managed subscriptions only work when GKO is configured to sync APIs with a Gravitee API management control plane (i.e. local=false for v2 APIs, or syncFrom=MANAGEMENT for v4 APIs). See [api-storage-and-control-options](../getting-started/api-storage-and-control-options/ "mention") for more information about these configuration options.
{% endhint %}

## Before you begin

* You must have Gravitee Kubernetes Operator running on your system.
* You must have Gravitee API Management and a Gravitee Gateway running on your system.

## Procedure

To set up a subscription, complete the following steps.

1.  Generate a public key using the following command. You can use a hardcoded public key to configure the plan.

    ```bash
    ssh-keygen -t rsa -b 4096 -m PEM -f pki/private.key
    openssl rsa -in jwt-demo.key -pubout -outform PEM -out pki/public.key
    ```
2.  Store the public key in a Secret using the following command:

    ```
    kubectl create secret generic jwt --from-file=pki/public.key --dry-run=client -o yaml > resources/jwt-key.yml
    ```
3.  Configure the JSON Web Token (JWT) plan in the API definition. Here is an example of an API definition that is configured with a JSON Web Token plan:

    ```yaml
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
4.  Configure the application resource based on your setup. The `client_Id` must match the client ID of the token. Here is an example of the client resource:

    ```yaml
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
5.  Configure the subscription resource. For a subscription to be valid, it must reference the following:

    1. A valid API, using the APIs name and an optional namespace. If you do not provide a namespace, the namespace of the subscription is used.
    2. A valid plan key defined in the API.
    3. A valid application and an optional namespace.

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning">
      <p>If your API reference points to a v2 API, you must add the <code>kind</code> property with the <code>ApiDefinition</code> value to your API reference.</p>
    </div>

    Here is an example of a subscription resource:

    ```yaml
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
6.  Apply the resource.

    <div data-gb-custom-block data-tag="hint" data-style="danger" class="hint hint-danger">
      <ul>
        <li>Only resources with a management context reference are supported.</li>
        <li>The management context must be configured for your setup. To configure the management context, use the Management API URL and credentials.</li>
      </ul>
    </div>

    \
    To apply the resource, use the following commands:

    ```bash
    kubectl apply -f resources/management-context.yml
    kubectl apply -f resources/jwt-key.yml
    kubectl apply -f resources/api.yml
    kubectl apply -f resources/application.yml
    kubectl apply -f resources/subscription.yml
    ```
7.  Retrieve a token. Forge a token using the JWT debugger. For more information about the JWT debugger, go to [jwt.io](https://jwt.io/).

    Set the algorithm to `RS256` and sign your token with the provided keys and the following claims:

    ```json
    {
    "sub": "echo-client",
    "client_id": "echo-client",
    "iat": 1516239022
    }
    ```

    Alternatively, if you are following this guide on macOS or Linux, you can get a token by running this [get\_token.sh](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/examples/usecase/subscribe-to-jwt-plan/pki/get_token.sh) bash script:

    ```sh
    export TOKEN=$(bash pki/get_token.sh)
    ```
8.  Invoke the API. You can now call your API using the following command. Replace \<GATEWAY\_URL> with your Gateway's URL.

    ```bash
    GW_URL=<GATEWAY_URL>
    curl -H "Authorization: Bearer $TOKEN" "$GW_URL/jwt-demo"
    ```
9.  Close the subscription. Deleting the subscription resource results in the subscription being closed. This means that the client ID associated with your token will be rejected with a 401 status on subsequent calls to the Gateway.

    ```bash
    kubectl delete -f resources/subscription.yml
    ```
