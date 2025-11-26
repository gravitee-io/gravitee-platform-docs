---
description: Tutorial on Configuring the OpenTracing in Gravitee API Management Gateway.
---

# Configuring the OpenTracing in Gravitee API Management Gateway

## Introduction

Gravitee's OpenTracing solution with Jaeger allows you to trace every request that comes through the API Management (APIM) Gateway. This provides enhanced monitoring capabilities, such as in-depth visibility into API policies and requests across multiple services, and simplifies debugging.

This page describes how to:

* [Enable OpenTracing using the `gravitee.yaml` file](opentracing.md#enable-opentracing-using-gravitee.yaml)
* [Enable OpenTracing using Docker Compose](opentracing.md#enable-opentracing-via-docker-compose)

## Enable OpenTracing using `gravitee.yaml`

To enable OpenTracing on APIM Gateway, add the following to the gravitee.yaml file:

```yaml
tracing:
    enabled: true
    type: jaeger
    jaeger:
    host: localhost
    port: 14250
```

### Test OpenTracing in Docker

To test OpenTracing in Docker:

1.  Use the Docker run command for installing Jaeger with no customizations:

    \{% code overflow="wrap" %\}

    ```bash
    docker run -d --name jaeger \
      -p 5775:5775/udp \
      -p 6831:6831/udp \
      -p 6832:6832/udp \
      -p 5778:5778 \
      -p 16686:16686 \
      -p 14268:14268 \
      -p 14250:14250 \
      -p 9411:9411 \
      jaegertracing/all-in-one:1.24
    ```

    \{% endcode %\}

    {% hint style="info" %} Running this Docker command will also provide access to the JaegerUI, which can be reached on its default port: `http://localhost:16686` {% endhint %}2. Confirm Jaeger has been enabled and is running by checking Docker
2. Install the .ZIP file for the Jaeger tracer plugin:
   1. Since the Jaeger tracer is not bundled by default, [click here](https://download.gravitee.io/#graviteeio-apim/plugins/tracers/gravitee-tracer-jaeger/) to download it
   2. Add the plugin for the Gravitee Jaeger tracer .ZIP file to the configuration of your APIM Gateway instance
3. Run your API Gateway and APIM.
4. Open Gravitee APIM and choose an API with a policy assigned to it
5. Call your API
6. To see your calls:
   1. Open JaegerUI by visiting `http://localhost:16686` (note that JaegerUI was automatically installed earlier in the process)
   2.  Select **Search** and find the API you called

       <figure><img src="broken-reference" alt=""><figcaption><p>See API calls using JaegerUI</p></figcaption></figure>

       Each policy traversed is listed on a different line to provide greater visibility and assist with debugging. Timestamp info is included in the detailed view.

       <figure><img src="broken-reference" alt=""><figcaption><p>Timestamp information in the detailed view</p></figcaption></figure>

### Configure Environment Variables

Configure environment variables as needed in the Jaeger Gateway. For example:

```
gravitee_service_tracing_enabled: true
gravitee_services_tracing_jaegar_host: localhost
gravitee_services_tracing_jaeger_port: 14250
```

## Enable OpenTracing via Docker Compose

To enable OpenTracing using Jaeger as a tracer, use the `docker-compose.yml` found at https://github.com/gravitee-io/gravitee-api-management/tree/master/docker/quick-setup/opentracing-jaeger.

With this option enabled, you can continue to call your APIs through your Gateway with the usual host: `http://localhost:8082/myapi`.

### How To Run OpenTracing With Jaeger

1. Since the Jaeger tracer is not bundled by default, you must download the .ZIP file for the version you want to run [here](https://download.gravitee.io/#graviteeio-apim/plugins/tracers/gravitee-tracer-jaeger/)
2.  Copy the .ZIP into the `opentracing-jaeger/.plugins` directory:

    `APIM_VERSION={APIM_VERSION} docker-compose up -d`
3.  Fetch the last version of images:

    ```bash
    export APIM_VERSION={APIM_VERSION} && docker-compose down -v && docker-compose pull && docker-compose up
    ```
