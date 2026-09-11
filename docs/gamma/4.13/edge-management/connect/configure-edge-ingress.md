---
hidden: false
noIndex: false
description: Expose the Edge Reactor port on Kubernetes so the Edge Daemons on your devices reach it. Follow the steps to enable the listener, the service port, and the ingress.
---

# Configure Edge Ingress

## Overview

The Edge Reactor listens on its own port on the gateway, separate from the port that serves your APIs. On Kubernetes, that port isn't exposed by default, so an Edge Daemon can't fetch its configuration or report its heartbeat, its metrics, and its shadow AI detections until you expose it.

Exposing it takes three settings in your `values.yaml`, each of which gates the next:

1. `gateway.edge.enabled` turns the Edge Reactor listener on in the gateway configuration.
2. `gateway.services.edge.enabled` adds the port to the gateway Kubernetes Service.
3. `gateway.services.edge.ingress.enabled` creates the Ingress that routes external traffic to that port.

{% hint style="warning" %}
The Edge Reactor listener is plain HTTP, and the connection between a daemon and the gateway isn't authenticated. Don't expose it to the public internet. Restrict it to a private network, a VPN, or an IP-allowlisted corporate network.
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
| `tls`              | The TLS blocks of the Ingress resource. This terminates TLS at the ingress. The listener behind it is still plain HTTP.             |

## Apply the change

Run the upgrade with your updated values file:

```bash
helm upgrade <release-name> graviteeio/apim -f values.yaml
```

Once the Ingress is live, use that host as the **Reactor URL** of the Edge Management configuration, so the daemons installed on your devices reach it.

{% hint style="warning" %}
The **Reactor URL** is locked once the Edge Management configuration is created, and the daemons already installed hold it in their own configuration. Decide the host before you run the setup. See [Set up Edge Management](set-up-edge-management.md).
{% endhint %}
