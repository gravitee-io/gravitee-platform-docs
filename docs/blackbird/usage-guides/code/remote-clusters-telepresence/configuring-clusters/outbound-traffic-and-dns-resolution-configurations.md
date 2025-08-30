# Outbound Traffic and DNS Resolution Configurations

You can manage how services within a cluster securely connect to external resources by proxying outbound traffic and using Domain Name System (DNS) resolution.

Using this page, you can learn how to:

* [Proxy outbound traffic to a cluster](outbound-traffic-and-dns-resolution-configurations.md#proxy-outbound-traffic-to-a-cluster)
* [Use the DNS resolver](outbound-traffic-and-dns-resolution-configurations.md#use-the-dns-resolver)

## Proxy outbound traffic to a cluster

Connecting to the cluster instead of running an intercept allows you to access cluster workloads as if your laptop was another Pod in the cluster. This allows you to access other Kubernetes services using `<service name>` in the connected namespace and also using `<service name>.<namespace>` to reach services in other namespaces. A service running on your laptop can interact with other services on the cluster by name.

**To proxy outbound traffic:**

1. Run the following command and enter your password to run the daemon.

```shell
blackbird cluster connect --namespace [namespace]
```

2. Run the following command to confirm the connection to your cluster and that it's proxying traffic.

```shell
blackbird cluster status
```

3. Access your service by running a curl command. Blackbird routes the request to the cluster, as if your laptop is running in the cluster.

If you terminate the client with `blackbird cluster quit` and try to access the service again, it will fail because traffic is no longer proxied from your laptop.

> **Note:** When using Blackbird in this way, you need to access services with the namespace-qualified DNS name (`<service name>.<namespace>`) before you start an intercept. After you start an intercept, only `<service name>` is required.

### Control outbound connectivity

#### Connected namespace

The `blackbird cluster connect` command connects to the default namespace (i.e., the namespace that your current Kubernetes context is configured to use, or a namespace named "default"). When connected, you can access all services in this namespace by using a single label name of the service. You can specify which namespace to connect to by adding a `--namespace <name>` to the connect command.

#### Mapped namespaces

By default, Blackbird provides access to all services found in all namespaces in the connected cluster. This can lead to potential issues if the user doesn't have role-based access control (RBAC) permissions to all namespaces. You can use the `--mapped-namespaces <comma separated list of namespaces>` flag to control which namespaces are accessible.

When you use the `--mapped-namespaces` flag, you must include all namespaces containing the services you want to access, as well as all namespaces that contain services related to the intercept.

### Proxy outbound connectivity for local machines

To specify additional hosts or subnets that you want to resolve inside the cluster, you can use the `--also-proxy [string]` flag. This is a comma-separated list of additional IP address ranges that should be routed through a proxy server. When a service attempts to communicate with an IP in these ranges, the traffic will be sent through a proxy.

## Use the DNS resolver

The DNS resolver is dynamically configured to resolve names using the namespaces of active intercepts. Processes running locally on your desktop will have network access to all services in the namespaces by service name only.

Intercepts contribute to the DNS resolver—even those that don't use the `--namespace=<value>` option. This is because `--namespace default` is implied, and in this context, `default` is treated just like any other namespace. No namespaces are used by the DNS resolver (not even `default`) when no intercepts are active, which means that no service is available by service name only. Without an active intercept, the namespace-qualified DNS name must be used in the following way: `<svc-name>.<namespace>`.

In the following example, no intercepts are currently running, so you can connect to the cluster and list the services that can be intercepted.

```
$ blackbird cluster connect

  Connecting to traffic manager...
  Connected to context default (https://<cluster-public-IP>)

$ blackbird cluster list

  web-app-5d568ccc6b   : ready to intercept (traffic-agent not yet installed)
  emoji                : ready to intercept (traffic-agent not yet installed)
  web                  : ready to intercept (traffic-agent not yet installed)
  web-app-5d568ccc6b   : ready to intercept (traffic-agent not yet installed)

$ curl web-app:80

  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="UTF-8">
      <title>Emoji Vote</title>
  ...
```

Using the namespace-qualified DNS name works in this example. Now, you can start an intercept against another service in the same namespace. Note that `--namespace default` is implied since it's not specified.

```
$ blackbird cluster intercept web --port 8080

  Using Deployment web
  intercepted
      Intercept name    : web
      State             : ACTIVE
      Workload kind     : Deployment
      Destination       : 127.0.0.1:8080
      Volume Mount Point: /tmp/telfs-166119801
      Intercepting      : all TCP connections

$ curl webapp:80

  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="UTF-8">
      <title>Emoji Vote</title>
  ...
```

The DNS resolver will also resolve services using `<service-name>.<namespace>`, regardless of which namespace the client is connected to.

## Supported Query Types

The DNS resolver can resolve query types: `A`, `AAAA`, `CNAME`, `MX`, `NS`, `PTR`, `SRV`, and `TXT`.
