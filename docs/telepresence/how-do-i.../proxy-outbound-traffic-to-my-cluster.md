# Proxy outbound traffic to my cluster

While preview URLs are a powerful feature, Telepresence offers other options for proxying traffic between your laptop and the cluster. This section describes how to proxy outbound traffic and control outbound connectivity to your cluster.

{% hint style="info" %}
This guide assumes that you have the [quick start](../) sample web app running in your cluster to test accessing the `web-app` service. You can substitute this service for any other service you are running.
{% endhint %}

### Proxying outbound traffic

Connecting to the cluster instead of running an intercept allows you to access cluster workloads as if your laptop was another pod in the cluster. This enables you to access other Kubernetes services using `<service name>` in the connected namespace and also to use `<service name>.<namespace>` to reach services in other namespaces. A service running on your laptop can interact with other services on the cluster by name.

1.  Run `telepresence connect` and enter your password to run the daemon.

    ```
    $ telepresence connect --namespace emojivoto
    Launching Telepresence User Daemon
    Launching Telepresence Root Daemon
    Connected to context default, namespace default (https://<cluster public IP>)
    ```
2.  Run `telepresence status` to confirm connection to your cluster and that it is proxying traffic.

    ```
    $ telepresence status
    Ambassador Cloud: Connected
    User ID     : 2fbc7882-e308-4be1-a3ac-30875345b803
    Account ID  : e974421e-8dbc-4792-827e-1230a1c807ce
    User Name   : <your user name>
    Email       : <your email>
    Account Name: <name of your account>
    Plan        : Enterprise
    User Daemon: Running
    Version           : v2.19.0
    Executable        : /usr/local/bin/telepresence
    Install ID        : 4b1655a6-7f48-4af3-a6d3-f521bc1d1112
    Status            : Connected
    Kubernetes server : https://<cluster public IP>
    Kubernetes context: default
    Namespace         : emojivoto
    Manager namespace : ambassador
    Intercepts        : 0 total
    Root Daemon: Running
    Version: v2.19.0
    DNS    : 
      Remote IP       : 127.0.0.1
      Exclude suffixes: [.com .io .net .org .ru]
      Include suffixes: []
      Timeout         : 8s
    Subnets: (2 subnets)
      - 10.96.0.0/16
      - 10.244.0.0/24
    Traffic Manager: Connected
    Version      : v2.19.0
    Traffic Agent: docker.io/datawire/ambassador-telepresence-agent:1.14.4
    ```
3.  Access your service by name with `curl web-app:80`. Telepresence routes the request to the cluster, as if your laptop is actually running in the cluster.

    ```
    $ curl web-app:80
    <!DOCTYPE html>
    <html>
    <head>
       <meta charset="UTF-8">
       <title>Emoji Vote</title>
    ...
    ```

If you terminate the client with `telepresence quit` and try to access the service again, it will fail because traffic is no longer proxied from your laptop.

```
  $ telepresence quit
  Disconnected
```

{% hint style="info" %}
When using Telepresence in this way, you need to access services with the namespace qualified DNS name (`<service name>.<namespace>`) before you start an intercept. After you start an intercept, only `<service name>` is required. Read more about these differences in the [DNS resolution reference guide](../).
{% endhint %}

### Controlling outbound connectivity

#### Connected Namespace

The `telepresence connect` command will connect to the default namespace, i.e. the namespace that your current kubernetes context is configured to use, or a namespace named "default". When connected, you can access all services in this namespace by just using a single label name of the service.

You can specify which namespace to connect to by using a `--namespace <name>` to the connect command.

#### Mapped Namespaces

By default, Telepresence provides access to all Services found in all namespaces in the connected cluster. This can lead to problems if the user does not have RBAC access permissions to all namespaces. You can use the `--mapped-namespaces <comma separated list of namespaces>` flag to control which namespaces are accessible.

When you use the `--mapped-namespaces` flag, you need to include all namespaces containing services you want to access, as well as all namespaces that contain services related to the intercept.

#### Proxy outbound connectivity for laptops

To specify additional hosts or subnets that should be resolved inside the cluster, see [AlsoProxy](../technical-reference/laptop-side-configuration.md#alsoproxysubnets) for more details.
