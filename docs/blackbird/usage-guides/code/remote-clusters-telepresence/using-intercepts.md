---
noIndex: true
---

# Using Intercepts

Blackbird cluster (powered by Telepresence) allows you to intercept traffic from a Kubernetes service and route it to your local machine, enabling your local environment to function as if it were running in the cluster. There are two types of intercepts:

* **Global intercept:** This is the default. A global intercept redirects traffic from the Kubernetes service to the version running on your local machine.
* **Personal intercept:** A personal intercept allows you to selectively intercept a portion of traffic to a service without interfering with the rest of traffic. The end user won't experience the change, but you can observe and debug using your development tools. This allows you to share a cluster with others on your team without interfering with their work.

Using this page, you can learn about:

* [Specifying a namespace for an intercept](using-intercepts.md#specifying-a-namespace-for-an-intercept)
* [Creating an intercept](using-intercepts.md#creating-a-global-intercept)
* [Creating a personal intercept](using-intercepts.md#creating-a-personal-intercept)
* [Creating an intercept when the service has multiple ports](using-intercepts.md#creating-an-intercept-when-the-service-has-multiple-ports)
* [Creating an intercept when multiple services match your workload](using-intercepts.md#creating-an-intercept-when-multiple-services-match-your-workload)
* [Intercepting multiple ports](using-intercepts.md#intercepting-multiple-ports)
* [Port-forwarding an intercepted container's sidecars](using-intercepts.md#port-forwarding-an-intercepted-containers-sidecars)
* [Intercepting headless services](using-intercepts.md#intercepting-headless-services)
* [Intercepting without a service](using-intercepts.md#intercepting-without-a-service)
* [Specifying the intercept traffic target](using-intercepts.md#specifying-the-intercept-traffic-target)
* [Environment variables and intercept specifications](using-intercepts.md#environment-variables-and-intercept-specifications)

## Prerequisites

* You downloaded the Blackbird CLI. For more information, see [#getting-started-with-the-blackbird-cli](../../../technical-reference/blackbird-cli/#getting-started-with-the-blackbird-cli "mention").
* You installed the Traffic Manager. For more information, see [using-the-traffic-manager.md](using-the-traffic-manager.md "mention").
* You're connected to a cluster. For more information, see [using-connects.md](using-connects.md "mention").
* You can access a Kubernetes cluster using the Kubernetes CLI (kubectl) or the OpenShift CLI (oc).
* Your application is deployed in the cluster and accessible using a Kubernetes service.
* You have a local copy of the service ready to run on your local machine.

## Specifying a namespace for an intercept

You can specify the name of the namespace when you connect using the `--namespace` option.

```shell
blackbird cluster connect --namespace myns
blackbird cluster intercept hello --port 9000
```

## Importing environment variables

Blackbird can import environment variables from the Pod that's being intercepted. For more information, see [Environment variables](using-intercepts.md#environment-variables).

## Creating a global intercept

The following command redirects all traffic destined for the service to your laptop, acting as a proxy. It includes traffic routed through the ingress controller, so use this option with caution to avoid disrupting production environments.

```shell
blackbird cluster intercept < name> --port=<TCP port>
```

## Creating a personal intercept

The following command creates a personal intercept. Blackbird will then generate a header that uniquely identifies your intercept. Requests that don't contain this header will not be affected by your intercept.

```shell
blackbird cluster intercept < name> --port=<TCP port> --http-header auto
```

This command outputs an HTTP header that you can set on your request for the traffic to be intercepted.

```console
$ blackbird cluster intercept < name> --port=<TCP port> --http-header=auto
Using Deployment <deployment name>
intercepted
    Intercept name: <full name of intercept>
    State         : ACTIVE
     kind : Deployment
    Destination   : 127.0.0.1:<local TCP port>
   Service Port Identifier: proxied
   Volume Mount Point     : /tmp/telfs-3758847665
   Intercepting           : HTTP requests with headers
         'x-telepresence-intercept-id: 101e5551-7471-4991-93db-ba8c6978dc2b:echo-easy'
```

You can then run `blackbird cluster status` to see the list of active intercepts.

```console
$ blackbird cluster status
User Daemon: Running
  Version           : v2.19.0
  Executable        : /usr/local/bin/blackbird
  Install ID        : 4b1658f3-7ff8-4af3-66693-f521bc1da32f
  Status            : Connected
  Kubernetes server : https://cluster public IP>
  Kubernetes context: default
  Namespace         : default
  Manager namespace : ambassador
  Intercepts        : 1 total
    dataprocessingnodeservice: <laptop username>@<laptop name>
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

You can then run `blackbird cluster leave <name of intercept>` to stop the intercept.

## Bypassing the ingress configuration

You can bypass the ingress configuration by setting the relevant parameters using flags. If any of the following flags are set, the dialogue will be skipped and the flag values will be used instead. If any of the required flags are missing, an error will occur.

| Flag             | Description                                                       | Required |
| ---------------- | ----------------------------------------------------------------- | -------- |
| `--ingress-host` | The IP address for the ingress.                                   | yes      |
| `--ingress-port` | The port for the ingress.                                         | yes      |
| `--ingress-tls`  | Whether tls should be used.                                       | no       |
| `--ingress-l5`   | Whether a different ip address should be used in request headers. | no       |

## Creating an intercept when the service has multiple ports

You can intercept a service that has multiple ports by telling Blackbird which service port you want to intercept. Specifically, you can either use the name of the service port or the port number itself. To see which options might be available to you and your service, use kubectl to describe your service or look in the object's YAML. For more information on multiple ports, see [Multi-port services](https://kubernetes.io/docs/concepts/services-networking/service/#multi-port-services) in the Kubernetes documentation.

```console
$ blackbird cluster intercept <base name of intercept> --port=<local TCP port>:<servicePortIdentifier>
Using Deployment <name of deployment>
intercepted
    Intercept name         : <full name of intercept>
    State                  : ACTIVE
     kind          : Deployment
    Destination            : 127.0.0.1:<local TCP port>
    Service Port Identifier: <servicePortIdentifier>
    Intercepting           : all TCP connections
```

When intercepting a service with multiple ports, the intercepted service port name is displayed. To change the intercepted port, create a new intercept using the same method as above. This will update the selected service port.

## Creating an intercept when multiple services match your workload

In many cases, a service has a one-to-one relationship with a , allowing Blackbird to automatically determine which service to intercept based on the targeted . However, when using tools like Argo, multiple services might share the same labels to manage traffic between a canary and a stable service, which can affect auto-detection.

If you know which service you want to use when intercepting a workload, you can use the `--service` flag. Using the example above, if you want to intercept your workload using the `echo-stable` service your command would be as follows.

```console
$ blackbird cluster intercept echo-rollout-<generatedHash> --port <local TCP port> --service echo-stable
Using ReplicaSet echo-rollout-<generatedHash>
intercepted
    Intercept name    : echo-rollout-<generatedHash>
    State             : ACTIVE
    Workload kind     : ReplicaSet
    Destination       : 127.0.0.1:3000
    Volume Mount Point: /var/folders/cp/2r22shfd50d9ymgrw14fd23r0000gp/T/telfs-921196036
    Intercepting      : all TCP connections
```

## Intercepting multiple ports

You can intercept more than one service and/or service port that are using the same workload by creating more than one intercept that identifies the same workload using the `--workload` flag. In the following example, there's a service `multi-echo` with the two ports: `http` and `grpc`. They're both targeting the same `multi-echo` deployment.

```console
$ blackbird cluster intercept multi-echo-http --workload multi-echo --port 8080:http
Using Deployment multi-echo
intercepted
    Intercept name         : multi-echo-http
    State                  : ACTIVE
    Workload kind          : Deployment
    Destination            : 127.0.0.1:8080
    Service Port Identifier: http
    Volume Mount Point     : /tmp/telfs-893700837
    Intercepting           : all TCP requests
$ blackbird cluster intercept multi-echo-grpc --workload multi-echo --port 8443:grpc --mechanism tcp
Using Deployment multi-echo
intercepted
    Intercept name         : multi-echo-grpc
    State                  : ACTIVE
    Workload kind          : Deployment
    Destination            : 127.0.0.1:8443
    Service Port Identifier: extra
    Volume Mount Point     : /tmp/telfs-1277723591
    Intercepting           : all TCP requests
```

## Port-forwarding an intercepted container's sidecars

Sidecars are containers that are in the same Pod as an application container. Typically, they provide auxiliary functionality to an application and can usually be reached at `localhost:${SIDECAR_PORT}`. For example, a common use case for a sidecar is to proxy requests to a database. Your application would connect to `localhost:${SIDECAR_PORT}`, and the sidecar would then connect to the database, possibly augmenting the connection with TLS or authentication.

When intercepting a container that uses sidecars, you might want to have the sidecar ports available to your local application at `localhost:${SIDECAR_PORT}`, as if running in-cluster. Blackbird's `--to-pod ${PORT}` flag implements this behavior, adding port-forwards for the port given.

```console
$ blackbird cluster intercept <base name of intercept> --port=<local TCP port>:<servicePortIdentifier> --to-pod=<sidecarPort>
Using Deployment <name of deployment>
intercepted
    Intercept name         : <full name of intercept>
    State                  : ACTIVE
    Workload kind          : Deployment
    Destination            : 127.0.0.1:<local TCP port>
    Service Port Identifier: <servicePortIdentifier>
    Intercepting           : all TCP connections
```

If there are multiple ports that you need to forward, simply repeat the flag (`--to-pod=<sidecarPort0> --to-pod=<sidecarPort1>`).

## Intercepting headless services

Kubernetes allows you to create services without a ClusterIP. When these services include a Pod selector, they provide a DNS record that directly resolves to the backing Pods.

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: my-headless
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    service: my-headless
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: my-headless
  labels:
    service: my-headless
spec:
  replicas: 1
  serviceName: my-headless
  selector:
    matchLabels:
      service: my-headless
  template:
    metadata:
      labels:
        service: my-headless
    spec:
      containers:
        - name: my-headless
          image: jmalloc/echo-server
          ports:
            - containerPort: 8080
          resources: {}
```

You can intercept it like any other service.

```console
$ blackbird cluster intercept my-headless --port 8080
Using StatefulSet my-headless
intercepted
    Intercept name    : my-headless
    State             : ACTIVE
    Workload kind     : StatefulSet
    Destination       : 127.0.0.1:8080
    Volume Mount Point: /var/folders/j8/kzkn41mx2wsd_ny9hrgd66fc0000gp/T/telfs-524189712
    Intercepting      : all TCP connections
```

> **Note:** This option utilizes an `initContainer` that requires `NET_ADMIN` capabilities. If your cluster administrator has disabled them, you must use numeric ports with the agent injector. This option also requires the Traffic Agent to run as GID `7777`. By default, this is disabled on openshift clusters. To enable running as GID `7777` on a specific OpenShift namespace, run: `oc adm policy add-scc-to-group anyuid system:serviceaccounts:$NAMESPACE`

> **Note:** Blackbird doesn't support intercepting headless services without a selector.

## Intercepting without a service

You can intercept a workload without a service by adding an annotation that informs Blackbird about what container ports are eligible for intercepts. Blackbird will then inject a Traffic Agent when the workload is deployed, and you can intercept the given ports as if they were service ports. The annotation value is a comma-separated list of port identifiers consisting of either the name or the port number of a container port, optionally suffixed with `/TCP` or `/UDP`.

```yaml
      annotations:
        telepresence.getambassador.io/inject-container-ports: http
```

**To intercept without a service:**

1.  Deploy an annotation similar to the following.

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: echo-no-svc
      labels:
        app: echo-no-svc
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: echo-no-svc
      template:
        metadata:
          labels:
            app: echo-no-svc
          annotations:
            telepresence.getambassador.io/inject-container-ports: http
        spec:
          automountServiceAccountToken: false
          containers:
            - name: echo-server
              image: ghcr.io/telepresenceio/echo-server:latest
              ports:
                - name: http
                  containerPort: 8080
              env:
                - name: PORT
                  value: "8080"
              resources:
                limits:
                  cpu: 50m
                  memory: 8Mi
    ```
2.  Connect to the cluster.

    ```console
    $ blackbird cluster connect
    Launching Telepresence User Daemon
    Launching Telepresence Root Daemon
    Connected to context kind-dev, namespace default (https://127.0.0.1:36767)
    ```
3.  List your intercept eligible workloads. If the annotation is correct, the deployment will display in the list.

    ```console
    $ blackbird cluster list
    echo-no-svc: ready to intercept (traffic-agent not yet installed)
    ```
4.  Start a local intercept handler that receives the incoming traffic. The following is an example using a simple Python HTTP service.

    ```console
    $ python3 -m http.server 8080
    ```
5.  Create an intercept.

    ```console
    $ blackbird cluster intercept echo-no-svc
    Using Deployment echo-no-svc
       Intercept name    : echo-no-svc
       State             : ACTIVE
       Workload kind     : Deployment
       Destination       : 127.0.0.1:8080
       Volume Mount Point: /tmp/telfs-3306285526
       Intercepting      : all TCP connections
       Address           : 10.244.0.13:8080
    ```

> **Note:** The response contains an address that you can curl to reach the intercepted pod. You won't be able to curl the name "echo-no-svc". Because there's no service by that name, there's no DNS entry for it.

6.  Curl the intercepted workload.

    ```console
    $ curl 10.244.0.13:8080
    < output from your local service>
    ```

> **Note:** An intercept without a service utilizes an `initContainer` that requires `NET_ADMIN` capabilities. If your cluster administrator has disabled them, you can't intercept services using numeric target ports.

## Specifying the intercept traffic target

By default, your local application is reachable on `127.0.0.1`, and intercepted traffic will be sent to that IP at the port given by `--port`. If you want to change this behavior and send traffic to a different IP address, you can use the `--address` parameter to `blackbird cluster intercept`. For example, if your local machine is configured to respond to HTTP requests for an intercept on `172.16.0.19:8080`, you would use the following.

```console
$ blackbird cluster intercept my-service --address 172.16.0.19 --port 8080
Using Deployment echo-easy
   Intercept name         : echo-easy
   State                  : ACTIVE
   Workload kind          : Deployment
   Destination            : 172.16.0.19:8080
   Service Port Identifier: proxied
   Volume Mount Point     : /var/folders/j8/kzkn41mx2wsd_ny9hrgd66fc0000gp/T/telfs-517018422
   Intercepting           : all TCP connections
```

## Environment variables and intercept specifications

### Environment variables

You can import environment variables from the cluster pod when running an intercept and apply them to the code running on your local machine for the intercepted service.

There are several options available:

*   `blackbird cluster intercept [service] --port [port] --env-file=[FILENAME]`

    This writes the environment variables to a file. The file can be used when starting containers locally. The option `--env-syntax` allows control over the syntax of the file. Valid syntaxes include "docker", "compose", "sh", "csh", "cmd", and "ps" where "sh", "csh", and "ps" can be suffixed with ":export".
*   `blackbird cluster intercept [service] --port [port] --env-json=[FILENAME]`

    This writes the environment variables to a JSON file. The file can be injected into other build processes.
*   `blackbird cluster intercept [service] --port [port] -- [COMMAND]`

    This runs a command locally with the pod's environment variables set on your local machine. After the command quits, the intercept stops (as if `blackbird cluster leave [service]` was run). This can be used in conjunction with a local server command, such as `python [FILENAME]` or `node [FILENAME]` to run a service locally while using the environment variables that were set on the pod using a ConfigMap.

    Another is running a subshell, such as Bash:

    `blackbird cluster intercept [service] --port [port] -- /bin/bash`

    This starts the intercept and then launches the subshell on your local machine with the same variables set as on the pod.
*   `blackbird cluster intercept [service] --docker-run -- [CONTAINER]`

    This ensures that the environment is propagated to the container. It also works for `--docker-build` and `--docker-debug`.

### Telepresence environment variables

You can also import environment variables specific to Telepresence.

*   `TELEPRESENCE_ROOT`

    The directory where all remote volumes mounts are rooted.
*   `TELEPRESENCE_MOUNTS`

    A colon-separated list of remotely mounted directories.
*   `TELEPRESENCE_CONTAINER`

    The name of the intercepted container.
*   `TELEPRESENCE_INTERCEPT_ID`

    The ID of the intercept. This is the same as the "x-intercept-id" HTTP header. This variable is useful when you need custom behavior while intercepting a pod. For example, in pub-sub systems like Kafka, processes without the `TELEPRESENCE_INTERCEPT_ID` can filter out messages containing an `x-intercept-id` header, while those with an ID process only matching headers. This ensures that messages for a specific intercept are always routed to the intercepting process.

## Intercept specifications

Intercept specifications can be used to create a standard configuration for intercepts that can be used to start local applications and handle intercepted traffic.

> **Note:** Previously, intercept specifications were referred to as _saved intercepts_.

### Templating

This intercept specification supports [template expansion](https://pkg.go.dev/text/template) in all properties except names that references other objects within the specification, and it makes all functions from the [Masterminds/sprig package](https://masterminds.github.io/sprig/) available. The following example shows how to provide a header value created from two environment variables.

```yaml
    headers:
      - name: who
        value: {{env "USER"}}@{{env "HOST"}}
```

Blackbird also provides its own set of properties. This is limited to the following.

| Options                | Type   | Description                                     |
| ---------------------- | ------ | ----------------------------------------------- |
| .Telepresence.Username | string | The name of the user running the specification. |

### Root

This intercept specification can create a standard configuration to easily run tasks, start an intercept, and start your local application to handle the intercepted traffic.

| Options                                            | Description                                                                                           |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [name](using-intercepts.md#name)                   | The name of the specification.                                                                        |
| [connection](using-intercepts.md#connection)       | The connection properties to use when Telepresence connects to the cluster.                           |
| [handlers](using-intercepts.md#handlers)           | The local processes to handle traffic.                                                                |
| [prerequisites](using-intercepts.md#prerequisites) | Items to set up prior to starting any intercepts, and items to remove once the intercept is complete. |
| [workloads](using-intercepts.md#workloads)         | Remote workloads that are intercepted, keyed by workload name.                                        |

#### Name

The name is optional. If you don't specify the name, it will use the filename of the specification file.

```yaml
name : echo-server-spec
```

#### Connection

The connection defines how Blackbird establishes connections to a cluster. Connections established during the execution of an intercept specification will be temporary and terminate with the completion of the specification, while pre-existing connections are discovered and retained for future use.

A connection can be declared in singular form as the following:

```yaml
connection:
  namespace: my_a
  mappedNamespaces:
    - my_a
```

It can also be declared when more than one connection is necessary, in plural form, such as the following:

```yaml
connections:
  - name: alpha
    namespace: my_a
    mappedNamespaces:
      - my_a
  - name: bravo
    namespace: my_b
    mappedNamespaces:
      - my_b
```

When multiple connections are used, all intercept handlers must run in Docker and all connections must have a name.

You can pass the most common parameters from `blackbird cluster connect` command (`blackbird cluster connect --help`) using a camel case format.

Commonly used options include the following:

| Options          | Type        | Format                       | Description                                                                                       |
| ---------------- | ----------- | ---------------------------- | ------------------------------------------------------------------------------------------------- |
| namespace        | string      | \[a-z0-9]\[a-z0-9-]{1,62}    | The namespace that this connection is bound to. Defaults to the default appointed by the context. |
| mappedNamespaces | string list | \[a-z0-9]\[a-z0-9-]{1,62}    | The namespaces that Blackbird will be concerned with.                                             |
| managerNamespace | string      | \[a-z0-9]\[a-z0-9-]{1,62}    | The namespace where the traffic manager is to be found.                                           |
| context          | string      | N/A                          | The Kubernetes context to use.                                                                    |
| hostname         | string      | N/A                          | Docker only. Hostname used by the connection container.                                           |
| expose           | string      | \[IP:]\[port:]container-port | Docker only. Make a connection container port available to services outside of Docker.            |
| name             | string      | N/A                          | The name used when referencing the connection.                                                    |

### Handlers

A handler is code running locally. It can receive traffic for an intercepted service or set up prerequisites to run before/after the intercept itself.

When it's intended as an intercept handler (i.e., to handle traffic), it's usually the service you're working on or another dependency (e.g., database, another third-party service) running on your local machine. A handler can be a Docker container or an application running natively.

The following example creates an intercept handler with the name `echo-server` and uses a Docker container. The container will automatically have access to the ports, environment, and mounted directories of the intercepted container.

The ports field is important for the intercept handler while running in Docker. It indicates which ports should be exposed to the host. If you want to access to it locally, this field must be provided.

```yaml
handlers:
  - name: echo-server
    environment:
      - name: PORT
        value: "8080"
    docker:
      image: jmalloc/echo-server:latest
      ports:
        - 8080
```

If you don't want to use Docker containers, you can still configure your handlers to start using a regular script. The following shows how to create a handler called `echo-server` that sets an environment variable of `PORT=8080` and starts the application.

```yaml
handlers:
  - name: echo-server
    environment:
      - name: PORT
        value: "8080"
    script:
      run: bin/echo-server
```

If you don't want to utilize Docker containers or scripts but want to harness all the essential data, including volumes and environment variables, to start a process that can manage intercepted traffic directed toward a specified output without executing anything, the solution lies in setting up an external handler.

The following shows how to establish this type of handler with the name `echo-server`. This configuration not only sets an environment variable defined as `PORT=8080`, but it also generates a file encompassing all pertinent metadata.

```yaml
handlers:
  - name: echo-server
    environment:
      - name: PORT
        value: "8080"
    external:
      outputPath: /mypath/metadata.yaml
      outputFormat: yaml
      isDocker: true
```

The following table defines the parameters that can be used within the handlers section.

| Options                                  | Type     | Format                      | Description                                                                                |
| ---------------------------------------- | -------- | --------------------------- | ------------------------------------------------------------------------------------------ |
| name                                     | string   | \[a-zA-Z]\[a-zA-Z0-9\_-]\*  | The name of your handler that the intercepts use to reference it.                          |
| environment                              | map list | N/A                         | The environment variables in your handler.                                                 |
| environment\[\*].name                    | string   | \[a-zA-Z\_]\[a-zA-Z0-9\_]\* | The name of the environment variable.                                                      |
| environment\[\*].value                   | string   | N/A                         | The value for the environment variable.                                                    |
| [script](using-intercepts.md#script)     | map      | N/A                         | Tells the handler to run as a script, mutually exclusive to docker and external.           |
| [docker](using-intercepts.md#docker)     | map      | N/A                         | Tells the handler to run as a Docker container, mutually exclusive to script and external. |
| [external](using-intercepts.md#external) | map      | N/A                         | Tells the handler to run as an external, mutually exclusive to script and Docker.          |

#### Script

The handler's script element defines the parameters.

| Options | Type   | Format       | Description                                                                                                                                   |
| ------- | ------ | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| run     | string | N/A          | The script to run. It can use multiple lines.                                                                                                 |
| shell   | string | bash\|sh\|sh | The shell that will parse and run the script. It can be "bash", "zsh", or "sh". It defaults to the value of the `SHELL` environment variable. |

#### Docker

The handler's Docker element defines the parameters. The `build` and `image` parameters are mutually exclusive.

| Options                                | Type        | Format | Description                                                                                                                           |
| -------------------------------------- | ----------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| [build](using-intercepts.md#build)     | map         | N/A    | Defines how to build the image from source using [docker build](https://docs.docker.com/engine/reference/commandline/build/) command. |
| [compose](using-intercepts.md#compose) | map         | N/A    | Defines how to integrate with an existing Docker Compose file.                                                                        |
| image                                  | string      | image  | Defines which image to use.                                                                                                           |
| ports                                  | int list    | N/A    | The ports that should be exposed to the host.                                                                                         |
| options                                | string list | N/A    | Options for Docker run [options](https://docs.docker.com/engine/reference/commandline/run/#options).                                  |
| command                                | string      | N/A    | An optional command to run.                                                                                                           |
| args                                   | string list | N/A    | An optional command arguments                                                                                                         |

#### External

The handler's external element defines the parameters.

| Options      | Type    | Format     | Description                                                       |
| ------------ | ------- | ---------- | ----------------------------------------------------------------- |
| isDocker     | boolean | N/A        | Indicates if the runner is in a Docker container (true/false).    |
| outputFormat | string  | json\|yaml | Sets the output format to either JSON or YAML.                    |
| outputPath   | string  | N/A        | Specifies output destination: "stdout", "stderr", or a file path. |

**Build**

The Docker build element defines the parameters.

| Options | Type        | Format | Description                                                                                |
| ------- | ----------- | ------ | ------------------------------------------------------------------------------------------ |
| context | string      | N/A    | Defines either a path to a directory containing a Dockerfile or a URL to a Git repository. |
| args    | string list | N/A    | Additional arguments for the Docker build command.                                         |

For additional information on these parameters, see [docker container run](https://docs.docker.com/engine/reference/commandline/run).

**Compose**

The Docker Compose element defines the way to integrate with the tool of the same name.

| Options                                 | Type     | Format       | Description                                                                                            |
| --------------------------------------- | -------- | ------------ | ------------------------------------------------------------------------------------------------------ |
| context                                 | string   | N/A          | (Optional) Docker context, meaning the path to / or the directory containing your Docker Compose file. |
| [services](using-intercepts.md#service) | map list |              | The services to use with the Telepresence integration.                                                 |
| spec                                    | map      | compose spec | (Optional) Embedded Docker Compose specification.                                                      |

**Service**

The service describes how to integrate with each service from your Docker Compose file, and it can be seen as an override functionality. A service is normally not provided when you want to keep the original behavior, but it can be provided for documentation purposes using the `local` behavior.

A service can be declared either as a property of `compose` in the intercept specification or as an `x-telepresence` extension in the Docker Compose specification. The syntax is the same in both cases, but the `name` property can't be used together with `x-telepresence` because it's implicit.

| Options                                  | Type   | Format                          | Description                                                                 |
| ---------------------------------------- | ------ | ------------------------------- | --------------------------------------------------------------------------- |
| name                                     | string | \[a-zA-Z]\[a-zA-Z0-9\_-]\*      | The name of your service in the compose file                                |
| [behavior](using-intercepts.md#behavior) | string | interceptHandler\|remote\|local | Behavior of the service in context of the intercept.                        |
| [mapping](using-intercepts.md#mapping)   | map    |                                 | Optional mapping to cluster service. Only applicable for `behavior: remote` |

**Behavior**

| Value            | Description                                                                                                     |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| interceptHandler | The service runs locally and will receive traffic from the intercepted pod.                                     |
| remote           | The service will not run as part of Docker Compose. Instead, traffic is redirected to a service in the cluster. |
| local            | The service runs locally without modifications. This is the default.                                            |

**Mapping**

| Options   | Type   | Description                                                                                  |
| --------- | ------ | -------------------------------------------------------------------------------------------- |
| name      | string | The name of the cluster service to link the compose service with.                            |
| namespace | string | (Optional) The cluster namespace for service. It defaults to the namespace of the intercept. |

**Examples**

Considering the following Docker Compose file:

```yaml
services:
  redis:
    image: redis:6.2.6
    ports:
      - "6379"
  postgres:
    image: "postgres:14.1"
    ports:
      - "5432"
  myapp:
    build:
      # Directory containing the Dockerfile and source code
      context: ../../myapp
    ports:
      - "8080"
    volumes:
      - .:/code
    environment:
      DEV_MODE: "true"
```

The following will use the myapp service as the interceptor.

```yaml
services:
  - name: myapp
    behavior: interceptHandler
```

Due to the possibility of multiple workloads using different connections utilizing the same `compose-handler`, the services designated as `interceptHandler` within the `compose-spec` might operate on distinct connections. When this is the case, the connection must be explicitly specified within each service.

```yaml
services:
  - name: postgres
    behavior: interceptHandler
    connection: alpha
```

The following will prevent the service from running locally. DNS will point to the service in the cluster with the same name.

```yaml
services:
  - name: postgres
    behavior: remote
```

Adding mapping allows you to select the cluster service more accurately by indicating to Telepresence that the _postgres_ service should be mapped to the _psql_ service in the _big-data_ namespace.

```yaml
services:
  - name: postgres
    behavior: remote
    mapping:
      name: psql
      namespace: big-data
```

As an alternative, the `services` can be added as `x-telepresence` extensions in the Docker Compose file:

```yaml
services:
  redis:
    image: redis:6.2.6
    ports:
      - "6379"
  postgres:
    x-telepresence:
      behavior: remote
      mapping:
        name: psql
        namespace: big-data
    image: "postgres:14.1"
    ports:
      - "5432"
  myapp:
    x-telepresence:
      behavior: interceptHandler
    build:
      # Directory containing the Dockerfile and source code
      context: ../../myapp
    ports:
      - "8080"
    volumes:
      - .:/code
    environment:
      DEV_MODE: "true"
```

### Prerequisites

When you're creating an intercept specification, there's an option to include prerequisites.

Prerequisites give you the ability to run scripts for setup, build binaries to run as your intercept handler, and more. Prerequisites is an array, so it can handle many options prior to starting your intercept and running your intercept handlers. The elements of the `prerequisites` array correspond to [`handlers`](using-intercepts.md#handlers).

The following example declares that `build-binary` and `rm-binary` are two handlers; the first will be run before any intercepts, and the second will run after cleaning up the intercepts.

If a prerequisite create succeeds, the corresponding delete is guaranteed to run even if the other steps in the spec fail.

```yaml
prerequisites:
  - create: build-binary
    delete: rm-binary
```

The follow example defines the parameters available within the prerequisites section.

| Options | Description                                       |
| ------- | ------------------------------------------------- |
| create  | The name of a handler to run before the intercept |
| delete  | The name of a handler to run after the intercept  |

### Workloads

Workloads define the services in your cluster that will be intercepted.

The following example creates an intercept on a service called `echo-server` on port 8080. It creates a personal intercept with the header of `x-intercept-id: foo` and routes its traffic to a handler called `echo-server`.

```yaml
workloads:
  # You can define one or more workload(s)
  - name: echo-server
    intercepts:
      # You can define one or more intercept(s)
      - headers:
          - name: myHeader
            value: foo
        port: 8080
        handler: echo-server
```

When multiple connections are used, the name of the workload must be prefixed with the name of the connection and a slash. Like this:

```yaml
workloads:
  # The workload "echo-server" from connection "alpha"
  - name: alpha/echo-server:
```

This following table defines the parameters available within a workload.

| Options    | Type                                             | Format                                                | Description                                                                         | Default |
| ---------- | ------------------------------------------------ | ----------------------------------------------------- | ----------------------------------------------------------------------------------- | ------- |
| name       | string                                           | ^(\[a-z0-9]\[a-z0-9-]{0,62}/)?\[a-z]\[a-z0-9-]{0,62}$ | The name of the workload to intercept (optionally prefixed with a connection name). | N/A     |
| intercepts | [intercept](using-intercepts.md#intercepts) list | N/A                                                   | The list of intercepts associated to the workload.                                  | N/A     |

### Intercepts

The following table defines the parameters available for each intercept.

| Options    | Type                                      | Format                 | Description                                                                                     | Default        |
| ---------- | ----------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------- | -------------- |
| enabled    | boolean                                   | N/A                    | If set to false, it disables this intercept.                                                    | true           |
| headers    | [header](using-intercepts.md#header) list | N/A                    | The headers that filter the intercept.                                                          | Auto generated |
| service    | name                                      | \[a-z]\[a-z0-9-]{1,62} | The name of the service to intercept.                                                           | N/A            |
| localPort  | integer\|string                           | 1-65535                | The port for the service being intercepted.                                                     | N/A            |
| port       | integer                                   | 1-65535                | The port the service in the cluster is running on.                                              | N/A            |
| pathPrefix | string                                    | N/A                    | The path prefix filter for the intercept. Defaults to "/".                                      | /              |
| replace    | boolean                                   | N/A                    | Determines if the app container should be stopped.                                              | false          |
| global     | boolean                                   | N/A                    | If true, intercept all TCP/UDP traffic. Mutually exclusive with headers and pathXxx properties. | true           |
| mountPoint | string                                    | N/A                    | The local directory or drive where the remote volumes are mounted.                              | false          |

**Header**

You can define headers to filter the requests that should end up on your local machine when intercepting.

| Options | Type   | Format | Description              | Default |
| ------- | ------ | ------ | ------------------------ | ------- |
| name    | string | N/A    | The name of the header.  | N/A     |
| value   | string | N/A    | The value of the header. | N/A     |

```yaml
intercepts:
  - headers:
      - name: sentBy
        value: {{ .Telepresence.Username }}
      - name: sentFrom
        value: {{ env "HOSTNAME" }}
```

### Usage

#### Running your specification from the CLI

After you've written your intercept specification, you can run it.

To start your intercept, use the following command.

```bash
blackbird cluster intercept run <path/to/file>
```

This validates and run your specification. If you want to validate it, you can use the following command.

```bash
blackbird cluster intercept validate <path/to/file>
```

#### Using and sharing your specification as a CRD

You can use this specification if you want to share specifications across your team or your organization. You can save specifications as CRDs inside your cluster.

> **Note:** The intercept specification CRD requires Kubernetes 1.22 or higher. If you're using an old cluster you'll need to install using Helm directly and use the `--disable-openapi-validation` flag.

1. Install the CRD object in your cluster. This is a one-time installation.

```bash
blackbird cluster helm install --crds
```

2. Deploy the specification in your cluster as a CRD.

```yaml
apiVersion: getambassador.io/v1alpha4
kind: InterceptSpecification
metadata:
  name: my-crd-spec
  namespace: my-crd-namespace
spec:
  {intercept specification}
```

The `echo-server` example looks like this:

```bash
kubectl apply -f - <<EOF
---
apiVersion: getambassador.io/v1alpha4
kind: InterceptSpecification
metadata:
  name: echo-server-spec
  namespace: my-crd-namespace
spec:
  connection:
    context: "my-context"
  workloads:
    - name: echo-easy
      namespace: default
      intercepts:
        - headers:
            - name: test-{{ .Telepresence.Username }}
              value: "{{ .Telepresence.Username }}"
          localPort: 9090
          port: proxied
          handler: echo-easy
          service: echo-easy
          previewURL:
            enable: false
  handlers:
    - name: echo-easy
      environment:
        - name: PORT
          value: "9090"
      docker:
        image: jmalloc/echo-server
EOF
```

Now, every person that's connected to the cluster can start your intercept by using the following command.

```bash
blackbird cluster intercept run echo-server-spec
```

You can also list available specifications.

```bash
kubectl get ispecs
```

#### Integrating with Docker

An intercept specification can be used within the Docker extension if you're using a YAML file and a Docker runtime as handlers.

#### Integrating with your IDE

You can integrate JSON schemas into your IDE to provide autocompletion and hints while writing your intercept specification. There are two schemas available:

* [YAML specification](https://app.getambassador.io/yaml/telepresence/latest/intercept-schema.yaml)
* [CRD specification](https://app.getambassador.io/yaml/telepresence/latest/intercept-crd-schema.yaml)

To add the schema to your IDE, follow the instructions for your IDE. For example:

* [VSCode](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings)
* [GoLand](https://www.jetbrains.com/help/go/json.html#ws_json_using_schemas)
