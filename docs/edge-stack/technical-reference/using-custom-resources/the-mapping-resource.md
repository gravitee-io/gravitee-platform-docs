---
noIndex: true
---

# The Mapping Resource

## Introduction to the Mapping resource

Ambassador Edge Stack is designed around a [declarative, self-service management model](../../core-concepts/the-ambassador-operating-model-gitops-and-continuous-delivery.md). The core resource used to support application development teams who need to manage the edge with Ambassador Edge Stack is the `Mapping` resource.

{% hint style="warning" %}
Remember that `Listener` and `Host` resources are  required for a functioning Ambassador Edge Stack installation that can route traffic!\
Learn more about `Listener`: [the-listener-resource.md](the-listener-resource.md "mention")\
Learn more about `Host`: [the-host-resource.md](the-host-resource.md "mention")
{% endhint %}

### Quick example

At its core a `Mapping` resource maps a `resource` to a `service`:

| Required attribute                            | Description                                                                                                                                                                                                              |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                                        | is a string identifying the `Mapping` (e.g. in diagnostics)                                                                                                                                                              |
| [`prefix`](the-mapping-resource.md#resources) | is the URL prefix identifying your [resource](the-mapping-resource.md#resources)                                                                                                                                         |
| [`service`](the-mapping-resource.md#services) | is the name of the [service](the-mapping-resource.md#services) handling the resource; must include the namespace (e.g. `myservice.othernamespace`) if the service is in a different namespace than Ambassador Edge Stack |

These resources are defined as Kubernetes Custom Resource Definitions. Here's a simple example that maps all requests to `/httpbin/` to the `httpbin.org` web service:

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind:  Mapping
metadata:
  name:  httpbin-mapping
spec:
  prefix: /httpbin/
  service: http://httpbin.org
```

### Applying a Mapping resource

A `Mapping` resource can be managed using the same workflow as any other Kubernetes resources (e.g., `service`, `deployment`). For example, if the above `Mapping` is saved into a file called `httpbin-mapping.yaml`, the following command will apply the configuration directly to Ambassador Edge Stack:

```
kubectl apply -f httpbin-mapping.yaml
```

For production use, the general recommended best practice is to store the file in a version control system and apply the changes with a continuous deployment pipeline. For more detail, see the [Ambassador Operating Model](../../core-concepts/the-ambassador-operating-model-gitops-and-continuous-delivery.md).

### Extending Mappings

`Mapping` resources support a rich set of annotations to customize the specific routing behavior. Here's an example service for implementing the CQRS pattern (using HTTP):

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind:  Mapping
metadata:
  name:  cqrs-get
spec:
  prefix: /cqrs/
  method: GET
  service: getcqrs
---
apiVersion: getambassador.io/v3alpha1
kind:  Mapping
metadata:
  name:  cqrs-put
spec:
  prefix: /cqrs/
  method: PUT
  service: putcqrs
```

More detail on each of the available annotations are discussed in subsequent sections.

### Resources

To Ambassador Edge Stack, a `resource` is a group of one or more URLs that all share a common prefix in the URL path. For example:

```
https://ambassador.example.com/resource1/foo
https://ambassador.example.com/resource1/bar
https://ambassador.example.com/resource1/baz/zing
https://ambassador.example.com/resource1/baz/zung
```

all share the `/resource1/` path prefix, so it can be considered a single resource. On the other hand:

```
https://ambassador.example.com/resource1/foo
https://ambassador.example.com/resource2/bar
https://ambassador.example.com/resource3/baz/zing
https://ambassador.example.com/resource4/baz/zung
```

share only the prefix `/` -- you _could_ tell Ambassador Edge Stack to treat them as a single resource, but it's probably not terribly useful.

Note that the length of the prefix doesn't matter: if you want to use prefixes like `/v1/this/is/my/very/long/resource/name/`, go right ahead, Ambassador Edge Stack can handle it.

Also note that Ambassador Edge Stack does not actually require the prefix to start and end with `/` -- however, in practice, it's a good idea. Specifying a prefix of

```
/man
```

would match all of the following:

```
https://ambassador.example.com/man/foo
https://ambassador.example.com/mankind
https://ambassador.example.com/man-it-is/really-hot-today
https://ambassador.example.com/manohmanohman
```

which is probably not what was intended.

### Services

Ambassador Edge Stack routes traffic to a `service`. A `service` is defined as:

```
[scheme://]service[.namespace][:port]
```

Where everything except for the `service` is optional.

* `scheme` can be either `http` or `https`; if not present, the default is `http`.
* `service` is the name of a service (typically the service name in Kubernetes or Consul); it is not allowed to contain the `.` character.
* `namespace` is the namespace in which the service is running. Starting with Ambassador Edge Stack 1.0.0, if not supplied, it defaults to the namespace in which the Mapping resource is defined. The default behavior can be configured using the [`ambassador` Module](the-module-resource.md). When using a Consul resolver, `namespace` is not allowed.
* `port` is the port to which a request should be sent. If not specified, it defaults to `80` when the scheme is `http` or `443` when the scheme is `https`. Note that the [resolver](docs/edge-stack/technical-reference/ingress-and-load-balancing/service-discovery-and-resolvers.md) may return a port in which case the `port` setting is ignored.

Note that while using `service.namespace.svc.cluster.local` may work for Kubernetes resolvers, the preferred syntax is `service.namespace`.

### Best practices for configuration

Ambassador Edge Stack's configuration is assembled from multiple YAML blocks which are managed by independent application teams. This implies:

*   Ambassador Edge Stack's configuration should be under version control.

    While you can always read back the Ambassador Edge Stack's configuration from Kubernetes or its diagnostic service, the Ambassador Edge Stack will not do versioning for you.
*   Be aware that the Ambassador Edge Stack tries to not start with a broken configuration, but it's not perfect.

    Gross errors will result in Ambassador Edge Stack refusing to start, in which case `kubectl logs` will be helpful. However, it's always possible to e.g. map a resource to the wrong service, or use the wrong `rewrite` rules. Ambassador Edge Stack can't detect that on its own, although its diagnostic pages can help you figure it out.
*   Be careful of mapping collisions.

    If two different developers try to map `/user/` to something, this can lead to unexpected behavior. Ambassador Edge Stack's canary-deployment logic means that it's more likely that traffic will be split between them than that it will throw an error -- again, the diagnostic service can help you here.

**Note:** Unless specified, mapping attributes cannot be applied to any other resource type.
