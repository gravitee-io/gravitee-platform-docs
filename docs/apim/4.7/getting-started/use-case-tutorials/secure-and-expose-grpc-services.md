# Secure and Expose gRPC Services

## Overview

This article demonstrates how to use Gravitee as a centralized location to secure and manage your gRPC APIs.

gRPC is well-suited for use cases that require real-time performance and treat an API like a JAVA class method that is instead executing on a remote server. A gRPC API relies on a [Protocol Buffers](https://protobuf.dev/overview) definition to serve an application and can use either Protocol Buffers or JSON for the message exchange format. What matters to Gravitee is that gRPC runs on HTTP/2 protocol, so you can easily create an HTTP proxy.

The following examples explain how to create a gRPC proxy API on top of an existing gRPC service, secure it with plans, document it, publish it in a Developer Portal, deploy it in a Gateway, and monitor its activity and logs. For these examples, we’ll be using [a simple set of sample gRPC services](https://hub.docker.com/r/jgiovaresco/apim-samples) and a default deployment of Gravitee API Management running in local Docker containers.&#x20;

## Prerequisites

To use the samples, the proper services must be running in the Docker containers:

* Docker Engine (e.g., [Docker Desktop on MacOS](https://docs.docker.com/desktop/install/mac-install/))
* The correct setup of gRPC samples and Gravitee installation in Docker, e.g., [load the setup using `docker-compose`](https://github.com/adriengravitee/grpc-gravitee-demo/blob/644b2e93aa03a5ab616047136c6201d6b0c9cfc0/docker/docker-compose-gravitee-grpc-demo.yml)
* The proper network configuration
* The [protofile related to each service](https://github.com/adriengravitee/grpc-gravitee-demo/tree/main/proto)

### gRPC samples and Gravitee installation in Docker

{% hint style="info" %}
You can adapt the following instructions to use your own gRPC services and setup
{% endhint %}

1. Download [the `docker-compose` file](https://github.com/adriengravitee/grpc-gravitee-demo/blob/14c53c68bb1e87c073b455669cba52290d08d551/docker/docker-compose-gravitee-grpc-demo.yml)
2. Copy it to the directory from which you'll be launching the `docker-compose` command
3.  Run the following:&#x20;

    {% code overflow="wrap" %}
    ```bash
    > docker compose -f docker-compose-gravitee-grpc-demo.yml up -d
    ```
    {% endcode %}
4.  Verify the containers initialize and run&#x20;

    <figure><img src="../../.gitbook/assets/docker containers.png" alt=""><figcaption></figcaption></figure>

### Modify the network

In this exercise, we will use a virtual host and dynamic routing to configure our API in Gravitee. To make that work, we need to modify the network configuration by adding the following lines to the `/etc/hosts` file:&#x20;

<figure><img src="../../.gitbook/assets/grpc networking.png" alt=""><figcaption></figcaption></figure>

## Examples

Since a gRPC service is a little different from a REST service, there are some subtleties that can be overlooked when creating a gRPC proxy API in Gravitee.&#x20;

### Example 1: Create a gRPC proxy API in Gravitee APIM

#### Step 1: Create a simple gRPC proxy

Follow the steps below to expose a simple gRPC service with one API on the Gateway. This exercise creates a gRPC proxy on port 8082 of the Gateway to expose the gRPC service method `helloworld.Greeter.SayHello` running in the local container `grpcbackend-1`.

1. Log in to your APIM Console
2.  Create a new API using the v4 API creation wizard

    <div align="left"><figure><img src="../../.gitbook/assets/grpc wizard.png" alt="" width="375"><figcaption></figcaption></figure></div>
3.  Enter the name, version, and description of your API (e.g., **HelloService gRPC** / **1.0** / **Simple gRPC proxy service**)&#x20;

    <figure><img src="../../.gitbook/assets/grpc proxy details.png" alt=""><figcaption></figcaption></figure>
4.  Select **Proxy Upstream Protocol**&#x20;

    <figure><img src="../../.gitbook/assets/grpc proxy select.png" alt=""><figcaption></figcaption></figure>
5.  Enter the context-path **/helloworld.Greeter** (do not enable virtual hosts for this API)&#x20;

    <figure><img src="../../.gitbook/assets/grpc context path.png" alt=""><figcaption></figcaption></figure>
6.  Configure your API endpoint:&#x20;

    * Set the **Target URL** to `grpc://grpc-backend1:8888/helloworld.Greeter`
    * Set the **Security Configuration** option to **HTTP 2**
    * Leave all other settings as default

    <figure><img src="../../.gitbook/assets/grpc endpoint.png" alt=""><figcaption></figcaption></figure>
7.  Configure and validate a **KEY\_LESS** security plan&#x20;

    <figure><img src="../../.gitbook/assets/grpc keyless.png" alt=""><figcaption></figcaption></figure>
8. Check that all values are correct in the summary, then deploy your API
9.  Verify that your API **HelloService gRPC** is accessible from the **APIs** menu of the APIM Console&#x20;

    <figure><img src="../../.gitbook/assets/grpc apis.png" alt=""><figcaption></figcaption></figure>
10. Click on your API and confirm it has started, e.g., by checking the Danger Zone section for the **Stop the API** action&#x20;

    <figure><img src="../../.gitbook/assets/grpc started.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Click **Publish the API** to publish **HelloService gRPC** in the Developer Portal that is also available in this Docker installation.
{% endhint %}

#### Step 2: Test HelloService gRPC (no virtual host)

To test **HelloService gRPC** on Mac OS, use the command line `grpcurl`.

1. Download the [`.proto` files](https://github.com/adriengravitee/grpc-gravitee-demo/tree/644b2e93aa03a5ab616047136c6201d6b0c9cfc0/proto)
2. Open a terminal and go to the directory that contains the `.proto` files
3.  Call your service using the `helloworld.proto` file and a sample body message:&#x20;

    {% code overflow="wrap" %}
    ```bash
    > grpcurl -plaintext -proto ./helloworld.proto -import-path . -d '{"name":"Adrien"}'   localhost:8082 helloworld.Greeter.SayHello
    ```
    {% endcode %}
4.  Verify the expected response:

    {% code overflow="wrap" %}
    ```bash
    {
      "message": "Hello Adrien"
    }
    ```
    {% endcode %}

{% hint style="success" %}
Your gRPC service is now accessible through Gravitee and you can manage the whole lifecycle of **HelloService gRPC**.
{% endhint %}

### Example 2: Create multiple gRPC services

#### Step 1: Create a gRPC proxy with virtual host

The steps below use the virtual host feature to expose multiple gRPC services running in the same container with a single entrypoint.

1. Log in to your APIM Console
2.  Create a new API using the v4 API creation wizard

    <div align="left"><figure><img src="../../.gitbook/assets/grpc wizard.png" alt="" width="375"><figcaption></figcaption></figure></div>
3.  Enter the name, version, and description of your API (e.g., **gRPC Proxy** / **1.0** / **Simple gRPC proxy service**)&#x20;

    <figure><img src="../../.gitbook/assets/grpc proxy details 2.png" alt=""><figcaption></figcaption></figure>
4.  Select **Proxy Upstream Protocol**&#x20;

    <figure><img src="../../.gitbook/assets/grpc proxy select.png" alt=""><figcaption></figcaption></figure>
5.  Configure your API entrypoints to use virtual hosts and set the **Virtual host** to `grpc.gravitee.io` (same as the entry in the `/etc/hosts` file), then click **Validate my entrypoints**

    <figure><img src="../../.gitbook/assets/grpc entrypoints.png" alt=""><figcaption></figcaption></figure>
6.  Configure your API endpoint:&#x20;

    * Set the **Target URL** to `grpc://grpc-backend1:8888`
    * Set the **Security Configuration** option to **HTTP 2**
    * Leave all other settings as default

    <figure><img src="../../.gitbook/assets/grpc endpoint 2.png" alt=""><figcaption></figcaption></figure>
7.  Configure and validate a **KEY\_LESS** security plan&#x20;

    <figure><img src="../../.gitbook/assets/grpc keyless.png" alt=""><figcaption></figcaption></figure>
8. Check that all values are correct in the summary, then deploy your API
9.  Verify that your API **gRPC Proxy** is accessible from the **APIs** menu of the APIM Console&#x20;

    <figure><img src="../../.gitbook/assets/grpc apis list.png" alt=""><figcaption></figcaption></figure>
10. Click on your API and confirm it has started, e.g., by checking the Danger Zone section for the **Stop the API** action&#x20;

    <figure><img src="../../.gitbook/assets/grpc api running.png" alt=""><figcaption></figcaption></figure>

#### Step 2: Test gRPC Proxy

To test **gRPC Proxy** on Mac OS, use the command line `grpcurl`.

1. Download the [`.proto` files](https://github.com/adriengravitee/grpc-gravitee-demo/tree/644b2e93aa03a5ab616047136c6201d6b0c9cfc0/proto)
2. Open a terminal and go to the directory that contains the `.proto` files
3.  Call your service using the `helloworld.proto` file and a sample body message:&#x20;

    {% code overflow="wrap" %}
    ```bash
    > grpcurl -plaintext -proto ./helloworld.proto -import-path . -d '{"name":"here"}' -authority grpc.gravitee.io grpc.gravitee.io:8082 helloworld.Greeter.SayHello
    ```
    {% endcode %}
4.  Verify the expected response:

    {% code overflow="wrap" %}
    ```bash
    {
      "message": "Hello here"
    }
    ```
    {% endcode %}
5.  Call your second service:

    {% code overflow="wrap" %}
    ```bash
    > grpcurl -plaintext -proto ./route_guide.proto -import-path . -d '{"latitude": 413628156, "longitude": -749015468}' -authority grpc.gravitee.io grpc.gravitee.io:8082 routeguide.RouteGuide/GetFeature
    ```
    {% endcode %}
6.  Verify the expected response:

    {% code overflow="wrap" %}
    ```bash
    {
      "name": "U.S. 6, Shohola, PA 18458, USA",
      "location": {
        "latitude": 413628156,
        "longitude": -749015468
      }
    }
    ```
    {% endcode %}

{% hint style="success" %}
Both of your gRPC services are now accessible through Gravitee and you can manage the whole lifecycle of **gRPC Proxy**.
{% endhint %}

### Example 3: Secure your gRPC call with an API Key

Every Gravitee API requires at least one plan, which provides a service and access layer on top of your API and includes a security type, e.g., Keyless (the default plan type). To add an API Key plan to an existing API, follow the steps below.

#### Step 1: Create an API Key Plan

1. Open your API definition in APIM Console
2. Click on **Consumers** in the inner left nav
3.  Under the **Plans** tab, click **Add new plan** and choose **API Key**&#x20;

    <figure><img src="../../.gitbook/assets/grpc add plan 2.png" alt=""><figcaption></figcaption></figure>
4. Name your plan, e.g., “API Key Plan”
5.  Toggle the **Auto Validate subscription** option ON (you can leave this OFF to add an extra step of manual validation for each subscription)&#x20;

    <figure><img src="../../.gitbook/assets/grpc plan validate.png" alt=""><figcaption></figcaption></figure>
6. Click through additional configuration pages, leaving the default settings, then click **Create**
7.  Under the **Plans** header tab, go to the **Staging** tab and click the publish icon to promote the API Key plan to the **PUBLISHED** Stage&#x20;

    <figure><img src="../../.gitbook/assets/grpc plan publish.png" alt=""><figcaption></figcaption></figure>
8.  Verify that the API Key plan appears under the **PUBLISHED** tab&#x20;

    <figure><img src="../../.gitbook/assets/grpc published.png" alt=""><figcaption></figcaption></figure>
9.  Click on the API Key Plan, then select the **Subscriptions** tab&#x20;

    <figure><img src="../../.gitbook/assets/grpc subscriptions.png" alt=""><figcaption></figcaption></figure>
10. Using an existing application, click **Create a subscription** using the API Key plan (this example uses a **Default application** , but you can create your own)&#x20;

    <figure><img src="../../.gitbook/assets/grpc default application.png" alt=""><figcaption></figcaption></figure>
11. To retrieve the API Key, select the **Subscriptions** tab and scroll down to the bottom of the page&#x20;

    <figure><img src="../../.gitbook/assets/grpc subscription details.png" alt=""><figcaption></figcaption></figure>

#### Step 2: Test your Proxy gRPC with an API Key&#x20;

1. Open a terminal
2. Go to the directory where you can access the `.proto` files
3.  Run the following command after replacing `<yourapikeyhere>` with your API Key:

    {% code overflow="wrap" %}
    ```bash
    > grpcurl -plaintext -proto ./helloworld.proto -import-path . -d '{"name":"here"}' -H 'X-Gravitee-Api-Key: <yourapikeyhere>' -authority grpc.gravitee.io grpc.gravitee.io:8082 helloworld.Greeter.SayHello
    ```
    {% endcode %}
4.  Verify the expected response:

    {% code overflow="wrap" %}
    ```bash
    {
      "message": "Hello here"
    }
    ```
    {% endcode %}
5.  Test with the `routeguide.RouteGuide` service:

    {% code overflow="wrap" %}
    ```bash
    > grpcurl -plaintext -proto ./route_guide.proto -import-path . -d '{"latitude": 413628156, "longitude": -749015468}' -H 'X-Gravitee-Api-Key: <yourapikeyhere>' -authority grpc.gravitee.io grpc.gravitee.io:8082 routeguide.RouteGuide/GetFeature
    ```
    {% endcode %}
6.  Verify the expected response:

    {% code overflow="wrap" %}
    ```bash
    {
      "name": "U.S. 6, Shohola, PA 18458, USA",
      "location": {
        "latitude": 413628156,
        "longitude": -749015468
      }
    }
    ```
    {% endcode %}
7.  Close plans for the API except for the API Key plan:&#x20;

    1. Under the **Plans** header tab, select the **PUBLISHED** tab&#x20;
    2. Click on the **X** icon to close a plan

    <figure><img src="../../.gitbook/assets/grpc close plans.png" alt=""><figcaption></figcaption></figure>
8. Confirm that if you try to connect to the gRPC proxy service without an API Key, the Gateway will block the call:
   1.  Run the following command:

       {% code overflow="wrap" %}
       ```bash
       grpcurl -plaintext -proto ./helloworld.proto -import-path . -d '{"name":"here"}' -authority grpc.gravitee.io grpc.gravitee.io:8082 helloworld.Greeter.SayHello
       ```
       {% endcode %}
   2.  Verify the expected response:

       {% code overflow="wrap" %}
       ```bash
       ERROR:
         Code: Unauthenticated
         Message: unexpected HTTP status code received from server: 401 (Unauthorized); transport: received unexpected content-type "text/plain"
       ```
       {% endcode %}

{% hint style="success" %}
Success! The API Key plan is protecting access to the backend service.
{% endhint %}
