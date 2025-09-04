---
noIndex: true
---

# Local Machine Configurations

Blackbird cluster (powered by Telepresence) can be configured using various settings. You can configure these settings in two ways:

* [Globally](local-machine-configurations.md#global-configurations): These can be done by a platform engineer with deployment access to the Traffic Manager.
* [Locally](local-machine-configurations.md#local-configurations): These can be done by any user.

**Note:** If the Traffic Manager's location is different from the default (`ambassador`), it must be set locally per cluster to ensure connectivity.

## Global configurations

Global configurations are set at the Traffic Manager level and apply to any user connecting to that Traffic Manager. To set them, pass a `client` dictionary to the `blackbird cluster helm install` command with any config values. The `client` config supports values for [dns](local-machine-configurations.md#dns), [grpc](local-machine-configurations.md#grpc), [images](local-machine-configurations.md#images), [logLevels](local-machine-configurations.md#log-levels), [routing](local-machine-configurations.md#routing), [telepresenceAPI](local-machine-configurations.md#telepresenceapi), and [timeouts](local-machine-configurations.md#timeouts).

The following example shows standard configuration conventions.

```yaml
client:
  timeouts:
    intercept: 10s
  logLevels:
    userDaemon: debug
  grpc:
    maxReceiveSize: 10Mi
  telepresenceAPI:
    port: 9980
  dns:
    includeSuffixes: [.private]
    excludeSuffixes: [.se, .com, .io, .net, .org, .ru]
    lookupTimeout: 30s
  routing:
      alsoProxySubnets:
        - 1.2.3.4/32
      neverProxySubnets:
      - 1.2.3.4/32
```

### DNS

This configuration provides options for configuring the DNS resolution behavior in a client application or system. The following is a summary of the available fields.

| Field             | Description                                                                                                                                                               | Type                                                                                       | Default                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| `localIP`         | The address of the local DNS server. This entry is only used on Linux systems that aren't configured to use `systemd-resolved`.                                           | IP address [string](https://yaml.org/type/str.html)                                        | first `nameserver` mentioned in `/etc/resolv.conf` |
| `excludeSuffixes` | The suffixes for which the DNS resolver will always fail (or fallback, in case of the overriding resolver). It can be globally configured in the Helm chart.              | [sequence](https://yaml.org/type/seq.html) of [strings](https://yaml.org/type/str.html)    | `[".arpa", ".com", ".io", ".net", ".org", ".ru"]`  |
| `includeSuffixes` | The suffixes for which the DNS resolver will always attempt to do a lookup. Includes have higher priority than excludes. It can be globally configured in the Helm chart. | [sequence](https://yaml.org/type/seq.html) of [strings](https://yaml.org/type/str.html)    | `[]`                                               |
| `excludes`        | The names to be excluded by the DNS resolver.                                                                                                                             | `[]`                                                                                       |                                                    |
| `mappings`        | The names to be resolved to other names (CNAME records) or to explicit IP addresses.                                                                                      | `[]`                                                                                       |                                                    |
| `lookupTimeout`   | The maximum time to wait for a side host lookup.                                                                                                                          | [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 4 seconds                                          |

The following is an example values.yaml.

```yaml
client:
  dns:
    includeSuffixes: [.private]
    excludeSuffixes: [.se, .com, .io, .net, .org, .ru]
    localIP: 8.8.8.8
    lookupTimeout: 30s
```

#### Mappings

Mappings allow you to map hostnames to aliases or IP addresses. You can use this when you want an alternative name for a service in the , or when you want the DNS resolver to map a name to an IP address of your choice.

In the given , the service named `postgres` is located within a separate namespace titled `big-data`, and it's referred to as `psql`.

```yaml
dns:
  mappings:
    - name: postgres
      aliasFor: psql.big-data
    - name: my.own.domain
      aliasFor: 192.168.0.15
```

#### Excludes

Lists service names that you want to exclude from the Blackbird DNS server. You can use this when you want your application to interact with a local service instead of a service. In the following example, "redis" is resolved locally instead of by the .

```yaml
dns:
  excludes:
    - redis
```

### gRPC

The `maxReceiveSize` determines the size of a message that the workstation receives using gRPC. The default is 4Mi, which is determined by gRPC. All traffic to and from the cluster is tunneled using gRPC.

The size is measured in bytes. You can express it as a plain integer or as a fixed-point number using E, G, M, or K. You can also use the power-of-two equivalents: Gi, Mi, Ki. The following example represents approximately the same value.

```
128974848, 129e6, 129M, 123Mi
```

### Images

The values for `client.images` are strings. These values affect the objects that are deployed in the cluster, so it's important to ensure users have the same configuration.

The following are valid fields for the `client.images` key.

| Field         | Description                                                                                       | Type                                                                 | Default                             |
| ------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ----------------------------------- |
| `registry`    | The Docker registry you want to use for installing the Traffic Manager and default Traffic Agent. | Docker registry name [string](https://yaml.org/type/str.html)        | `docker.io/datawire`                |
| `agentImage`  | `$registry/$imageName:$imageTag` to use when installing the Traffic Agent.                        | qualified Docker image name [string](https://yaml.org/type/str.html) | (unset)                             |
| `clientImage` | `$registry/$imageName:$imageTag` to use locally when connecting with `--docker`.                  | qualified Docker image name [string](https://yaml.org/type/str.html) | `$registry/ambassador-telepresence` |

### Intercept

This configuration controls apply how Telepresence intercepts the communications to the intercepted service.

| Field                 | Description                                                                                                                                 | Type                | Default      |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------ |
| `appProtocolStrategy` | Controls how Blackbird selects the application protocol to use when intercepting a service that has no defined `service.ports.appProtocol`. | appProtocolStrategy | `http2Probe` |
| `defaultPort`         | Controls which port is selected when no `--port` flag is given to the `blackbird cluster intercept` command.                                | int                 | 8080         |
| `useFtp`              | Use FuseFTP (Filesystem in Userspace) instead of SSHFS (SSH Filesystem) when mounting remote file systems.                                  | boolean             | false        |

`appProtocolStrategy` is only relevant when using personal intercepts. The following are valid values.

| Value        | Resulting action                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------- |
| `http2Probe` | The Blackbird Traffic Agent probes the intercepted container to check whether it supports HTTP/2. |
| `portName`   | Blackbird assumes the protocol based on the name of the service port.                             |
| `http`       | Blackbird uses HTTP/1.1.                                                                          |
| `http2`      | Blackbird uses HTTP/2.                                                                            |

When `portName` is used, Blackbird will determine the protocol by the name of the port: `<protocol>[-suffix]`. The following protocols are recognized.

| Protocol | Meaning                                |
| -------- | -------------------------------------- |
| `http`   | Plaintext HTTP/1.1 traffic.            |
| `http2`  | Plaintext HTTP/2 traffic.              |
| `https`  | TLS Encrypted HTTP (1.1 or 2) traffic. |
| `grpc`   | This is the same as HTTP/2.            |

### Log levels

The values for the `client.logLevels` fields include one of the following case-sensitive strings.

* `trace`
* `debug`
* `info`
* `warning` or `warn`
* `error`

For the log level you select, you'll get logs labeled with that level and those of a higher severity. For example, if you use `info`, you'll also get logs labeled `error`, but you won't get logs labeled `debug`.

The following are valid fields for the `client.logLevels` key.

| Field        | Description                                                       | Type                                                                                                                  | Default |
| ------------ | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------- |
| `userDaemon` | Logging level for the user daemon to use (logs to connector.log). | [loglevel](https://github.com/sirupsen/logrus/blob/v1.8.1/logrus.go#L25-L45) [string](https://yaml.org/type/str.html) | debug   |
| `rootDaemon` | Logging level for the root daemon to use (logs to daemon.log).    | [loglevel](https://github.com/sirupsen/logrus/blob/v1.8.1/logrus.go#L25-L45) [string](https://yaml.org/type/str.html) | info    |

### Routing

#### alsoProxySubnets

When using `alsoProxySubnets`, you provide a list of subnets that you want to add to the TUN device. All connections to addresses that the subnet spans will be dispatched to the cluster.

The following example is a values.yaml for the subnet `1.2.3.4/32`.

```yaml
client:
  routing:
    alsoProxySubnets:
      - 1.2.3.4/32
```

#### neverProxySubnets

When using `neverProxySubnets`, you provide a list of subnets. The subnets won't be routed using the TUN device, even if they fall within the subnets (pod or service) for the cluster. Instead, they'll use the route they have before Blackbird connects.

The following is an example kubeconfig for the subnet `1.2.3.4/32`.

```yaml
client:
  routing:
    neverProxySubnets:
      - 1.2.3.4/32
```

#### Using neverProxy together with alsoProxy

neverProxy and alsoProxy are implemented as routing rules, meaning that when the two conflict, regular routing routes apply. Typically, this means that the most specific route will be used.

In the following example, the `alsoProxySubnets` subnet falls within a broader `neverProxySubnets` subnet.

```yaml
neverProxySubnets: [10.0.0.0/16]
alsoProxySubnets: [10.0.5.0/24]
```

The specific `alsoProxySubnets` of `10.0.5.0/24` will be proxied by the TUN device, whereas the rest of `10.0.0.0/16` won't. In the following example, a `neverProxySubnets` subnet is inside a larger `alsoProxySubnets` subnet.

```yaml
alsoProxySubnets: [10.0.0.0/16]
neverProxySubnets: [10.0.5.0/24]
```

Then, all the `alsoProxySubnets` of `10.0.0.0/16` will be proxied, with the exception of the specific `neverProxySubnets` of `10.0.5.0/24`.

### TelepresenceAPI

`client.telepresenceAPI` controls the behavior of Telepresence's RESTful API server that can be queried for additional information about ongoing intercepts. When present, and the `port` is set to a valid port number, it's propagated to the auto-installer so that application containers that can be intercepted get the `TELEPRESENCE_API_PORT` environment set. The server can then be queried at `localhost:<TELEPRESENCE_API_PORT>`. Additionally, the `traffic-agent` and the `user-daemon` on the workstation that performs an intercept will start the server on that port.

If the Traffic Manager is auto-installed, its webhook agent injector will be configured to add the `TELEPRESENCE_API_PORT` environment to the app container when the `traffic-agent` is injected.

### Timeouts

The values for `client.timeouts` are all durations, either as a number of seconds or as a string with a unit suffix of `ms`, `s`, `m`, or `h`. Strings can be fractional (`1.5h`) or combined (`2h45m`).

The following fields are valid for the `timeouts` key.

| Field                   | Description                                                                         | Type                                                                                                                                                                                                | Default    |
| ----------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `clusterConnect`        | Waiting for cluster to be connected.                                                | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 20 seconds |
| `connectivityCheck`     | Timeout used when checking if cluster is already proxied on the workstation.        | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 500 ms     |
| `endpointDial`          | Waiting for a Dial to a service for which the IP is known.                          | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 3 seconds  |
| `roundtripLatency`      | How much to add to the endpointDial timeout when establishing a remote connection.  | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 2 seconds  |
| `intercept`             | Waiting for an intercept to become active.                                          | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 30 seconds |
| `proxyDial`             | Waiting for an outbound connection to be established.                               | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 5 seconds  |
| `trafficManagerConnect` | Waiting for the Traffic Manager API to connect for port forwards.                   | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 60 seconds |
| `trafficManagerAPI`     | Waiting for connection to the gPRC API after `trafficManagerConnect` is successful. | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 15 seconds |
| `helm`                  | Waiting for Helm operations (e.g. `install`) on the Traffic Manager.                | [int](https://yaml.org/type/int.html) or [float](https://yaml.org/type/float.html) number of seconds, or [duration](https://pkg.go.dev/time#ParseDuration) [string](https://yaml.org/type/str.html) | 30 seconds |

## Local configurations

You can override each of these variables at the local level by setting up new values in local config files. There are two types of config values that can be set locally: those that apply to all clusters, which are set in a single `config.yml` file, and those that only apply to specific clusters, which are set as extensions to the `$KUBECONFIG` file.

### Config for all clusters

Blackbird uses a `config.yml` file to store and change the configuration values that will be used for all clusters you use Blackbird with. The location of this file varies based on your OS:

* macOS: `$HOME/Library/Application Support/telepresence/config.yml`
* Linux: `$XDG_CONFIG_HOME/telepresence/config.yml` or, if that variable is not set, `$HOME/.config/telepresence/config.yml`
* Windows: `%APPDATA%\telepresence\config.yml`

For Linux, the above paths are for a user-level configuration. For a system-level configuration, use the file at `$XDG_CONFIG_DIRS/telepresence/config.yml` or, if that variable is empty, `/etc/xdg/telepresence/config.yml`. If a file exists at both the user-level and system-level, the user-level path file will take precedence.

### Values

The config file currently supports values for the [grpc](local-machine-configurations.md#grpc), [images](local-machine-configurations.md#images), [logLevels](local-machine-configurations.md#log-levels), [telepresenceAPI](local-machine-configurations.md#telepresenceapi), and [timeouts](local-machine-configurations.md#timeouts) keys. The definitions of these values are identical to those values in the `client` config above.

The following example shows the conventions of how Blackbird is configured.

```yaml
timeouts:
  intercept: 10s
logLevels:
  userDaemon: debug
images:
  registry: privateRepo # This overrides the default docker.io/datawire repo
  agentImage: ambassador-telepresence-agent:1.8.0 # This overrides the agent image to inject when intercepting
grpc:
  maxReceiveSize: 10Mi
telepresenceAPI:
  port: 9980
```

## Workstation per-cluster configuration

The workstation per-cluster configuration is a configuration that's specific to a cluster and can also be overridden per-workstation by modifying your `$KUBECONFIG` file. We recommend that you don't do this, and instead rely on upstream values provided to the Traffic Manager. This ensures that all users that connect to the Traffic Manager will have the same routing and DNS resolution behavior. An important exception to this is the [`manager.namespace` configuration](local-machine-configurations.md#manager), which must be set locally.

### Values

The kubeconfig supports values for `dns`, `also-proxy`, `never-proxy`, and `manager`.

Example kubeconfig:

```yaml
apiVersion: v1
clusters:
- cluster:
    server: https://127.0.0.1
    extensions:
    - name: telepresence.io
      extension:
        manager:
          namespace: staging
        dns:
          include-suffixes: [.private]
          exclude-suffixes: [.se, .com, .io, .net, .org, .ru]
          local-ip: 8.8.8.8
          lookup-timeout: 30s
        never-proxy: [10.0.0.0/16]
        also-proxy: [10.0.5.0/24]
  name: example-cluster
```

#### Manager

This is the one cluster configuration that can't be set using the Helm chart because it defines how Blackbird connects to the Traffic Manager. When it's not set to `default`, the setting needs to be configured in the workstation's kubeconfig for the cluster. The `manager` key contains configuration settings for finding the `traffic-manager` that Blackbird will connect to. It supports one key, `namespace`, indicating the namespace where the Traffic Manager should be found.

The following is a kubeconfig that will instruct Blackbird to connect to a manager in namespace `staging`.

```yaml
apiVersion: v1
clusters:
  - cluster:
      server: https://127.0.0.1
      extensions:
        - name: telepresence.io
          extension:
            manager:
              namespace: staging
    name: example-cluster
```
