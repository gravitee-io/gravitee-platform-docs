---
hidden: false
noIndex: false
description: The Gamma Edge Reactor listens on its own gateway port, which Kubernetes does not expose by default. Follow the steps to create an Edge ingress.
---

# Configure Edge Ingress

## Overview

The Edge Reactor listens on its own port on the gateway, separate from the port that serves your APIs. On Kubernetes, that port isn't exposed by default, so an Edge Daemon can't fetch its configuration or report its heartbeat, its metrics, and its shadow AI detections until you expose it.

Exposing it takes three settings in your `values.yaml`, each of which gates the next:

1. `gateway.edge.enabled` turns the Edge Reactor listener on in the gateway configuration.
2. `gateway.services.edge.enabled` adds the port to the gateway Kubernetes Service.
3. `gateway.services.edge.ingress.enabled` creates the Ingress that routes external traffic to that port.

{% hint style="warning" %}
By default, the Edge Reactor listener is plain HTTP, and the connection between a daemon and the gateway isn't authenticated. Until you secure it, don't expose it to the public internet. Restrict it to a private network, a VPN, or an IP-allowlisted corporate network. See [Secure the Edge Reactor listener](secure-the-edge-reactor-listener.md).
{% endhint %}

## Enable the Edge Reactor listener

Add a `gateway.edge` block to your `values.yaml`. Without this block, neither the service port nor the ingress is rendered, whatever the other settings say.

```yaml
gateway:
  edge:
    enabled: true
    port: 18093
```

The following table describes each field:

| Field     | Description                                                                                                          |
| --------- | ---------------------------------------------------------------------------------------------------------------------- |
| `enabled` | Turns the Edge Reactor listener on. There's no `gateway.edge` block in the default `values.yaml`, so you add it yourself. |
| `port`    | The port the listener binds to. The default is `18093`.                                                              |

## Expose the port on the gateway service

Add the port to the gateway Kubernetes Service under `gateway.services.edge`. It's enabled by default, and it takes effect only once `gateway.edge.enabled` is `true`.

```yaml
gateway:
  services:
    edge:
      enabled: true
      service:
        externalPort: 18093
        internalPort: 18093
```

The following table describes each field:

| Field                  | Description                                                                          |
| ---------------------- | -------------------------------------------------------------------------------------- |
| `enabled`              | Adds the Edge Reactor port to the gateway Service. The default is `true`.            |
| `service.externalPort` | The port the Service exposes. The default is `18093`.                                |
| `service.internalPort` | The port on the gateway pod that the Service forwards to. The default is `18093`.    |

## Create the ingress

Enable the ingress under `gateway.services.edge.ingress` and give it the host your devices reach. This creates a dedicated Ingress resource that routes external traffic to the Edge Reactor port on your gateway pods.

```yaml
gateway:
  services:
    edge:
      ingress:
        enabled: true
        ingressClassName: nginx
        path: /
        pathType: Prefix
        hosts:
          - apim-edge.example.com
        annotations: {}
        tls:
          - secretName: apim-gateway-edge-tls
            hosts:
              - apim-edge.example.com
```

The following table describes each field:

| Field              | Description                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`          | Creates the Ingress resource. The default is `false`.                                                                               |
| `ingressClassName` | The ingress class to use. Leave it empty to let the cluster's default class handle the resource. The value `none` omits the field. |
| `path`             | The path the rule matches. The default is `/`.                                                                                      |
| `pathType`         | The Kubernetes path-matching type. The default is `Prefix`.                                                                         |
| `hosts`            | The hosts the rule answers for. One rule is created per host.                                                                       |
| `annotations`      | Annotations to add to the Ingress resource.                                                                                          |
| `tls`              | The TLS blocks of the Ingress resource. This terminates TLS at the ingress, so a daemon's client certificate stops there. See [Terminate TLS in front of the gateway](secure-the-edge-reactor-listener.md#terminate-tls-in-front-of-the-gateway). |

## Apply the change

Run the upgrade with your updated values file:

```bash
helm upgrade <release-name> graviteeio/apim -f values.yaml
```

Once the Ingress is live, the guided setup of Edge Management proposes its address as the **Reactor URL**. See [Propose the Reactor URL to Edge Management](#propose-the-reactor-url-to-edge-management).

{% hint style="warning" %}
Daemons keep the **Reactor URL** they were installed with. A **Reactor URL** changed after the setup only applies to the daemons installed after the change, so decide the host before you install the daemons. See [Change the gateway addresses](set-up-edge-management.md#change-the-gateway-addresses).
{% endhint %}

## Propose the Reactor URL to Edge Management

Your installation proposes a **Reactor URL** to an environment of Edge Management when one of the following settings gives an address for it. The guided setup fills in an empty **Reactor URL** with it, and the **Gateway** page shows it under the field when it differs from the address in the field. A proposed address never replaces a saved one.

### Propose the address of the Edge ingress

When the chart creates the Edge ingress and the ingress has at least one host, the chart proposes the address of the ingress to every environment. It builds the address from `https://`, the first host of `hosts`, and `path` without its trailing slash, for example `https://apim-edge.example.com`. The chart proposes it only when the same release deploys the gateway and the Management API.

To propose the address with another scheme, set `scheme` on the ingress:

```yaml
gateway:
  services:
    edge:
      ingress:
        scheme: http
```

### Propose an address per environment

To propose a different address to each environment, list the environments under `installation.standalone.edge-reactor` in your `values.yaml`:

```yaml
installation:
  standalone:
    edge-reactor:
      urls:
        - envId: DEFAULT
          url: https://edge.example.com
        - envId: <environment ID>
          url: https://edge-prod.example.com
      url: https://edge.example.com
```

The following table describes each field:

| Field  | Description                                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------------- |
| `urls` | The environments, each with the address proposed to it: `envId` is the ID of the environment, and `url` the address. |
| `url`  | The address proposed to the `DEFAULT` environment when `urls` doesn't list it.                                      |

For each environment, the installation proposes the first address that applies:

1. The `url` of the `urls` entry whose `envId` is the ID of the environment.
2. `url`, for the `DEFAULT` environment only.
3. The address of the Edge ingress.

An entry of `urls` without `envId` ends the list, and the entries after it are ignored. The chart doesn't render `installation.standalone.edge-reactor` in a multi-tenant installation.

Without the chart, set the same settings in the `gravitee.yml` of the Management API. There, `installation.edge.reactorUrl` takes the place of the address of the Edge ingress, and is proposed to every environment that `installation.standalone.edge-reactor` doesn't cover:

```yaml
installation:
  edge:
    reactorUrl: https://edge-reactor.example.com
  standalone:
    edge-reactor:
      urls:
        - envId: DEFAULT
          url: https://edge-reactor.example.com
```
