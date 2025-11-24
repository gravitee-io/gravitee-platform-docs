---
description: Overview of Cluster.
noIndex: true
---

# Cluster

This reference provides a list of commands, arguments, and flags you can use to work with Blackbird clusters (powered by Telepresence).

If you're a former Telepresence user, consider the following before working with cluster commands:

* You don't need to immediately update your existing scripts that rely on `telepresence` commands. To maintain compatibility, you can run `alias telepresence='blackbird cluster'` in your terminal. This allows your existing scripts to continue working as expected while you transition to Blackbird.
* You must install the latest Blackbird CLI and Traffic Manager. Previously installed Traffic Managers from Telepresence are incompatible. For more information, see [#getting-started-with-the-blackbird-cli](./#getting-started-with-the-blackbird-cli "mention") and [#installing-the-traffic-manager](../../usage-guides/code/remote-clusters-telepresence/using-the-traffic-manager.md#installing-the-traffic-manager "mention").

## blackbird cluster connect

Connect your local workstation to your remote Kubernetes cluster.

```shell
blackbird cluster connect [flags]
```

### Flags

`--allow-conflicting-subnets strings`

Specify a comma-separated list of specific IP address ranges that are explicitly allowed to conflict with the IP ranges used by local subnets in a network. This prevents the system from rejecting the connection or throwing errors.

`--also-proxy strings`

Specify a comma-separated list of additional IP address ranges that should be routed through a proxy server. When a service attempts to communicate with an IP in these ranges, the traffic will be sent through a proxy.

`--as string`

Specify a regular user or a service account in a namespace to impersonate for this operation.

`--as-group stringArray`

Specify a group to impersonate for this operation. You can repeat the flag to specify multiple groups.

`--as-uid string`

Specify a user ID to impersonate for this operation.

`--cache-dir string`

Specify the default directory for caching data.

`--certificate-authority string`

Specify the path to a certificate file within the certificate directory.

`--client-certificate string`

Specify the path to a client certificate file for TLS authentication.

`--client-key string`

Specify the path to a client key file for TLS authentication.

`--cluster string`

Specify the name of the kubeconfig cluster to use for this operation.

`--context string`

Specify the name of the kubeconfig context to use for this operation.

`--disable-compression`

If set to `true`, disable response compression for all requests to the server.

`--docker`

Start or connect to a Docker daemon, which builds, runs, and manages containers.

`--expose stringArray`

Specify one or more ports that a containerized daemon will expose.

`--hostname string`

Specify the hostname used by a containerized daemon that allows it to identify itself within a network or system.

`--insecure-skip-tls-verify`

If set to `true`, skip validation to the server's certificate, making HTTPS connections insecure.

`--kubeconfig string`

Specify the path to the kubeconfig file for CLI requests.

`--manager-namespace string`

The namespace where the Blackbird Traffic Manager is running. This overrides other manager namespaces set in `config`.

`--mapped-namespaces strings`

A comma-separated list of namespaces considered by the domain name system (DNS) and network address translation (NAT) for outbound connections. This defaults to all namespaces.

`--name string`

An optional name to use for the connection.

`--namespace string`

The namespace scope for the CLI request.

`--never-proxy strings`

A comma-separated list of IP address ranges that shouldn't be routed through a proxy server.

`--proxy-via strings`

Locally translate cluster DNS responses matching classless inter-domain routing (CIDR) to virtual IPs that are routed with reverse translation using `WORKLOAD`. The format must be `CIDR=WORKLOAD`, where `CIDR` can be substituted for `service`, `pods`, `also`, or `all`.

`--request-timeout string`

Specify the timeout duration for a single server request, including a time unit (e.g., 1s, 2m, 3h). Use 0 to disable timeouts (default: "0").

`--server string`

Specify the address and port of the Kubernetes API server.

`--tls-server-name string`

Specify the server name for the certificate validation. If not provided, the hostname used to contact the server will be used.

`--token string`

Specify the bearer token for authentication to the API server.

`--user string`

Specify the name of the kubeconfig user to use for this operation.

## blackbird cluster gather-logs

Compile logs from the Traffic Manager, Blackbird Traffic Agent, user daemons, and root daemon, and then export them to a .zip file.

```shell
blackbird cluster gather-logs [flags]
```

### Optional flags

`-a`, `--anonymize`

Replace the actual pod names and namespaces used for the Traffic Manager, and pods containing Traffic Agents in the logs.

`daemons string`

Specify a comma-separated list of daemons you want logs from. The options include: `all`, `root`, `user`, `kubeauth`, or `none`. The default is `all`.

`-y`, `--get-pod-yaml`

Include the YAML for the Traffic Manager and Traffic Agents.

`-o`, `--output-file string`

Specify the file where you want to output the logs.

`--traffic-agents string`

Specify the Traffic Agents you want to collect logs from. The options include: `all,` `name substring`, or `none`. The default is `all`.

`--traffic-manager`

Choose if you want to collect logs from the Traffic Manager. The default is `true`.

## blackbird cluster genyaml

Generate a YAML configuration for the Traffic Agent that can be manually added to existing Kubernetes manifests. This enables integration without requiring automated injection.

To make your modified workload valid, you’ll need to manually add a container, volume, and a configmap entry in blackbird-agents. Use `genyaml config`, `genyaml container`, and `genyaml volume` to generate the required YAML.

> **Note:** We don't recommend this setup unless absolutely necessary. We suggest using Blackbird’s webhook injector to configure Traffic Agents automatically.

```shell
blackbird cluster genyaml [flags]
```

```shell
blackbird cluster genyaml [command]
```

### Flags

`-o`, `--output-file string`

Specify the file where you want to output the YAML. The default is `-`, which directs the output to the standard output (`stdout`).

### Global flags

`--no-report`

Disable anonymous crash reports and log submission on failure.

`--output string`

Specify the output format. Supported values include `JSON`, `YAML`, and `default`. The default is `default`.

`--use string`

Specify a Match expression that uniquely identifies the daemon container.

### Commands

`config`

Generate YAML for the Traffic Agent's entry in the configuration map.

`container`

Generate YAML for the Traffic Agent container configuration.

`initcontainer`

Generate YAML for the Traffic Agent initContainer configuration.

`volume`

Generate YAML for the Traffic Agent volume configuration.

## blackbird cluster helm install

Install a Traffic Manager to send or receive cloud traffic in your cluster.

```shell
blackbird cluster helm install [flags]
```

### Flags

`--allow-conflicting-subnets strings`

Specify a comma-separated list of CIDR that can conflict with local subnets.

`--also-proxy strings`

Specify an additional comma-separated list of CIDR to proxy.

`--as string`

Specify the username to impersonate for the operation. This can be a regular user or a service account in a namespace.

`--as-group stringArray`

Specify the group to impersonate for the operation. You can repeat this flag to specify multiple groups.

`--as-uid string`

Specify the user ID to impersonate for the operation.

`--cache-dir string`

Specify the default cache directory. The default is: `$HOME/.kube/cache`.

`--certificate-authority string`

Specify the SpecPath to a certificate file for the certificate authority.

`--client-certificate string`

Specify the path to a certificate file for the certificate authority.

`--client-key string`

Specify the path to a client certificate file for TLS authentication.

`--cluster string`

Specify the name of the kubeconfig cluster you want to use.

`--context string`

Specify the name of the kubeconfig context you want to use.

`--crds`

Use this flag to only install the CRDs.

`--create-namespace`

Use this flag to create a namespace for the Traffic Manager if it's not present. The default is `true`.

`--disable-compression`

If set to `true`, you'll opt out of response compression for all requests to the server.

`--docker`

Use this flag to start or connect to a daemon in the Docker container.

`--expose stringArray`

Specify the port that a containerized daemon will expose. You can repeat this flag.

`--hostname string`

Specify the hostname used by a containerized daemon.

`--insecure-skip-tls-verify`

If set to `true`, the server's certificate will not be checked for validity. This will make your HTTPS connections insecure.

`--kubeconfig string`

Specify the path to the kubeconfig file to use for CLI requests.

`--manager-namespace string`

Specify the namespace where the Traffic Manager is located. This flag overrides any other manager namespace set in config.

`--mapped-namespaces strings`

Specify a comma-separated list of namespaces considered by DNS resolver and NAT for outbound connections. This defaults to all namespaces.

`--name string`

Specify an optional name to use for the connection.

`-n`, `--namespace string`

Specify an optional namespace scope for this CLI request.

`--never-proxy strings`

Specify a comma-separated list of CIDR you never want to proxy.

`--no-hooks`

Prevent hooks from running during the installation.

`--proxy-via strings`

Locally translate cluster DNS responses matching CIDR to virtual IPs that are routed with reverse translation using `WORKLOAD`. The format must be `CIDR=WORKLOAD`, where `CIDR` can be substituted for `service`, `pods`, `also`, or `all`.

`--request-timeout string`

Specify the timeout duration for a single server request, including a time unit (e.g., 1s, 2m, 3h). Use 0 to disable timeouts (default: "0").

`-s`, `--server string`

Specify the address and port of the Kubernetes API server.

`--set stringArray`

Specify a value as a.b=v. You can specify multiple or separate values with commas: `a.b=v1,a.c=v2`.

`--set-file stringArray`

Set values from respective files specified using the command line. You can specify multiple or separate values with commas: `key1=path1,key2=path2`.

`--set-json stringArray`

Set JSON values on the command line. You can specify multiple or separate values with commas: `a.b=jsonval1,a.c=jsonval2`.

`--set-string stringArray`

Set string values on the command line. You can specify multiple or separate values with commas: `a.b=val1,a.c=val2`.

`--tls-server-name string`

Specify the server name to use for server certificate validation. If it's not provided, the hostname used to contact the server will be used.

`--token string`

Specify the bearer token for authentication to the API server.

`--user string`

Specify the name of the kubeconfig user to use.

`-f`, `--values stringArray`

Specify values in a YAML file or a URL. You can specify multiple values.

## blackbird cluster helm uninstall

Uninstall the Traffic manager and all installed agents.

```shell
blackbird cluster helm uninstall [flags]
```

### Flags

`--allow-conflicting-subnets strings`

Specify a comma-separated list of CIDR that can conflict with local subnets.

`--also-proxy strings`

Specify an additional comma-separated list of CIDR to proxy.

`--as string`

Specify the username to impersonate for the operation. This can be a regular user or a service account in a namespace.

`--as-group stringArray`

Specify the group to impersonate for the operation. You can repeat this flag to specify multiple groups.

`--as-uid string`

Specify the user ID to impersonate for the operation.

`--cache-dir string`

Specify the default cache directory The default is: `$HOME/.kube/cache`.

`--certificate-authority string`

Specify the SpecPath to a certificate file for the certificate authority.

`--client-certificate string`

Specify the path to a certificate file for the certificate authority.

`--client-key string`

Specify the path to a client certificate file for TLS authentication.

`--cluster string`

Specify the name of the kubeconfig cluster you want to use.

`--context string`

Specify the name of the kubeconfig context you want to use.

`--crds`

Use this flag to only install the CRDs.

`--disable-compression`

If set to `true`, you'll opt out of response compression for all requests to the server.

`--docker`

Use this flag to start or connect to a daemon in the Docker container.

`--expose stringArray`

Specify the port that a containerized daemon will expose. You can repeat this flag.

`--hostname string`

Specify the hostname used by a containerized daemon.

`--insecure-skip-tls-verify`

If set to `true`, the server's certificate will not be checked for validity. This will make your HTTPS connections insecure.

`--kubeconfig string`

Specify the path to the kubeconfig file to use for CLI requests.

`--manager-namespace string`

Specify the namespace where the Traffic Manager is located. This flag overrides any other manager namespace set in config.

`--mapped-namespaces strings`

Specify a comma-separated list of namespaces considered by DNS resolver and NAT for outbound connections. This defaults to all namespaces.

`--name string`

Specify an optional name to use for the connection.

`-n`, `--namespace string`

Specify an optional namespace scope for this CLI request.

`--never-proxy strings`

Specify a comma-separated list of CIDR you never want to proxy.

`--no-hooks`

Prevent hooks from running during the installation.

`--proxy-via strings`

Locally translate cluster DNS responses matching CIDR to virtual IPs that are routed with reverse translation using `WORKLOAD`. The format must be `CIDR=WORKLOAD`, where `CIDR` can be substituted for `service`, `pods`, `also`, or `all`.

`--request-timeout string`

Specify the timeout duration for a single server request, including a time unit (e.g., 1s, 2m, 3h). Use 0 to disable timeouts (default: "0").

`-s`, `--server string`

Specify the address and port of the Kubernetes API server.

`--tls-server-name string`

Specify the server name to use for server certificate validation. If it's not provided, the hostname used to contact the server will be used.

`--token string`

Specify the bearer token for authentication to the API server.

`--user string`

Specify the name of the kubeconfig user to use.

## blackbird cluster helm upgrade

Upgrade the Traffic Manager to a newer version.

```shell
blackbird cluster helm upgrade [flags]
```

### Flags

`--allow-conflicting-subnets strings`

Specify a comma-separated list of CIDR that can conflict with local subnets.

`--also-proxy strings`

Specify additional comma-separated list of CIDR to proxy.

`--as string`

Specify the username to impersonate for the operation. This can be a regular user or a service account in a namespace.

`--as-group stringArray`

Specify the group to impersonate for the operation. You can repeat this flag to specify multiple groups.

`--as-uid string`

Specify the user ID to impersonate for the operation.

`--cache-dir string`

Specify the default cache directory. The default is: `$HOME/.kube/cache`.

`--certificate-authority string`

Specify the SpecPath to a certificate file for the certificate authority.

`--client-certificate string`

Specify the path to a certificate file for the certificate authority.

`--client-key string`

Specify the path to a client certificate file for TLS authentication.

`--cluster string`

Specify the name of the kubeconfig cluster you want to use.

`--context string`

Specify the name of the kubeconfig context you want to use.

`--crds`

Use this flag to only install the CRDs.

`--create-namespace`

Use this flag to create a namespace for the Traffic Manager if it's not present. The default is `true`.

`--disable-compression`

If set to `true`, you'll opt out of response compression for all requests to the server.

`--docker`

Use this flag to start or connect to a daemon in the Docker container.

`--expose stringArray`

Specify the port that a containerized daemon will expose. You can repeat this flag.

`--hostname string`

Specify the hostname used by a containerized daemon.

`--insecure-skip-tls-verify`

If set to `true`, the server's certificate will not be checked for validity. This will make your HTTPS connections insecure.

`--kubeconfig string`

Specify the path to the kubeconfig file to use for CLI requests.

`--manager-namespace string`

Specify the namespace where the Traffic Manager is located. This flag overrides any other manager namespace set in config.

`--mapped-namespaces strings`

Specify a comma-separated list of namespaces considered by DNS resolver and NAT for outbound connections. This defaults to all namespaces.

`--name string`

Specify an optional name to use for the connection.

`-n`, `--namespace string`

Specify an optional namespace scope for this CLI request.

`--never-proxy strings`

Specify a comma-separated list of CIDR you never want to proxy.

`--no-hooks`

Prevent hooks from running during the installation.

`--proxy-via strings`

Locally translate cluster DNS responses matching CIDR to virtual IPs that are routed with reverse translation using `WORKLOAD`. The format must be `CIDR=WORKLOAD`, where `CIDR` can be substituted for `service`, `pods`, `also`, or `all`.

`--request-timeout string`

Specify the timeout duration for a single server request, including a time unit (e.g., 1s, 2m, 3h). Use 0 to disable timeouts (default: "0").

`--reset-values`

When upgrading the Traffic Manager, reset the values to the values built into the Helm chart.

`--reuse-values`

When upgrading the Traffic Manager, reuse the release's values and merge in overrides from the command line using `--set` and `-f`.

`-s`, `--server string`

Specify the address and port of the Kubernetes API server.

`--set stringArray`

Specify a value as a.b=v. You can specify multiple or separate values with commas: `a.b=v1,a.c=v2`.

`--set-file stringArray`

Set values from respective files specified using the command line. You can specify multiple or separate values with commas: `key1=path1,key2=path2`.

`--set-json stringArray`

Set JSON values on the command line. You can specify multiple or separate values with commas: `a.b=jsonval1,a.c=jsonval2`.

`--set-string stringArray`

Set string values on the command line. You can specify multiple or separate values with commas: `a.b=val1,a.c=val2`.

`--tls-server-name string`

Specify the server name to use for server certificate validation. If it's not provided, the hostname used to contact the server will be used.

`--token string`

Specify the bearer token for authentication to the API server.

`--user string`

Specify the name of the kubeconfig user to use.

`-f`, `--values stringArray`

Specify values in a YAML file or a URL. You can specify multiple values.

## blackbird cluster intercept

Redirect traffic from a specific Kubernetes service to your local workstation.

```shell
blackbird cluster intercept [flags]
```

### Flags

`--address string`

Specify the local address where you want to forward traffic. You must use a value (e.g., `--address 10.0.0.2`). The default is `127.0.0.1`.

`--detailed-output`

Detailed information about the intercept when used with `--output=json` or `--output=yaml`.

`--docker-build string`

Specify a path or URL to a Docker container from Docker context and run it with an intercepted environment and volume mounts.

`--docker-build-opt stringArray`

Specify one or more Docker project settings using key-value pairs (e.g., `--docker-build-opt tag=mytag`).

`--docker-debug string`

Specify a debugger to run inside a container with relaxed security.

`--docker-mount string`

Specify the volume mount point in Docker. The default is the same as `--mount`.

`--docker-run`

Run a Docker container with an intercepted environment and volume mount.

`-e`, `--env-file string`

Save or export the settings, variables, or configurations into a file. You can determine the syntax used in the file using the `--env-syntax` flag.

`-j`, `--env-json string`

Save or export the remote environment to a file as a JSON Blob (binary large object).

`--env-syntax string`

Specify the syntax used for the `env-file`. The options include `docker`, `compose`, `sh`, `csh`, `cmd`, and `ps`. The following options can use the `:export` option: `sh`, `chs`, `ps`.

`--http-header stringArray`

Intercept traffic that matches the `HTTP2_HEADER=REGEXP` specifier. Instead of a `--http-header=HTTP2_HEADER=REGEXP` pair, you could use `--http-header=auto`, which will automatically select a unique matcher for your intercept. If you provide the flag multiple times, it will only intercept traffic that matches all of the specifiers.

`--http-meta stringArray`

Associate key-value pairs with an intercept that can later be retrieved using the Telepresence API service.

`--http-path-equal string`

Intercept traffic that matches this exact path, ignoring the query string.

`--http-path-prefix string`

Intercept traffic with paths beginning with this prefix.

`--http-path-regexp string`

Intercept traffic only if the path fully matches this regular expression, ignoring the query string.

`--http-plaintext`

Use plain text format to communicate with the interceptor process on the local workstation. This is only relevant for intercepting workloads annotated with `getambassador.io/inject-originating-tls-secret` to disable TLS during intercepts.

`--ingress-host string`

Specify the hostname that the ingress controller uses to route traffic.

`--ingress-l5 string`

Specify the Layer 5 (L5) hostname for ingress routing. This is a logical service name used for application-layer traffic management.

`--ingress-port int32`

Specify the port number for ingress traffic (integer value). This determines the port on which the ingress controller listens for incoming requests.

`--ingress-tls`

Enable or disable TLS encryption for ingress traffic. When enabled, traffic will be secured using HTTPS.

`--local-mount-port uint16`

Instead of mounting a remote folder to your computer, set up a local connection using a specified port.

`--mechanism mechanism`

Specify which method of communication to use. By default, this is Transmission Control Protocol (TCP).

`--mount string`

Specify the absolute path for the root directory where volumes will be mounted (`$TELEPRESENCE_ROOT`). Set to `true` to mount to a random mount point, and use `false` to disable filesystem mounting. The default is `true`.

`-p`, `--port string`

Specify the local port you want to use. If you're intercepting a service with multiple ports, use `<local port>:<svcPortIdentifier>`, where the identifier is the port name or port number. With `--docker-run` and a daemon that doesn't run in Docker, use `<local port>:<container port>` or `<local port>:<container port>:<svcPortIdentifier>`.

`--replace`

Specify if the Traffic Agent should replace application containers in workload pods. The default behavior is for the sidecar to install with existing containers.

`--service string`

Specify the name of the service you want to intercept. If you don't provide one, Blackbird will attempt to automatically detect a service.

`--to-pod strings`

An additional port you want to use. The pod's port will be accessible on your computer at `localhost:PORT`, so you can interact with it as if it's running locally.

`--use-saved-intercept`

Use a saved intercept.

`--wait-message string`

Specify the text that will appear to confirm that the intercept process has begun.

`-w`, `--workload string`

Specify the name of the workload you want to intercept.

## blackbird cluster leave

Stop and remove an existing intercept.

```shell
blackbird cluster leave <intercept name>
```

## blackbird cluster list

List all current intercepts.

```shell
blackbird cluster list [flags]
```

### Flags

`-a`, `--agents`

List intercepts with installed agents only.

`--debug`

Include debugging information.

`-i`, `--intercepts`

List intercepts only.

`-n`, `--namespace string`

Specify the namespace scope.

`-o`, `--only-interceptable`

List interceptable workloads only.

## blackbird cluster list-contexts

List the available cluster contexts. Contexts define which cluster and user credentials the CLI is using.

```shell
blackbird cluster list-contexts
```

## blackbird cluster list-namespaces

List all namespaces in the cluster. Namespaces help organize resources and manage access.

```shell
blackbird cluster list-namespaces
```

## blackbird cluster loglevel

Temporarily adjust how much detail the system logs for the Traffic Manager, Traffic Agent, root daemons, and user daemons. Increasing the log level can help with troubleshooting by showing more details, while lowering it can reduce unnecessary log messages.

```shell
blackbird cluster loglevel [flags]
```

### Flags

`-d`, `--duration duration`

Specify the duration the log level will remain in effect. If the time is set to 0 seconds (0s), the log level will remain in effect indefinitely until manually changed. By default, the duration is 30 minutes (30m0s).

`-l`, `--local-only`

Provide the logs for the user and root daemons only.

`-r`, `--remote-only`

Provide the logs for the Traffic Manager and Traffic Agents.

## blackbird cluster quit

Stop the daemon process.

```shell
blackbird cluster quit [flags]
```

### Flags

`-s`, `--stop-daemons`

Stop all local daemons.

## blackbird cluster status

Display information about how different components in the cluster are communicating with each other. This can help identify issues such as network failures, misconfigurations, or connectivity issues.

```shell
blackbird cluster status [flags]
```

### Flags

`--multi-daemon`

Use a multi-daemon format, even if there's only one daemon connected.

## blackbird cluster uninstall

Uninstall Traffic Agents from your cluster.

```shell
blackbird cluster uninstall [flags] { --agent <agents...> | --all-agents }
```

### Flags

`--agent`

Remove the Traffic Agent for a specific workload.

`--all-agents`

Remove all Traffic Agents from all workloads.

## blackbird cluster config view

View the current cluster configuration.

```shell
blackbird cluster config view
```
