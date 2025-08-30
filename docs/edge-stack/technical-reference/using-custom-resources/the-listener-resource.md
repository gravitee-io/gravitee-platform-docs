# The Listener Resource

## The Listener CRD

The `Listener` CRD defines where and how Ambassador Edge Stack should listen for requests from the network, and which `Host` definitions should be used to process those requests. For additional examples of how to use `Listener`, see [configuring-ambassador-edge-stack-communications.md](../../edge-stack-user-guide/service-routing-and-communication/configuring-ambassador-edge-stack-communications.md "mention").

**A `Listener` is never created by Ambassador Edge Stack and must be defined by the user.** If you don't define a `Listener`, Ambassador Edge Stack won't listen anywhere for connections and will log a `WARNING`.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Listener
metadata:
  name: example-listener
spec:
  port: 8080                     # int32, port number on which to listen
  protocol: HTTPS                # HTTP, HTTPS, HTTPPROXY, HTTPSPROXY, TCP
  securityModel: XFP             # XFP (for X-Forwarded-Proto), SECURE, INSECURE
  statsPrefix: example-listener  # default depends on protocol; see below
  l7Depth: 0                     # int32
  internal_address_config:
    unix_sockets: true
    cidr_ranges:
      - address_prefix: 192.0.0.1
        prefix_len: 24
      - address_prefix: 193.0.0.0
        prefix_len: 24
  hostBinding:
    namespace:
      from: SELF                 # SELF, ALL
    selector: ...                # Kubernetes label selector
```

| Element                   | Type                       | Definition                                                                                                               |
| ------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `port`                    | `int32`                    | The network port on which Ambassador Edge Stack should listen. _Required._                                               |
| `protocol`                | `enum`; see below          | A high-level protocol type, like "HTTPS". _Exactly one of `protocol` and `protocolStack` must be supplied._              |
| `protocolStack`           | array of `enum`; see below | A sequence of low-level protocols to layer together. _Exactly one of `protocol` and `protocolStack` must be supplied._   |
| `securityModel`           | `enum`; see below          | How does Ambassador Edge Stack decide whether requests here are secure? _Required._                                      |
| `statsPrefix`             | `string`; see below        | Under what name do statistics for this `Listener` appear? _Optional; default depends on protocol._                       |
| `l7Depth`                 | `int32`                    | How many layer 7 load balancers are between the edge of the network and Ambassador Edge Stack? _Optional; default is 0._ |
| `hostBinding`             | `struct`, see below        | Mechanism for determining which `Host`s will be associated with this `Listener`. _Required_                              |
| `internal_address_config` | `struct`; see below        | Determines what network addresses are considered internal for statistics and header sanitation purposes.                 |

### `protocol` and `protocolStack`

`protocol` is the **recommended** way to tell Ambassador Edge Stack that a `Listener` expects connections using a well-known protocol. When using `protocol`, `protocolStack` may not also be supplied.

Valid `protocol` values are:

| `protocol`   | Description                                                                                                                                                 |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `HTTP`       | Cleartext-only HTTP. HTTPS is not allowed.                                                                                                                  |
| `HTTPS`      | Either HTTPS or HTTP -- Envoy's TLS support can tell whether or not TLS is in use, and it will set `X-Forwarded-Proto` correctly for later decision-making. |
| `HTTPPROXY`  | Cleartext-only HTTP, using the HAProxy `PROXY` protocol.                                                                                                    |
| `HTTPSPROXY` | Either HTTPS or HTTP, using the HAProxy `PROXY` protocol.                                                                                                   |
| `TCP`        | TCP sessions without HTTP at all. You will need to use `TCPMapping`s to route requests for this `Listener`.                                                 |
| `TLS`        | TLS sessions without HTTP at all. You will need to use `TCPMapping`s to route requests for this `Listener`.                                                 |

### `securityModel`

`securityModel` defines how the `Listener` will decide whether a request is secure or insecure:

| `securityModel` | Description                                                                                                                                |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `XFP`           | Requests are secure if, and only if, `X-Forwarded-Proto` indicates HTTPS. This is common; see below.                                       |
| `SECURE`        | Requests are always secure. You might set this if your load balancer always terminates TLS for you, and you can trust the clients.         |
| `INSECURE`      | Requests are always insecure. You might set this for an HTTP-only `Listener`, or a `Listener` for clients that are expected to be hostile. |

The `X-Forwarded-Proto` header mentioned above is meant to reflect the protocol the _original client_ used to contact Ambassador Edge Stack. When no layer 7 proxies are in use, Envoy will make certain that the `X-Forwarded-Proto` header matches the wire protocol of the connection the client made to Envoy, which allows Ambassador Edge Stack to trust `X-Forwarded-Proto` for routing decisions such as deciding to redirect requests made using HTTP over to HTTPS for greater security. When using Ambassador Edge Stack as an edge proxy or a typical API gateway, this is a desirable configuration; setting `securityModel` to `XFP` makes this easy.

When layer proxies _are_ in use, the `XFP` setting is often still desirable; however, you will also need to set `l7Depth` to allow it to function. See below.

`SECURE` and `INSECURE` are helpful for cases where something downstream of Ambassador Edge Stack should be allowing only one kind of request to reach Ambassador Edge Stack. For example, a `Listener` behind a load balancer that terminates TLS and checks client certificates might use `SecurityModel: SECURE`, then use `Host`s to reject insecure requests if one somehow arrives.

### `l7Depth`

When layer 7 (L7) proxies are in use, the connection to Ambassador Edge Stack comes from the L7 proxy itself rather than from the client. Examining the protocol and IP address of that connection is useless, and instead you need to configure the L7 proxy to pass extra information about the client to Ambassador Edge Stack using the `X-Forwarded-Proto` and `X-Forwarded-For` headers.

However, if Ambassador Edge Stack always trusted `X-Forwarded-Proto` and `X-Forwarded-For`, any client could use them to lie about itself to Ambassador Edge Stack. As a security mechanism, therefore, you must _also_ set `l7Depth` in the `Listener` to the number of trusted L7 proxies in front of Ambassador Edge Stack. If `l7Depth` is not set in the `Listener`, the `xff_num_trusted_hops` value from the `ambassador` `Module` will be used. If neither is set, the default `l7Depth` is 0.

When `l7Depth` is 0, any incoming `X-Forwarded-Proto` is stripped: Envoy always provides an `X-Forwarded-Proto` matching the wire protocol of the incoming connection, so that `X-Forwarded-Proto` can be trusted. When `l7Depth` is non-zero, `X-Forwarded-Proto` is accepted from the L7 proxy, and trusted. The actual wire protocol in use from the L7 proxy to Ambassador Edge Stack is ignored.

`l7Depth` also affects Ambassador Edge Stack's view of the client's source IP address, which is used as the `remote_address` field when rate limiting, and for the `X-Envoy-External-Address` header:

* When `l7Depth` is 0, Ambassador Edge Stack uses the IP address of the incoming connection.
*   When `l7Depth` is some value N that is non-zero, the behavior is determined by the value of `use_remote_address` in the `ambassador` `Module`:

    * When `use_remote_address` is true (the default) then the trusted client address will be the Nth address from the right end of the `X-Forwarded-For` header. (If the XFF contains fewer than N addresses, Envoy falls back to using the immediate downstream connection’s source address as a trusted client address.)
    * When `use_remote_address` is false, the trusted client address is the (N+1)th address from the right end of XFF. (If the XFF contains fewer than N+1 addresses, Envoy falls back to using the immediate downstream connection’s source address as a trusted client address.)

    For more detailed examples of this interaction, refer to [Envoy's documentation](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_conn_man/headers.html#x-forwarded-for).

### `hostBinding`

`hostBinding` specifies how this `Listener` should determine which `Host`s are associated with it:

* `namespace.from` allows filtering `Host`s by the namespace of the `Host`:
  * `namespace.from: SELF` accepts only `Host`s in the same namespace as the `Listener`.
  * `namespace.from: ALL` accepts `Host`s in any namespace.
* `selector` accepts only `Host`s that has labels matching the selector.

`hostBinding` is mandatory, and at least one of `namespace.from` and `selector` must be set. If both are set, both must match for a `Host` to be accepted.

### `statsPrefix`

Ambassador Edge Stack produces detailed [statistics](../../edge-stack-user-guide/service-monitoring/statistics-and-monitoring.md) which can be monitored in a variety of ways. Statistics have hierarchical names, and the `Listener` will cause a set of statistics to be logged under the name specified by `statsPrefix`.

The default `statsPrefix` depends on the protocol for this `Listener`:

* If the `Listener` speaks HTTPS, the default is `ingress-https`.
* Otherwise, if the `Listener` speaks HTTP, the default is `ingress-http`.
* Otherwise, if the `Listener` speaks TLS, the default is `ingress-tls-$port`.
* Otherwise, the default is `ingress-$port`.

Note that it doesn't matter whether you use `protocol` or `protocolStack`: what matters is what protocol is actually configured. Also note that the default doesn't take the HAProxy `PROXY` protocol into account.

The following example uses a `statsPrefix` of `ingress-https`.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Listener
metadata:
  name: example-listener
spec:
  port: 8080
  protocol: HTTPS
  ...
```

The following example uses `statsPrefix` of `ingress-8080`.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Listener
metadata:
  name: example-listener
spec:
  port: 8080
  protocol: TCP
  ...
```

The following example uses `ingress-https`, but it explicitly overrides `statsPrefix` to `proxy-8080`.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Listener
metadata:
  name: example-listener
spec:
  port: 8080
  protocol: HTTPSPROXY
  statsPrefix: proxy-8080
  ...
```

For complete information on which statistics will appear for the `Listener`, see [the Envoy listener statistics documentation](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/stats.html). The following are important statistics:

| Statistic name                                  | Type      | Description                       |
| ----------------------------------------------- | --------- | --------------------------------- |
| `listener.$statsPrefix.downstream_cx_total`     | Counter   | Total connections                 |
| `listener.$statsPrefix.downstream_cx_active`    | Gauge     | Total active connections          |
| `listener.$statsPrefix.downstream_cx_length_ms` | Histogram | Connection length in milliseconds |

### `protocolStack`

**`protocolStack` is not recommended if you can instead use `protocol`.**

Where `protocol` allows configuring the `Listener` to use well-known protocol stacks, `protocolStack` allows configuring exactly which protocols will be layered together. If `protocol` allows what you need, it is safer to use `Protocol` than to risk having the stack broken with an incorrect `protocolStack`.

The possible stack elements are:

| `ProtocolStack` Element | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `HTTP`                  | Cleartext-only HTTP; must be layered with `TLS` for HTTPS |
| `PROXY`                 | The HAProxy `PROXY` protocol                              |
| `TLS`                   | TLS                                                       |
| `TCP`                   | Raw TCP                                                   |

`protocolStack` supplies a list of these elements to describe the protocol stack. **Order matters.** Examples include:

| `protocolStack`            | Description                                                                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| \[ `HTTP`, `TCP` ]         | Cleartext-only HTTP, exactly equivalent to `protocol: HTTP`.                                                                                 |
| \[ `TLS`, `HTTP`, `TCP` ]  | HTTPS or HTTP, exactly equivalent to `protocol: HTTPS`.                                                                                      |
| \[ `PROXY`, `TLS`, `TCP` ] | The `PROXY` protocol, wrapping `TLS` _afterward_, wrapping raw TCP. This isn't equivalent to any `protocol` setting, and may be nonsensical. |

### `internal_address_config`

`internal_address_config` determines what network addresses are considered internal for statistics and header sanitation purposes. If unspecified, only RFC1918 IP addresses will be considered internal.

Example:

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Listener
metadata:
  name: example-listener
spec:
  port: 8080
  protocol: HTTPS
  internal_address_config:
    unix_sockets: true
    cidr_ranges:
      - address_prefix: 192.0.0.1
        prefix_len: 24
      - address_prefix: 193.0.0.0
        prefix_len: 24
  ...
```

## Examples

For additional examples of how to use `Listener`, see [configuring-ambassador-edge-stack-communications.md](../../edge-stack-user-guide/service-routing-and-communication/configuring-ambassador-edge-stack-communications.md "mention").
