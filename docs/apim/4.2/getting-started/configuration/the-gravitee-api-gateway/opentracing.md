---
description: Tutorial on OpenTracing.
---

# OpenTracing

## Introduction

Using OpenTracing allows Gravitee to trace every request that comes through the Gravitee API Management (APIM) Gateway, creating a deep level of insight into API policies and simplifying debugging. Without OpenTracing, you’ll only receive limited details, which makes monitoring and troubleshooting both complicated and time-consuming.

So, if you’re looking for a way to simplify debugging, improve monitoring, and enhance visibility into requests across multiple services, Gravitee’s OpenTracing solution with Jaeger as a tracer has you covered.

This article will run through how to enable OpenTracing using the `gravitee.yaml` file and using a Docker image.

### Enable OpenTracing using the `gravitee.yaml` file

In the `gravitee.yaml` file, enable tracing by adding the following configuration:

```yaml
tracing:
    enabled: true
    type: jaeger
    jaeger:
    host: localhost
    port: 14250
```

Here, you _must_ change `enabled` from `false` to `true`.

And that’s it! You’ve enabled OpenTracing on APIM Gateway.

### Test OpenTracing in Docker

First, you'll need to start the Jaeger component with the Docker image by running this command:

```sh
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

This is the Docker run command for installing Jaeger. It is direct from [Jaegertracing.io](https://www.jaegertracing.io/docs/1.25/getting-started/#all-in-one), and no customizations to the configuration are included. Visit the [Jaeger website](https://www.jaegertracing.io/docs/1.25/getting-started/#all-in-one) for more information on the Jaeger tracer from Uber.

{% hint style="info" %}
**Pro-tip**

Running this Docker command will also provide access to the JaegerUI, which can be reached using its default port: `http://localhost:16686`.
{% endhint %}

You can confirm Jaeger has been enabled and is running by checking Docker.

Next, you'll need to install the .ZIP File For The Jaeger Tracer Plugin. Since the Jaeger tracer is not bundled by default, [click here](https://download.gravitee.io/#graviteeio-apim/plugins/tracers/gravitee-tracer-jaeger/), and add the plugin for the Gravitee Jaeger Tracer .ZIP file to the configuration of your APIM Gateway instance.

Now, it's time to test OpenTracing. Follow these steps:

1. Now that you have OpenTracing enabled, run your API Gateway and APIM.
2. Open Gravitee APIM, and choose an API that already has a policy assigned to it (or create a test API and add any policies you like for this test). Now, call your API.
3. To see your calls, open the helpful, user-friendly JaegerUI by visiting `http://localhost:16686` (note that JaegerUI was automatically installed earlier in the process). Select **Search** and find the API you called.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/configuration/tracing-info-general.png" alt=""><figcaption><p>See API calls in JaegerUI</p></figcaption></figure>

In these examples, you’ll also notice that each policy traversed is listed on a different line to provide greater visibility and to assist with debugging. You can even see timestamp info on the detailed view.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/configuration/tracing-info-detailed.png" alt=""><figcaption><p>Timestamp information on the detailed view</p></figcaption></figure>

## Configure Environment Variables

You can configure the environment variables as needed in the Jaeger Gateway. For example:

```
gravitee_service_tracing_enabled: true
gravitee_services_tracing_jaegar_host: localhost
gravitee_services_tracing_jaeger_port: 14250
```

## Enable OpenTracing Via Docker Compose

You can also enable OpenTracing using Jaeger as a tracer with this Docker Compose. Go to https://github.com/gravitee-io/gravitee-api-management/tree/master/docker/quick-setup/opentracing-jaeger to access the `docker-compose.yml`.

With this option enabled, you can continue to call your APIs through your Gateway with the usual host: `http://localhost:8082/myapi`.

#### 1. How To Run OpenTracing With Jaeger

1. Since the Jaeger tracer is not bundled by default, **you must download the .ZIP file** for the version you want to run ([click here](https://download.gravitee.io/#graviteeio-apim/plugins/tracers/gravitee-tracer-jaeger/) to download the .ZIP).
2.  After downloading, **you must copy this into the `opentracing-jaeger/.plugins` directory** using the command below:

    `APIM_VERSION={APIM_VERSION} docker-compose up -d`
3.  Be sure to fetch last version of images by running this command:

    ```
    export APIM_VERSION={APIM_VERSION} && docker-compose down -v && docker-compose pull && docker-compose up

    ```
