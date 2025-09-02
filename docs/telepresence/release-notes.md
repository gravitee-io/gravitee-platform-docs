# Release Notes

### Version 2.20.2 (January 23, 2025) <a href="#id-2.20.2" id="id-2.20.2"></a>

#### Upgraded Golang to 1.23.5

Telepresence now uses the latest version of Golang. This update resolves CVE-2024-45341 and CVE-2024-45336.

### Version 2.20.1 (December 06, 2024) <a href="#id-2.20.1" id="id-2.20.1"></a>

#### Fixed an issue where Telepresence wouldn't create a cache directory

When installing Telepresence 2.20 and running `telepresence login` for the first time, Telepresence didn't create a cache directory. This resulted in an error until the user manually created it. Now, Telepresence automatically creates the directory during a new installation.

### Version 2.20.0 (November 15, 2024) <a href="#id-2.20.0" id="id-2.20.0"></a>

#### Added a timestamp for the telepresence\_logs.zip filename

The timestamp has now been added to telepresence\_logs.

#### Enabled intercepts of workloads that don’t have a service

Telepresence can now intercept workloads that don’t have an associated service. The intercept will then target a container port instead of a service port. You can enable the new behavior by adding a `telepresence.getambassador.io/inject-container-ports` annotation, where the value is a comma-separated list of port identifiers consisting of either the name or the port number of a container port (optionally suffixed with `/TCP` or `/UDP`). For more information, see [Intercepting without a service](technical-reference/intercepts/configure-intercept-using-cli.md#intercepting-without-a-service).

#### Publish the OSS version of the telepresence Helm chart

The OSS version of the telepresence helm chart is now available at ghcr.io/telepresenceio/telepresence-oss, and can be installed using the command:\
`helm install traffic-manager oci://ghcr.io/telepresenceio/telepresence-oss --namespace ambassador --version 2.20.0` The chart documentation is published at [ArtifactHUB](https://artifacthub.io/packages/helm/telepresence-oss/telepresence-oss).

#### Added syntax control for the environment file created with the intercept flag --env-file

You can now use `--env-syntax` to allow control over the syntax of the file created using the intercept flag `--env-file`. Valid syntaxes include `docker`, `compose`, `sh`, `csh`, `cmd`, and `ps`. You can use the export suffix with the following syntaxes: `sh`, `csh`, and `ps`. For more information, see [Environment variables](technical-reference/environment-variables.md).

#### Added Argo Rollouts support for workloads

You can now opt-in for support for workloads using Argo Rollouts. The behavior is controlled by the `workloads.argoRollouts.enabled` Helm chart value. We recommend setting the following annotation to avoid creating unwanted versions: `telepresence.getambassador.io/inject-traffic-agent: enabled` to avoid creation of unwanted revisions. For more information, see [Enable Argo Rollouts](technical-reference/intercepts/#enable-argorollouts).

#### Added --create-namespace flag to the telepresence helm install command

You can now use the `--create-namespace` (default is `true`) flag with the `telepresence helm install` command. If it’s explicitly set to `false`, no attempt will be made to create a namespace for the Traffic Manager. If the namespace is missing, the command will fail. For more information, see [Install into custom namespace](install-telepresence/install-uninstall-the-traffic-manager.md#install-into-custom-namespace).

#### Introduced DNS fallback on Windows

A `network.defaultDNSWithFallback` config option is now available on Windows. It causes the DNS resolver to fall back to the resolver that was first in the list prior to Telepresence establishing a connection. The default is `true` because it provides the best experience. For backwards compatibility, set to `false`.\
Note: When set to `false`, there can be issues when Telepresence connects because utilities that use `nslookup` or `node.resolveXXX` to look up addresses will only attempt to find the first server in the list.

#### Brew now supports MacOS (amd64/arm64) / Linux (amd64)

The brew formula can now dynamically support MacOS (amd64/arm64) / Linux (amd64) in a single formula

#### Added the ability to provide an externally provisioned webhook secret

Added `supplied` as a new option for `agentInjector.certificate.method`. This fully disables the generation of the mutating webhook's secret, allowing the chart to use the values of a pre-existing secret named `agentInjector.secret.name`. Previously, the install would fail when it attempted to create or update the externally managed secret. For more information, see [Customizing the Traffic Manager](install-telepresence/install-uninstall-the-traffic-manager.md#customizing-the-traffic-manager).

#### Added support to allow a PTR query for a DNS server to return the cluster domain

The `nslookup` program on Windows uses a DNS pointer record (PTR) query to retrieve its displayed `Server` property. This Telepresence DNS resolver will now return the cluster domain on this type of query.

#### Added schedulerName to PodTemplate

You can now use a Helm chart value called `schedulerName`. With this feature, you can define particular schedulers from Kubernetes to allocate Telepresence resources, including the Traffic Manager and hook Pods. For more information, see [Customizing the Traffic Manager](install-telepresence/install-uninstall-the-traffic-manager.md#customizing-the-traffic-manager).

#### The Ambassador Agent is no longer enabled by default

The Ambassador agent service, which is used for collecting information about services in the cluster and sending them to Ambassador Cloud, is no longer enabled by default.

#### Use nftables instead of iptables-legacy

We introduced `iptables-legacy` because there was an issue using Telepresence with Fly.io, where nftables wasn't supported by the kernel. Fly.io fixed this issue, so Telepresence now uses `nftables`, again. This ensures that `iptables-legacy` will work for modern systems that lack support.

#### Fixed an issue where the --http-path-regexp intercept flag yielded an illegal argument error

When using the `--http-path-regexp` intercept flag, the subsequent flag sent to the Traffic Agent was incorrect and resulted in an error about a `--path-regexp` flag. Now, the flag is passed correctly as `--path-regex` to Traffic Agent instead of `--path-regexp`.

#### Fixed an issue that caused repeated calls from the systray application to the daemon

Previously, the systray application called the daemon repeatedly to update the menu, even though the menu wasn't visible; this was due to a limitation in the systray component. When the menu was open, an event wasn’t sent. Now, instead of calling the daemon repeatedly, it’s called when the systray opens. This saves space in the connector log and makes the systray application more stable and less demanding on resources.

#### Fixed an issue that caused an incorrect priority for a Docker Compose Specification service

The environment declared in a Docker Compose Specification service used as an intercept handler had a lower priority than the environment declared in the container that was intercepted. This caused the Docker Compose environment to be overwritten. Now, the Docker Compose environment has higher priority. The following is the priority order when merging the environment:

1. Environment in the handler of the Intercept Specification
2. Environment in the service declaration in the Docker Compose Specification
3. Environment in the intercepted container

#### Fixed an issue that caused a crash in Traffic Manager when configured with agentInjector.enabled=false

A Traffic Manager that was installed with the Helm value `agentInjector.enabled=false` crashed when a client used the commands `telepresence version` or `telepresence status`. The commands called a method on the Traffic Manager that panicked if a Traffic Agent wasn't present. Now, this method returns the standard `Unavailable` error code, which is expected by the caller.

#### Fixed an issue that didn’t allow a comma-separated list of daemons for the gather-logs command

The name of the `telepresence gather-logs` flag `--daemons` suggested that the argument could contain more than one daemon, but it couldn't. Now, you can use a comma-separated list (for example, `telepresence gather-logs --daemons root,user`).

#### Fixed an issue where the Traffic Agent would route traffic to localhost during periods when an intercept wasn't active

This issue made it impossible for an application to bind to the Pod's IP, and it also meant that service meshes binding to the podIP would get bypassed, both during and after an intercept had been made. Now, the Traffic Agent forwards non-intercepted requests to the Pod's IP, thereby enabling the application to either bind to localhost or to that IP.

#### Fixed an issue where the root daemon wouldn't start when the sudo timeout was set to zero

The root daemon wouldn’t start when sudo was configured with a `timestamp_timeout=0`. The logic first requested root privileges using a sudo call and then relied on the caching of these privileges so that a subsequent call using `--non-interactive` was guaranteed to succeed. Now, the logic includes a single sudo call and solely rely on sudo to print an informative prompt and start the daemon in the background.

#### Fixed an issue where a telepresence connect --docker failed when attempting to connect to a minikube that uses a docker driver

This issue occurred because the containerized daemon didn’t have access to the minikube docker network. Telepresence now detects an attempt to connect to that network and attach it to the daemon container as needed.

#### Fixed an issue that caused a race condition in the Traffic Agent injector when using inject annotation

Applying multiple deployments that used the `telepresence.getambassador.io/inject-traffic-agent: enabled` would cause a race condition. This resulted in a large number of new pods that eventually had to be deleted, or sometimes in pods that didn't contain a Traffic Agent.

#### Fixed an issue that caused the incorrect use of a custom agent security context

The Traffic Manager helm chart now correctly uses a custom agent security context if one is provided.

### Version 2.19.6 <a href="#id-2.19.6" id="id-2.19.6"></a>

#### Panic in traffic-manager when using Istio integration with sidecars w/o a workloadSelector

A traffic-manager that was installed with `--set trafficManager.serviceMesh.type=istio` would panic if it encountered an istio `Sidecar` definition that didn't have a `workloadSelector` declared.

#### Fix bug in workload cache, causing endless recursion when a workload uses the same name as its owner.

The workload cache was keyed by name and namespace, but not by kind, so a workload named the same as its owner workload would be found using the same key. This led to the workload finding itself when looking up its owner, which in turn resulted in an endless recursion when searching for the topmost owner.

#### FailedScheduling events mentioning node availability considered fatal when waiting for agent to arrive.

The traffic-manager considers some events as fatal when waiting for a traffic-agent to arrive after an injection has been initiated. This logic would trigger on events like "Warning FailedScheduling 0/63 nodes are available" although those events indicate a recoverable condition and kill the wait. This is now fixed so that the events are logged but the wait continues.

### Version 2.19.5 (May 15, 2024) <a href="#id-2.19.5" id="id-2.19.5"></a>

#### Prevent bad cloud-daemon behavior when using WSL.

The cloud-daemon was not usable on a Linux box where the dbus was unavailable. The systray panicked (unless disabled) and the notifier exited with an error, resulting in that the cloud-daemon also exited.

#### Docker aliases deprecation caused failure to detect Kind cluster.

The logic for detecting if a cluster is a local Kind cluster, and therefore needs some special attention when using `telepresence connect --docker`, relied on the presence of `Aliases` in the Docker network that a Kind cluster sets up. In Docker versions from 26 and up, this value is no longer used, but the corresponding info can instead be found in the new `DNSNames` field.

### Version 2.19.4 (April 23, 2024) <a href="#id-2.19.4" id="id-2.19.4"></a>

#### Creation of individual pods was blocked by the agent-injector webhook.

An attempt to create a pod was blocked unless it was provided by a workload. Hence, commands like `kubectl run -i busybox --rm --image=curlimages/curl --restart=Never -- curl echo-easy.default` would be blocked from executing.

### Version 2.19.3 (April 11, 2024) <a href="#id-2.19.3" id="id-2.19.3"></a>

#### Fix panic due to root daemon not running.

If a `telepresence connect` was made at a time when the root daemon was not running (an abnormal condition) and a subsequent intercept was then made, a panic would occur when the port-forward to the agent was set up. This is now fixed so that the initial `telepresence connect` is refused unless the root daemon is running.

### Version 2.19.2 (April 05, 2024) <a href="#id-2.19.2" id="id-2.19.2"></a>

#### Fix Cloud-daemon termination when update is available.

The cloud-daemon terminated when it detected that an update was available, which resulted in a telepresence disconnect from the cluster.

### Version 2.19.1 (April 04, 2024) <a href="#id-2.19.1" id="id-2.19.1"></a>

#### Get rid of telemount plugin stickiness

The `datawire/telemount` that is automatically downloaded and installed, would never be updated once the installation was made. Telepresence will now check for the latest release of the plugin and cache the result of that check for 24 hours. If a new version arrives, it will be installed and used.

#### Use route instead of address for CIDRs with masks that don't allow "via"

A CIDR with a mask that leaves less than two bits (/31 or /32 for IPv4) cannot be added as an address to the VIF, because such addresses must have bits allowing a "via" IP. The logic was modified to allow such CIDRs to become static routes, using the VIF base address as their "via", rather than being VIF addresses in their own right.

#### Containerized daemon created cache files owned by root

When using `telepresence connect --docker` to create a containerized daemon, that daemon would sometimes create files in the cache that were owned by root, which then caused problems when connecting without the `--docker` flag.

#### Remove large number of requests when traffic-manager is used in large clusters.

The traffic-manager would make a very large number of API requests during cluster start-up or when many services were changed for other reasons. The logic that did this was refactored and the number of queries were significantly reduced.

#### Don't patch probes on replaced containers.

A container that is being replaced by a `telepresence intercept --replace` invocation will have no liveness-, readiness, nor startup-probes. Telepresence didn't take this into consideration when injecting the traffic-agent, but now it will refrain from patching symbolic port names of those probes.

#### Don't rely on context name when deciding if a kind cluster is used.

The code that auto-patches the kubeconfig when connecting to a kind cluster from within a docker container, relied on the context name starting with "kind-", but although all contexts created by kind have that name, the user is still free to rename it or to create other contexts using the same connection properties. The logic was therefore changed to instead look for a loopback service address.

### Version 2.19.0 (February 12, 2024) <a href="#id-2.19.0" id="id-2.19.0"></a>

#### Add ability to configure the systray application.

The systray application can now be configured via a `systray` entry in the `config.yml` file. The entry has the properties `enabled` (defaults to true), `includeContexts` (list of kubernetes contexts to continuously scan for namespaces, where empty means all contexts configured in the current `KUBECONFIG`), and `excludeContexts` (kubernetes contexts to exclude).

#### Include the image for the traffic-agent in the output of the version and status commands.

The version and status commands will now output the image that the traffic-agent will be using when injected by the agent-injector.

#### Custom DNS using the client DNS resolver.

A new `telepresence connect --proxy-via CIDR=WORKLOAD` flag was introduced, allowing Telepresence to translate DNS responses matching specific subnets into virtual IPs that are used locally. Those virtual IPs are then routed (with reverse translation) via the pod's of a given workload. This makes it possible to handle custom DNS servers that resolve domains into loopback IPs.

#### Make namespace-id command default to the manager's namespace.

The command `telepresence namespace-id` will no longer require a `--namespace` flag. When not given, the command will default to the namespace of where the traffic-manager is installed or will be installed by default.

#### Never ask for login when traffic-manager is licensed.

A licensed traffic-manager does not require that a connecting user is logged in, and telepresence will therefore no longer prompt a user to login when connecting to it. The `skipLogin` configuration is no longer relevant when the traffic-manager is licensed, instead it will just suppress the login-prompt when a login is required, so that an error is printed instead.

#### The telepresence license --id command was broken

The `telepresence license --id <namespace-id>` reported a conflict with the `--host-domain` flag and exited, regardless of the setting of that flag.

#### Make agent registry, name, and tag configurable individually.

Prior to this change, it was not possible to just provide a new tag or a new registry for the agent image in the Helm chart and have that override the default fetched from SystemA. Now all three parts can be provided individually or in combinations. An attempt will be made to fetch the preferred image from Ambassador Cloud unless all three are provided.

#### Make cloud-daemon functional without a user-interface.

Running the cloud-daemon without a user interface resulted in errors being generated in its log. Trying to run the cloud-daemon in a docker container made it fail and exit (no dbus available). This is now fixed by making the cloud-daemon sensitive to the environment in which it executes so that the systray-app and the notifier never starts unless a UI is present.

#### Include non-default zero values in output of telepresence config view.

The `telepresence config view` command will now print zero values in the output when the default for the value is non-zero.

#### Restore ability to run the telepresence CLI in a docker container.

The improvements made to be able to run the telepresence daemon in docker using `telepresence connect --docker` made it impossible to run both the CLI and the daemon in docker. This commit fixes that and also ensures that the user- and root-daemons are merged in this scenario when the container runs as root.

#### Remote mounts when intercepting with the --replace flag.

A `telepresence intercept --replace` did not correctly mount all volumes, because when the intercepted container was removed, its mounts were no longer visible to the agent-injector when it was subjected to a second invocation. The container is now kept in place, but with an image that just sleeps infinitely.

#### Intercepting with the --replace flag will no longer require all subsequent intercepts to use --replace.

A `telepresence intercept --replace` will no longer switch the mode of the intercepted workload, forcing all subsequent intercepts on that workload to use `--replace` until the agent is uninstalled. Instead, `--replace` can be used interchangeably just like any other intercept flag.

#### Kubeconfig exec authentication with context names containing colon didn't work on Windows

The logic added to allow the root daemon to connect directly to the cluster using the user daemon as a proxy for exec type authentication in the kube-config, didn't take into account that a context name sometimes contains the colon ":" character. That character cannot be used in filenames on windows because it is the drive letter separator.

#### Provide agent name and tag as separate values in Helm chart

The `AGENT_IMAGE` was a concatenation of the agent's name and tag. This is now changed so that the env instead contains an `AGENT_IMAGE_NAME` and `AGENT_INAGE_TAG`. The `AGENT_IMAGE` is removed. Also, a new env `REGISTRY` is added, where the registry of the traffic- manager image is provided. The `AGENT_REGISTRY` is no longer required and will default to `REGISTRY` if not set.

#### Environment interpolation expressions were prefixed twice.

Telepresence would sometimes prefix environment interpolation expressions in the traffic-agent twice so that an expression that looked like `$(SOME_NAME)` in the app-container, ended up as `$(_TEL_APP_A__TEL_APP_A_SOME_NAME)` in the corresponding expression in the traffic-agent.

#### Panic in root-daemon on darwin workstations with full access to cluster network.

A darwin machine with full access to the cluster's subnets will never create a TUN-device, and a check was missing if the device actually existed, which caused a panic in the root daemon.

### Version 2.18.1 (December 27, 2023) <a href="#id-2.18.1" id="id-2.18.1"></a>

#### False conflict when intercepting multiple services with the same service port number that targeted the same pod.

Telepresence would report that two intercepts on different service ports were conflicting if those ports used the same service port number and targeted the same pod.

#### Show allow-conflicting-subnets in telepresence status and telepresence config view.

The `telepresence status` and `telepresence config view` commands didn't show the `allowConflictingSubnets` CIDRs because the value wasn't propagated correctly to the CLI.

### Version 2.18.0 (December 15, 2023) <a href="#id-2.18.0" id="id-2.18.0"></a>

#### Multiple connections in the Intercept Specification.

The Intercept Specification can now accommodate multiple connections, making it possible to have simultaneous intercepts that make use of different Kubernetes contexts and/or namespaces.

#### New properties added to the Connection object of the Intercept Spec.

The properties `Expose`, `Hostname`, and `AllowConflictingSubnets` was added to the `Connection` object of the Internet Specification.

#### The directory of the Intercept Specification is now the default docker context.

An Intercept Specification that references a Docker build or a Docker compose Service that declares a build, will now set the default context for such builds to the directory from where the Intercept Specification was loaded.

#### The tray application can manage multiple connections and docker mode.

The tray application can now manage multiple connections and it is possible to choose if new connections should be using a containerized daemon or a daemon running on the host.

#### Permit templates in the JSON-schema for the Intercept Specification.

The JSON-schema for the Intercept Specification will now allow most properties to contain template specifications in the form `{{<template spec>}}`. The exception is properties that are used for referencing other objects within the specification.

#### The published- and target-port were swapped when exposing Docker compose Service ports.

The `socat` container that deals with exposing docker compose ports by bridging the "telepresence" network to the daemon container network had the published- and target-port swapped, making it impossible to user declarations where the two numbers differed.

#### It is now possible use a host-based connection and containerized connections simultaneously.

Only one host-based connection can exist because that connection will alter the DNS to reflect the namespace of the connection. but it's now possible to create additional connections using `--docker` while retaining the host-based connection.

#### Ability to set the hostname of a containerized daemon.

The hostname of a containerized daemon defaults to be the container's ID in Docker. You now can override the hostname using `telepresence connect --docker --hostname <a name>`.

#### New --multi-daemon flag to enforce a consistent structure for the status command output.

The output of the `telepresence status` when using `--output json` or `--output yaml` will either show an object where the `user_daemon` and `root_daemon` are top level elements, or when multiple connections are used, an object where a `connections` list contains objects with those daemons. The flag `--multi-daemon` will enforce the latter structure even when only one daemon is connected so that the output can be parsed consistently. The reason for keeping the former structure is to retain backward compatibility with existing parsers.

#### Make output from telepresence quit more consistent.

A quit (without -s) just disconnects the host user and root daemons but will quit a container based daemon. The message printed was simplified to remove some have/has is/are errors caused by the difference.

#### Fix errors about a bad TLS certificate when refreshing the mutator-webhook secret.

The `agent-injector` service will now refresh the secret used by the `mutator-webhook` each time a new connection is established, thus preventing the certificates to go out-of-sync when the secret is regenerated.

#### Keep telepresence-agents configmap in sync with pod states.

An intercept attempt that resulted in a timeout due to failure of injecting the traffic-agent left the `telepresence-agents` configmap in a state that indicated that an agent had been added, which caused problems for subsequent intercepts after the problem causing the first failure had been fixed.

#### The telepresence status command will now report the status of all running daemons.

A `telepresence status`, issued when multiple containerized daemons were active, would error with "multiple daemons are running, please select one using the --use \<match> flag". This is now fixed so that the command instead reports the status of all running daemons.

#### The telepresence version command will now report the version of all running daemons.

A `telepresence version`, issued when multiple containerized daemons were active, would error with "multiple daemons are running, please select one using the --use \<match> flag". This is now fixed so that the command instead reports the version of all running daemons.

#### Multiple containerized daemons can now be disconnected using telepresence quit -s.

A `telepresence quit -s`, issued when multiple containerized daemons were active, would error with "multiple daemons are running, please select one using the --use \<match> flag". This is now fixed so that the command instead quits all daemons.

### Version 2.17.1 (November 29, 2023) <a href="#id-2.17.1" id="id-2.17.1"></a>

#### Intercepting services with the same name but different namespaces caused a conflict.

The intercept conflict detection mechanism introduced in 2.17.0 incorrectly claimed that global intercepts on services with the same name, but in different namespaces, interfered with each-other.

#### The DNS search path on Windows is now restored when Telepresence quits

The DNS search path that Telepresence uses to simulate the DNS lookup functionality in the connected cluster namespace was not removed by a `telepresence quit`, resulting in connectivity problems from the workstation. Telepresence will now remove the entries that it has added to the search list when it quits.

#### The user-daemon would sometimes get killed when used by multiple simultaneous CLI clients.

The user-daemon would die with a fatal "fatal error: concurrent map writes" error in the `connector.log`, effectively killing the ongoing connection.

#### Multiple services ports using the same target port would not get intercepted correctly.

Intercepts didn't work when multiple service ports were using the same container port. Telepresence would think that one of the ports wasn't intercepted and therefore disable the intercept of the container port.

#### Root daemon refuses to disconnect.

The root daemon would sometimes hang forever when attempting to disconnect due to a deadlock in the VIF-device.

#### Fix panic in user daemon when traffic-manager was unreachable

The user daemon would panic if the traffic-manager was unreachable. It will now instead report a proper error to the client.

#### Removal of problematic backward support for versions predating 2.6.0.

The telepresence helm installer will no longer make attempts to discover and convert workloads that were modified by the telepresence client in versions prior to 2.6.0. Users have reported problems with the job performing this discovery, and it was therefore removed from the helm chart because the support for those versions was dropped some time ago.

### Version 2.17.0 (November 14, 2023) <a href="#id-2.17.0" id="id-2.17.0"></a>

#### Telepresence now has a native Istio integration.

Telepresence can now create Istio objects to manage traffic, preventing conflicts between its configuration and your mesh's networking configuration.

#### Telepresence will detect intercept conflicts.

When creating a personal intercept, if a header conflicts with those from an existing one, Telepresence will return an error indicating which headers are causing the issue. For instance, if you use the command `--http-header a=b --http-header c=d`, it will throw an error if there is another intercept already using the header `--http-header a=b`. Furthermore, it will now also detect a global intercept interference.

#### The "context" field wasn't parsed when executing a specification with Docker Compose.

When executing an intercept specification with the Docker Compose integration, the `context` field was not correctly interpreted. Consequently, it was impossible to specify the path to a Compose file from any location other than the working directory.

#### The cloud daemon should not start when calling Telepresence status.

The cloud daemon was started when calling Telepresence status while this command should not trigger any action.

#### Cloud daemon running state added to the status command.

Calling `telepresence status` will now display if the cloud daemon is running or not, including in JSON & YAML formats.

#### Changed "current-cluster-id" command to "namespace-id".

`namespace-id` should now be used to get IDs for licenses. `--namespace` should be used to identify the namespace of the telepresence installation

#### Option to return an error when a personal intercept expires.

A new option, `--set=intercept.expiredNotifications=true` has been introduced in the traffic manager. This option is disabled by default. When enabled, it ensures that any request utilizing a personal header associated with an expired intercept will result in an error (status code 503). This change aims to eliminate potential confusion that may arise when a user requests an endpoint, believing that the intercept is still active when it has actually expired. This feature is only compatible with traffic agent versions greater than or equal to v1.14.0

#### Fix the documentation link displayed in the help command.

The command was previously directing users to the OSS website instead of the proprietary documentation.

#### Additional Prometheus metrics to track intercept/connect activity

This feature adds the following metrics to the Prometheus endpoint: `connect_count`, `connect_active_status`, `intercept_count`, and `intercept_active_statusintercept_count` metric has been renamed to `active_intercept_count` for clarity.

#### Make the Telepresence client docker image configurable.

The docker image used when running a Telepresence intercept in docker mode can now be configured using the setting `images.clientImage` and will default first to the value of the environment `TELEPRESENCE_CLIENT_IMAGE`, and then to the value preset by the telepresence binary. This configuration setting is primarily intended for testing purposes.

#### Use traffic-agent port-forwards for outbound and intercepted traffic.

The telepresence TUN-device is now capable of establishing direct port-forwards to a traffic-agent in the connected namespace. That port-forward is then used for all outbound traffic to the device, and also for all traffic that arrives from intercepted workloads. Getting rid of the extra hop via the traffic-manager improves performance and reduces the load on the traffic-manager. The feature can only be used if the client has Kubernetes port-forward permissions to the connected namespace. It can be disabled by setting `cluster.agentPortForward` to `false` in `config.yml`.

#### Improve outbound traffic performance.

The root-daemon now communicates directly with the traffic-manager instead of routing all outbound traffic through the user-daemon. The root-daemon uses a patched kubeconfig where `exec` configurations to obtain credentials are dispatched to the user-daemon. This to ensure that all authentication plugins will execute in user-space. The old behavior of routing everything through the user-daemon can be restored by setting `cluster.connectFromRootDaemon` to `false` in `config.yml`.

#### New networking CLI flag --allow-conflicting-subnets

telepresence connect (and other commands that kick off a connect) now accepts an --allow-conflicting-subnets CLI flag. This is equivalent to client.routing.allowConflictingSubnets in the helm chart, but can be specified at connect time. It will be appended to any configuration pushed from the traffic manager.

#### Warn if large version mismatch between traffic manager and client.

Print a warning if the minor version diff between the client and the traffic manager is greater than three.

#### The authenticator binary was removed from the docker image.

The `authenticator` binary, used when serving proxied `exec` kubeconfig credential retrieval, has been removed. The functionality was instead added as a subcommand to the `telepresence` binary.

### Version 2.16.1 (October 12, 2023) <a href="#id-2.16.1" id="id-2.16.1"></a>

#### Use different names for the Telepresence client image in OSS and PRO

Both images used the name "telepresence", causing the OSS image to be replaced by the PRO image. The PRO client image is now renamed to "ambassador-telepresence".

#### Some \<code>--http-xxx\</code> flags didn't get propagated correctly to the traffic-agent.

the whole list of `--http` flags would get replaced with `--http-header=auto` unless an `--http-header` was given. As a result, flags like `--http-plaintext` were discarded.

#### Add \<code>--docker-debug\</code> flag to the \<code>telepresence intercept\</code> command.

This flag is similar to `--docker-build` but will start the container with more relaxed security using the `docker run` flags `--security-opt apparmor=unconfined --cap-add SYS_PTRACE`.

#### Add a \<code>--export\</code> option to the \<code>telepresence connect\</code> command.

In some situations it is necessary to make some ports available to the host from a containerized telepresence daemon. This commit adds a repeatable `--expose <docker port exposure>` flag to the connect command.

#### Prevent agent-injector webhook from selecting from kube-xxx namespaces.

The `kube-system` and `kube-node-lease` namespaces should not be affected by a global agent-injector webhook by default. A default `namespaceSelector` was therefore added to the Helm Chart `agentInjector.webhook` that contains a `NotIn` preventing those namespaces from being selected.

#### Backward compatibility for pod template TLS annotations.

Users of Telepresence < 2.9.0 that make use of the pod template TLS annotations were unable to upgrade because the annotation names have changed (now prefixed by "telepresence."), and the environment expansion of the annotation values was dropped. This fix restores support for the old names (while retaining the new ones) and the environment expansion.

#### Built with go 1.21.3

Built Telepresence with go 1.21.3 to address CVEs.

#### Match service selector against pod template labels

When listing intercepts (typically by calling `telepresence list`) selectors of services are matched against workloads. Previously the match was made against the labels of the workload, but now they are matched against the labels pod template of the workload. Since the service would actually be matched against pods this is more correct. The most common case when this makes a difference is that statefulsets now are listed when they should.

### Version 2.16.0 (October 02, 2023) <a href="#id-2.16.0" id="id-2.16.0"></a>

#### Intercepts can now replace running containers

It's now possible to stop a pod's container from running while the pod is intercepted. Once you leave the intercept, the pod will be restarted with its application container restored.

#### New "external" handler type in the Intercept Specification.

A new "external" handler type, primarily intended for integration purposes, was added to the Intercept Specification. This handler will emit all information needed to start a process that will handle intercepted traffic to a given output, but will not actually run anything.

#### System Tray Icon and Menu

A new telepresence icon and menu will appear in your system tray. The menu options are connect, disconnect, leave an intercept, and quit.

#### A telepresence quit -s will now also quit the cloud-daemon.

The cloud-daemon is designed to have the same life-cycle as the login, and did therefore only exit when the user logged out. This is now changed so that it also exits when running `telepresence quit --stop-daemons`.

#### The helm sub-commands will no longer start the user daemon.

-> The `telepresence helm install/upgrade/uninstall` commands will no longer start the telepresence user daemon because there's no need to connect to the traffic-manager in order for them to execute.

#### Routing table race condition

-> A race condition would sometimes occur when a Telepresence TUN device was deleted and another created in rapid succession that caused the routing table to reference interfaces that no longer existed.

#### Stop lingering daemon container

When using `telepresence connect --docker`, a lingering container could be present, causing errors like "The container name NN is already in use by container XX ...". When this happens, the connect logic will now give the container some time to stop and then call `docker stop NN` to stop it before retrying to start it.

#### Add file locking to the Telepresence cache

Files in the Telepresence cache are accesses by multiple processes. The processes will now use advisory locks on the files to guarantee consistency.

#### Lock connection to namespace

The behavior changed so that a connected Telepresence client is bound to a namespace. The namespace can then not be changed unless the client disconnects and reconnects. A connection is also given a name. The default name is composed from `<kube context name>-<namespace>` but can be given explicitly when connecting using `--name`. The connection can optionally be identified using the option `--use <name match>` (only needed when docker is used and more than one connection is active).

#### Deprecation of global --context and --docker flags.

The global flags `--context` and `--docker` will now be considered deprecated unless used with commands that accept the full set of Kubernetes flags (e.g. `telepresence connect`).

#### Deprecation of the --namespace flag for the intercept command.

The `--namespace` flag is now deprecated for `telepresence intercept` command. The flag can instead be used with all commands that accept the full set of Kubernetes flags (e.g. `telepresence connect`).

#### Legacy code predating version 2.6.0 was removed.

-> The telepresence code-base still contained a lot of code that would modify workloads instead of relying on the mutating webhook installer when a traffic-manager version predating version 2.6.0 was discovered. This code has now been removed.

#### Add \`telepresence list-namespaces\` and \`telepresence list-contexts\` commands

These commands can be used to check accessible namespaces and for automation.

#### Implicit connect warning

A deprecation warning will be printed if a command other than `telepresence connect` causes an implicit connect to happen. Implicit connects will be removed in a future release.

### Version 2.15.1 (September 06, 2023) <a href="#id-2.15.1" id="id-2.15.1"></a>

#### Rebuild with go 1.21.1

Rebuild Telepresence with go 1.21.1 to address CVEs.

#### Set security context for traffic agent

Openshift users reported that the traffic agent injection was failing due to a missing security context.

### Version 2.15.0 (August 28, 2023) <a href="#id-2.15.0" id="id-2.15.0"></a>

#### When logging out you will now automatically be disconnected

With the change of always being required to login for Telepresence commands, you will now be disconnected from any existing sessions when logging out.

#### Add ASLR to binaries not in docker

Addresses PEN test issue.

#### Ensure that the x-telepresence-intercept-id header is read-only.

The system assumes that the `x-telepresence-intercept-id` header contains the ID of the intercept when it is present, and attempts to redefine it will now result in an error instead of causing a malfunction when using preview URLs.

#### Fix parsing of multiple --http-header arguments

An intercept using multiple header flags, e.g. `--http-header a=b --http-header x=y` would assemble them incorrectly into one header as `--http-header a=b,x=y` which were then interpreted as a match for the header `a` with value `b,x=y`.

#### Fixed bug in telepresence status when apikey login fails

A bug was found when the docker-desktop extension would issue a telepresence status command with an expired or invalid apikey. This would cause the extension to get stuck in an authentication loop. This bug was addressed and resolved.

### Version 2.14.4 (August 23, 2023) <a href="#id-2.14.4" id="id-2.14.4"></a>

#### Nil pointer exception when upgrading the traffic-manager.

Upgrading the traffic-manager using `telepresence helm upgrade` would sometimes result in a helm error message executing "telepresence/templates/intercept-env-configmap.yaml" at <.Values.intercept.environment.excluded>: nil pointer evaluating interface {}.excluded"

### Version 2.14.2 (July 26, 2023) <a href="#id-2.14.2" id="id-2.14.2"></a>

#### Incorporation of the last version of Telepresence.

A new version of Telepresence OSS was published.

### Version 2.14.1 (July 07, 2023) <a href="#id-2.14.1" id="id-2.14.1"></a>

#### More flexible templating in the Intercept Specification.

The [Sprig](http://masterminds.github.io/sprig/) template functions can now be used in many unconstrained fields of an Intercept Specification, such as environments, arguments, scripts, commands, and intercept headers.

#### User daemon would panic during connect

An attempt to connect on a host where no login has ever been made, could cause the user daemon to panic.

### Version 2.14.0 (June 12, 2023) <a href="#id-2.14.0" id="id-2.14.0"></a>

#### Telepresence with Docker Compose

Telepresence now is integrated with Docker Compose. You can now use a compose file as an Intercept Handler in your Intercept Specifications to utilize you local dev stack alongside an Intercept.

#### Added the ability to exclude environment variables

You can now configure your traffic-manager to exclude certain environment variables from being propagated to your local environment while doing an intercept.

#### Routing conflict reporting.

Telepresence will now attempt to detect and report routing conflicts with other running VPN software on client machines. There is a new configuration flag that can be tweaked to allow certain CIDRs to be overridden by Telepresence.

#### Migration of Pod Daemon to the proprietary version of Telepresence

Pod Daemon has been successfully integrated with the most recent proprietary version of Telepresence. This development allows users to leverage the datawire/telepresence image for their deployment previews. This enhancement streamlines the process, improving the efficiency and effectiveness of deployment preview scenarios.

### Version 2.13.3 (May 25, 2023) <a href="#id-2.13.3" id="id-2.13.3"></a>

#### Add imagePullSecrets to hooks

Add .Values.hooks.curl.imagePullSecrets and .Values.hooks curl.imagePullSecrets to Helm values.

#### Change reinvocation policy to Never for the mutating webhook

The default setting of the reinvocationPolicy for the mutating webhook dealing with agent injections changed from Never to IfNeeded.

#### Fix mounting fail of IAM roles for service accounts web identity token

The eks.amazonaws.com/serviceaccount volume injected by EKS is now exported and remotely mounted during an intercept.

#### Correct namespace selector for cluster versions with non-numeric characters

The mutating webhook now correctly applies the namespace selector even if the cluster version contains non-numeric characters. For example, it can now handle versions such as Major:"1", Minor:"22+".

#### Enable IPv6 on the telepresence docker network

The "telepresence" Docker network will now propagate DNS AAAA queries to the Telepresence DNS resolver when it runs in a Docker container.

#### Fix the crash when intercepting with --local-only and --docker-run

Running telepresence intercept --local-only --docker-run no longer results in a panic.

#### Fix incorrect error message with local-only mounts

Running telepresence intercept --local-only --mount false no longer results in an incorrect error message saying "a local-only intercept cannot have mounts".

#### specify port in hook urls

The helm chart now correctly handles custom agentInjector.webhook.port that was not being set in hook URLs.

#### Fix wrong default value for disableGlobal and agentArrival

Params .intercept.disableGlobal and .timeouts.agentArrival are now correctly honored.

### Version 2.13.2 (May 12, 2023) <a href="#id-2.13.2" id="id-2.13.2"></a>

#### Authenticator Service Update

Replaced / characters with a - when the authenticator service creates the kubeconfig in the Telepresence cache.

#### Enhanced DNS Search Path Configuration for Windows (Auto, PowerShell, and Registry Options)

Configurable strategy (auto, powershell. or registry) to set the global DNS search path on Windows. Default is auto which means try powershell first, and if it fails, fall back to registry.

#### Configurable Traffic Manager Timeout in values.yaml

The timeout for the traffic manager to wait for traffic agent to arrive can now be configured in the values.yaml file using timeouts.agentArrival. The default timeout is still 30 seconds.

#### Enhanced Local Cluster Discovery for macOS and Windows

The automatic discovery of a local container based cluster (minikube or kind) used when the Telepresence daemon runs in a container, now works on macOS and Windows, and with different profiles, ports, and cluster names

#### FTP Stability Improvements

Multiple simultaneous intercepts can transfer large files in bidirectionally and in parallel.

#### Intercepted Persistent Volume Pods No Longer Cause Timeouts

Pods using persistent volumes no longer causes timeouts when intercepted.

#### Successful 'Telepresence Connect' Regardless of DNS Configuration

Ensure that \`telepresence connect\`\` succeeds even though DNS isn't configured correctly.

#### Traffic-Manager's 'Close of Closed Channel' Panic Issue

The traffic-manager would sometimes panic with a "close of closed channel" message and exit.

#### Traffic-Manager's Type Cast Panic Issue

The traffic-manager would sometimes panic and exit after some time due to a type cast panic.

#### Login Friction

Improve login behavior by clearing the saved intermediary API Keys when a user logins to force Telepresence to generate new ones.

### Version 2.13.1 (April 20, 2023) <a href="#id-2.13.1" id="id-2.13.1"></a>

#### Update ambassador-telepresence-agent to version 1.13.13

The malfunction of the Ambassador Telepresence Agent occurred as a result of an update which compressed the executable file.

### Version 2.13.0 (April 18, 2023) <a href="#id-2.13.0" id="id-2.13.0"></a>

#### Better kind / minikube network integration with docker

The Docker network used by a Kind or Minikube (using the "docker" driver) installation, is automatically detected and connected to a Docker container running the Telepresence daemon.

#### New mapped namespace output

Mapped namespaces are included in the output of the telepresence status command.

#### Setting of the target IP of the intercept

There's a new --address flag to the intercept command allowing users to set the target IP of the intercept.

#### Multi-tenant support

The client will no longer need cluster wide permissions when connected to a namespace scoped Traffic Manager.

#### Cluster domain resolution bugfix

The Traffic Manager now uses a fail-proof way to determine the cluster domain.

#### Windows DNS

DNS on windows is more reliable and performant.

#### Agent injection with huge amount of deployments

The agent is now correctly injected even with a high number of deployment starting at the same time.

#### Self-contained kubeconfig with Docker

The kubeconfig is made self-contained before running Telepresence daemon in a Docker container.

#### Version command error

The version command won't throw an error anymore if there is no kubeconfig file defined.

#### Intercept Spec CRD v1alpha1 depreciated

Please use version v1alpha2 of the intercept spec crd.

### Version 2.12.2 (April 04, 2023) <a href="#id-2.12.2" id="id-2.12.2"></a>

#### Update Golang build version to 1.20.3

Update Golang to 1.20.3 to address CVE-2023-24534, CVE-2023-24536, CVE-2023-24537, and CVE-2023-24538

### Version 2.12.1 (March 22, 2023) <a href="#id-2.12.1" id="id-2.12.1"></a>

#### Additions to gather-logs

Telepresence now includes the kubeauth logs when running the gather-logs command

#### Airgapped Clusters can once again create personal intercepts

Telepresence on airgapped clusters regained the ability to use the skipLogin config option to bypass login and create personal intercepts.

#### Environment Variables are now propagated to kubeauth

Telepresence now propagates environment variables properly to the kubeauth-foreground to be used with cluster authentication

### Version 2.12.0 (March 20, 2023) <a href="#id-2.12.0" id="id-2.12.0"></a>

#### Intercept spec can build images from source

Handlers in the Intercept Specification can now specify a `build` property instead of an `image` so that the image is built when the spec runs.

#### Improve volume mount experience for Windows and Mac users

On macOS and Windows platforms, the installation of sshfs or platform specific FUSE implementations such as macFUSE or WinFSP are no longer needed when running an Intercept Specification that uses docker images.

#### Check for service connectivity independently from pod connectivity

Telepresence now enables you to check for a service and pod's connectivity independently, so that it can proxy one without proxying the other.

#### Fix cluster authentication when running the telepresence daemon in a docker container.

Authentication to EKS and GKE clusters have been fixed (k8s >= v1.26)

#### The Intercept spec image pattern now allows nested and sha256 images.

Telepresence Intercept Specifications now handle passing nested images or the sha256 of an image

#### Fix panic when CNAME of kubernetes.default doesn't contain .svc

Telepresence will not longer panic when a CNAME does not contain the .svc in it

### Version 2.11.1 (February 27, 2023) <a href="#id-2.11.1" id="id-2.11.1"></a>

#### Multiple architectures

The multi-arch build for the `ambassador-telepresence-manager` and `ambassador-telepresence-agent` now works for both amd64 and arm64.

#### Ambassador agent Helm chart duplicates

Some labels in the Helm chart for the Ambassador Agent were duplicated, causing problems for FluxCD.

### Version 2.11.0 (February 22, 2023) <a href="#id-2.11.0" id="id-2.11.0"></a>

#### Intercept specification

It is now possible to leverage the intercept specification to spin up your environment without extra tools.

#### Support for arm64 (Apple Silicon)

The `ambassador-telepresence-manager` and `ambassador-telepresence-agent` are now distributed as multi-architecture images and can run natively on both linux/amd64 and linux/arm64.

#### Connectivity check can break routing in VPN setups

The connectivity check failed to recognize that the connected peer wasn't a traffic-manager. Consequently, it didn't proxy the cluster because it incorrectly assumed that a successful connect meant cluster connectivity,

#### VPN routes not detected by \<code>telepresence test-vpn\</code> on macOS

The `telepresence test-vpn` did not include routes of type `link` when checking for subnet conflicts.

### Version 2.10.5 (February 06, 2023) <a href="#id-2.10.5" id="id-2.10.5"></a>

#### mTLS secrets mount

mTLS Secrets will now be mounted into the traffic agent, instead of expected to be read by it from the API. This is only applicable to users of team mode and the proprietary agent

#### Daemon reconnection fix

Fixed a bug that prevented the local daemons from automatically reconnecting to the traffic manager when the network connection was lost.

### Version 2.10.4 (January 20, 2023) <a href="#id-2.10.4" id="id-2.10.4"></a>

#### Backward compatibility restored

Telepresence can now create intercepts with traffic-managers of version 2.9.5 and older.

#### Saved intercepts now works with preview URLs.

Preview URLs are now included/excluded correctly when using saved intercepts.

### Version 2.10.3 (January 17, 2023) <a href="#id-2.10.3" id="id-2.10.3"></a>

#### Saved intercepts

Fixed an issue which was causing the saved intercepts to not be completely interpreted by telepresence.

#### Traffic manager restart during upgrade to team mode

Fixed an issue which was causing the traffic manager to be redeployed after an upgrade to the team mode.

### Version 2.10.2 (January 16, 2023) <a href="#id-2.10.2" id="id-2.10.2"></a>

#### version consistency in helm commands

Ensure that CLI and user-daemon binaries are the same version when running telepresence helm install`or telepresence helm upgrade.`

#### Release Process

Fixed an issue that prevented the `--use-saved-intercept` flag from working.

### Version 2.10.1 (January 11, 2023) <a href="#id-2.10.1" id="id-2.10.1"></a>

#### Release Process

Fixed a regex in our release process that prevented 2.10.0 promotion.

### Version 2.10.0 (January 11, 2023) <a href="#id-2.10.0" id="id-2.10.0"></a>

#### Team Mode and Single User Mode

The Traffic Manager can now be set to either "team" mode or "single user" mode. When in team mode, intercepts will default to http intercepts.

#### Added \`insert\` and \`upgrade\` Subcommands to \`telepresence helm\`

The \`telepresence helm\` sub-commands \`insert\` and \`upgrade\` now accepts all types of helm \`--set-XXX\` flags.

#### Added Image Pull Secrets to Helm Chart

Image pull secrets for the traffic-agent can now be added using the Helm chart setting \`agent.image.pullSecrets\`.

#### Rename Configmap

The configmap \`traffic-manager-clients\` has been renamed to \`traffic-manager\`.

#### Webhook Namespace Field

If the cluster is Kubernetes 1.21 or later, the mutating webhook will find the correct namespace using the label \`kubernetes.io/metadata.name\` rather than \`app.kuberenetes.io/name\`.

#### Rename Webhook

The name of the mutating webhook now contains the namespace of the traffic-manager so that the webhook is easier to identify when there are multiple namespace scoped telepresence installations in the cluster.

#### OSS Binaries

The OSS Helm chart is no longer pushed to the datawire Helm repository. It will instead be pushed from the telepresence proprietary repository. The OSS Helm chart is still what's embedded in the OSS telepresence client.

#### Fix Panic Using \`--docker-run\`

Telepresence no longer panics when \`--docker-run\` is combined with \`--name \` instead of \`--name=\`.

#### Stop assuming cluster domain

Telepresence traffic-manager extracts the cluster domain (e.g. "cluster.local") using a CNAME lookup for "kubernetes.default" instead of "kubernetes.default.svc".

#### Uninstall hook timeout

A timeout was added to the pre-delete hook \`uninstall-agents\`, so that a helm uninstall doesn't hang when there is no running traffic-manager.

#### Uninstall hook check

The \`Helm.Revision\` is now used to prevent that Helm hook calls are served by the wrong revision of the traffic-manager.

### Version 2.9.5 (December 08, 2022) <a href="#id-2.9.5" id="id-2.9.5"></a>

#### Update to golang v1.19.4

Apply security updates by updating to golang v1.19.4

#### GCE authentication

Fixed a regression, that was introduced in 2.9.3, preventing use of gce authentication without also having a config element present in the gce configuration in the kubeconfig.

### Version 2.9.4 (December 02, 2022) <a href="#id-2.9.4" id="id-2.9.4"></a>

#### Subnet detection strategy

The traffic-manager can automatically detect that the node subnets are different from the pod subnets, and switch detection strategy to instead use subnets that cover the pod IPs.

#### Fix \`--set\` flag for \`telepresence helm install\`

The \`telepresence helm\` command \`--set x=y\` flag didn't correctly set values of other types than \`string\`. The code now uses standard Helm semantics for this flag.

#### Fix \`agent.image\` setting propagation

Telepresence now uses the correct \`agent.image\` properties in the Helm chart when copying agent image settings from the \`config.yml\` file.

#### Delay file sharing until needed

Initialization of FTP type file sharing is delayed, so that setting it using the Helm chart value \`intercept.useFtp=true\` works as expected.

#### Cleanup on \`telepresence quit\`

The port-forward that is created when Telepresence connects to a cluster is now properly closed when \`telepresence quit\` is called.

#### Watch \`config.yml\` without panic

The user daemon no longer panics when the \`config.yml\` is modified at a time when the user daemon is running but no session is active.

#### Thread safety

Fix race condition that would occur when \`telepresence connect\` \`telepresence leave\` was called several times in rapid succession.

### Version 2.9.3 (November 23, 2022) <a href="#id-2.9.3" id="id-2.9.3"></a>

#### Helm options for \`livenessProbe\` and \`readinessProbe\`

The helm chart now supports \`livenessProbe\` and \`readinessProbe\` for the traffic-manager deployment, so that the pod automatically restarts if it doesn't respond.

#### Improved network communication

The root daemon now communicates directly with the traffic-manager instead of routing all outbound traffic through the user daemon.

#### Root daemon debug logging

Using \`telepresence loglevel LEVEL\` now also sets the log level in the root daemon.

#### Multivalue flag value propagation

Multi valued kubernetes flags such as \`--as-group\` are now propagated correctly.

#### Root daemon stability

The root daemon would sometimes hang indefinitely when quit and connect were called in rapid succession.

#### Base DNS resolver

Don't use \`systemd.resolved\` base DNS resolver unless cluster is proxied.

### Version 2.9.2 (November 16, 2022) <a href="#id-2.9.2" id="id-2.9.2"></a>

#### Fix panic

Fix panic when connecting to an older traffic-manager.

#### Fix header flag

Fix an issue where the \`http-header\` flag sometimes wouldn't propagate correctly.

### Version 2.9.1 (November 16, 2022) <a href="#id-2.9.1" id="id-2.9.1"></a>

#### Connect failures due to missing auth provider.

The regression in 2.9.0 that caused a \`no Auth Provider found for name “gcp”\` error when connecting was fixed.

### Version 2.9.0 (November 15, 2022) <a href="#id-2.9.0" id="id-2.9.0"></a>

#### New command to view client configuration.

A new `telepresence config view` was added to make it easy to view the current client configuration.

#### Configure Clients using the Helm chart.

The traffic-manager can now configure all clients that connect through the `client:` map in the `values.yaml` file.

#### The Traffic manager version is more visible.

The command `telepresence version` will now include the version of the traffic manager when the client is connected to a cluster.

#### Command output in YAML format.

The global `--output` flag now accepts both `yaml` and `json`.

#### Deprecated status command flag

The `telepresence status --json` flag is deprecated. Use `telepresence status --output=json` instead.

#### Unqualified service name resolution in docker.

Unqualified service names now resolves OK from the docker container when using `telepresence intercept --docker-run`.

#### Output no longer mixes plaintext and json.

Informational messages that don't really originate from the command, such as "Launching Telepresence Root Daemon", or "An update of telepresence ...", are discarded instead of being printed as plain text before the actual formatted output when using the `--output=json`.

#### No more panic when invalid port names are detected.

A \`telepresence intercept\` of services with invalid port no longer causes a panic.

#### Proper errors for bad output formats.

An attempt to use an invalid value for the global `--output` flag now renders a proper error message.

#### Remove lingering DNS config on macOS.

Files lingering under `/etc/resolver` as a result of ungraceful shutdown of the root daemon on macOS, are now removed when a new root daemon starts.

### Version 2.8.5 (November 2, 2022) <a href="#id-2.8.5" id="id-2.8.5"></a>

#### CVE-2022-41716

Updated Golang to 1.19.3 to address CVE-2022-41716.

### Version 2.8.4 (November 2, 2022) <a href="#id-2.8.4" id="id-2.8.4"></a>

#### Release Process

This release resulted in changes to our release process.

### Version 2.8.3 (October 27, 2022) <a href="#id-2.8.3" id="id-2.8.3"></a>

#### Ability to disable global intercepts.

Global intercepts (a.k.a. TCP intercepts) can now be disabled by using the new Helm chart setting `intercept.disableGlobal`.

#### Configurable mutating webhook port

The port used for the mutating webhook can be configured using the Helm chart setting `agentInjector.webhook.port`.

#### Mutating webhook port defaults to 443

The default port for the mutating webhook is now `443`. It used to be `8443`.

#### Agent image configuration mandatory in air-gapped environments.

The traffic-manager will no longer default to use the `tel2` image for the traffic-agent when it is unable to connect to Ambassador Cloud. Air-gapped environments must declare what image to use in the Helm chart.

#### Can now connect to non-helm installs

`telepresence connect` now works as long as the traffic manager is installed, even if it wasn't installed via >code>helm install

#### check-vpn crash fixed

telepresence check-vpn no longer crashes when the daemons don't start properly.

### Version 2.8.2 (October 15, 2022) <a href="#id-2.8.2" id="id-2.8.2"></a>

#### Reinstate 2.8.0

There was an issue downloading the free enhanced client. This problem was fixed, 2.8.0 was reinstated

### Version 2.8.1 (October 14, 2022) <a href="#id-2.8.1" id="id-2.8.1"></a>

#### Rollback 2.8.0

Rollback 2.8.0 while we investigate an issue with ambassador cloud.

### Version 2.8.0 (October 14, 2022) <a href="#id-2.8.0" id="id-2.8.0"></a>

#### Improved DNS resolver

The Telepresence DNS resolver is now capable of resolving queries of type `A`, `AAAA`, `CNAME`, `MX`, `NS`, `PTR`, `SRV`, and `TXT`.

#### New \`client\` structure in Helm chart

A new `client` struct was added to the Helm chart. It contains a `connectionTTL` that controls how long the traffic manager will retain a client connection without seeing any sign of life from the client.

#### Include and exclude suffixes configurable using the Helm chart.

A dns element was added to the `client` struct in Helm chart. It contains an `includeSuffixes` and an `excludeSuffixes` value that controls what type of names that the DNS resolver in the client will delegate to the cluster.

#### Configurable traffic-manager API port

The API port used by the traffic-manager is now configurable using the Helm chart value `apiPort`. The default port is 8081.

#### Envoy server and admin port configuration.

An new `agent` struct was added to the Helm chart. It contains an \`envoy\` structure where the server and admin port of the Envoy proxy running in the enhanced traffic-agent can be configured.

#### Helm chart \`dnsConfig\` moved to \`client.routing\`.

The Helm chart `dnsConfig` was deprecated but retained for backward compatibility. The fields `alsoProxySubnets` and `neverProxySubnets` can now be found under `routing` in the `client` struct.

#### Helm chart \`agentInjector.agentImage\` moved to \`agent.image\`.

The Helm chart `agentInjector.agentImage` was moved to `agent.image`. The old value is deprecated but retained for backward compatibility.

#### Helm chart \`agentInjector.appProtocolStrategy\` moved to \`agent.appProtocolStrategy\`.

The Helm chart `agentInjector.appProtocolStrategy` was moved to `agent.appProtocolStrategy`. The old value is deprecated but retained for backward compatibility.

#### Helm chart \`dnsServiceName\`, \`dnsServiceNamespace\`, and \`dnsServiceIP\` removed.

The Helm chart `dnsServiceName`, `dnsServiceNamespace`, and `dnsServiceIP` has been removed, because they are no longer needed. The TUN-device will use the traffic-manager pod-IP on platforms where it needs to dedicate an IP for its local resolver.

#### Quit daemons with \`telepresence quit -s\`

The former options \`-u\` and \`-r\` for \`telepresence quit\` has been deprecated and replaced with one option \`-s\` which will quit both the root daemon and the user daemon.

#### Environment variable interpolation in pods now works.

Environment variable interpolation now works for all definitions that are copied from pod containers into the injected traffic-agent container.

#### Early detection of namespace conflict

An attempt to create simultaneous intercepts that span multiple namespace on the same workstation is detected early and prohibited instead of resulting in failing DNS lookups later on.

#### Annoying log message removed

Spurious and incorrect ""!! SRV xxx"" messages will no longer appear in the logs when the reason is normal context cancellation.

#### Single name DNS resolution in Docker on Linux host

Single label names now resolves correctly when using Telepresence in Docker on a Linux host

#### Misnomer \`appPortStrategy\` in Helm chart renamed to \`appProtocolStrategy\`.

The Helm chart value `appProtocolStrategy` is now correctly named (used to be `appPortStategy`)

### Version 2.7.6 (September 16, 2022) <a href="#id-2.7.6" id="id-2.7.6"></a>

#### Helm chart resource entries for injected agents

The `resources` for the traffic-agent container and the optional init container can be specified in the Helm chart using the `resources` and `initResource` fields of the `agentInjector.agentImage`

#### Cluster event propagation when injection fails

When the traffic-manager fails to inject a traffic-agent, the cause for the failure is detected by reading the cluster events, and propagated to the user.

#### FTP-client instead of sshfs for remote mounts

Telepresence can now use an embedded FTP client and load an existing FUSE library instead of running an external `sshfs` or `sshfs-win` binary. This feature is experimental in 2.7.x and enabled by setting `intercept.useFtp` to `true`> in the `config.yml`.

#### Upgrade of winfsp

Telepresence on Windows upgraded `winfsp` from version 1.10 to 1.11

#### Removal of invalid warning messages

Running CLI commands on Apple M1 machines will no longer throw warnings about `/proc/cpuinfo` and `/proc/self/auxv`.

### Version 2.7.5 (September 14, 2022) <a href="#id-2.7.5" id="id-2.7.5"></a>

#### Rollback of release 2.7.4

This release is a rollback of the changes in 2.7.4, so essentially the same as 2.7.3

### Version 2.7.4 (September 14, 2022) <a href="#id-2.7.4" id="id-2.7.4"></a>

####

This release was broken on some platforms. Use 2.7.6 instead.

### Version 2.7.3 (September 07, 2022) <a href="#id-2.7.3" id="id-2.7.3"></a>

#### PTY for CLI commands

CLI commands that are executed by the user daemon now use a pseudo TTY. This enables `docker run -it` to allocate a TTY and will also give other commands like `bash read` the same behavior as when executed directly in a terminal.

#### Traffic Manager useless warning silenced

The traffic-manager will no longer log numerous warnings saying `Issuing a systema request without ApiKey or InstallID may result in an error`.

#### Traffic Manager useless error silenced

The traffic-manager will no longer log an error saying `Unable to derive subnets from nodes` when the `podCIDRStrategy` is `auto` and it chooses to instead derive the subnets from the pod IPs.

### Version 2.7.2 (August 25, 2022) <a href="#id-2.7.2" id="id-2.7.2"></a>

#### Autocompletion scripts

Autocompletion scripts can now be generated with `telepresence completion SHELL` where `SHELL` can be `bash, zsh, fish` or `powershell`.

#### Connectivity check timeout

The timeout for the initial connectivity check that Telepresence performs in order to determine if the cluster's subnets are proxied or not can now be configured in the `config.yml` file using `timeouts.connectivityCheck`. The default timeout was changed from 5 seconds to 500 milliseconds to speed up the actual connect.

#### gather-traces feedback

The command `telepresence gather-traces` now prints out a message on success.

#### upload-traces feedback

The command `telepresence upload-traces` now prints out a message on success.

#### gather-traces tracing

The command `telepresence gather-traces` now traces itself and reports errors with trace gathering.

#### CLI log level

The `cli.log` log is now logged at the same level as the `connector.log`

#### Telepresence --help fixed

`telepresence --help` now works once more even if there's no user daemon running.

#### Stream cancellation when no process intercepts

Streams created between the traffic-agent and the workstation are now properly closed when no interceptor process has been started on the workstation. This fixes a potential problem where a large number of attempts to connect to a non-existing interceptor would cause stream congestion and an unresponsive intercept.

#### List command excludes the traffic-manager

The `telepresence list` command no longer includes the `traffic-manager` deployment.

### Version 2.7.1 (August 10, 2022) <a href="#id-2.7.1" id="id-2.7.1"></a>

#### Reinstate telepresence uninstall

Reinstate `telepresence uninstall` with `--everything` depreciated

#### Reduce telepresence helm uninstall

`telepresence helm uninstall` will only uninstall the traffic-manager helm chart and no longer accepts the `--everything`, `--agent`, or `--all-agents` flags.

#### Auto-connect for telepresence intercpet

`telepresence intercept` will attempt to connect to the traffic manager before creating an intercept.

### Version 2.7.0 (August 07, 2022) <a href="#id-2.7.0" id="id-2.7.0"></a>

#### Saved Intercepts

Create telepresence intercepts based on existing Saved Intercepts configurations with `telepresence intercept --use-saved-intercept $SAVED_INTERCEPT_NAME`

#### Distributed Tracing

The Telepresence components now collect OpenTelemetry traces. Up to 10MB of trace data are available at any given time for collection from components. `telepresence gather-traces` is a new command that will collect all that data and place it into a gzip file, and `telepresence upload-traces` is a new command that will push the gzipped data into an OTLP collector.

#### Helm install

A new `telepresence helm` command was added to provide an easy way to install, upgrade, or uninstall the telepresence traffic-manager.

#### Ignore Volume Mounts

The agent injector now supports a new annotation, `telepresence.getambassador.io/inject-ignore-volume-mounts`, that can be used to make the injector ignore specified volume mounts denoted by a comma-separated string.

#### telepresence pod-daemon

The Docker image now contains a new program in addition to the existing traffic-manager and traffic-agent: the pod-daemon. The pod-daemon is a trimmed-down version of the user-daemon that is designed to run as a sidecar in a Pod, enabling CI systems to create preview deploys.

#### Prometheus support for traffic manager

Added prometheus support to the traffic manager.

#### No install on telepresence connect

The traffic manager is no longer automatically installed into the cluster. Connecting or creating an intercept in a cluster without a traffic manager will return an error.

#### Helm Uninstall

The command `telepresence uninstall` has been moved to `telepresence helm uninstall`.

#### readOnlyRootFileSystem mounts work

Add an emptyDir volume and volume mount under `/tmp` on the agent sidecar so it works with \`readOnlyRootFileSystem: true\`

### Version 2.6.8 (June 23, 2022) <a href="#id-2.6.8" id="id-2.6.8"></a>

#### Specify Your DNS

The name and namespace for the DNS Service that the traffic-manager uses in DNS auto-detection can now be specified.

#### Specify a Fallback DNS

Should the DNS auto-detection logic in the traffic-manager fail, users can now specify a fallback IP to use.

#### Intercept UDP Ports

It is now possible to intercept UDP ports with Telepresence and also use `--to-pod` to forward UDP traffic from ports on localhost.

#### Additional Helm Values

The Helm chart will now add the `nodeSelector`, `affinity` and `tolerations` values to the traffic-manager's post-upgrade-hook and pre-delete-hook jobs.

#### Agent Injection Bugfix

Telepresence no longer fails to inject the traffic agent into the pod generated for workloads that have no volumes and \`automountServiceAccountToken: false\`.

### Version 2.6.7 (June 22, 2022) <a href="#id-2.6.7" id="id-2.6.7"></a>

#### Persistent Sessions

The Telepresence client will remember and reuse the traffic-manager session after a network failure or other reason that caused an unclean disconnect.

#### DNS Requests

Telepresence will no longer forward DNS requests for "wpad" to the cluster.

#### Graceful Shutdown

The traffic-agent will properly shut down if one of its goroutines errors.

### Version 2.6.6 (June 9, 2022) <a href="#id-2.6.6" id="id-2.6.6"></a>

#### Env Var \`TELEPRESENCE\_API\_PORT\`

The propagation of the `TELEPRESENCE_API_PORT` environment variable now works correctly.

#### Double Printing \`--output json\`

The `--output json` global flag no longer outputs multiple objects

### Version 2.6.5 (June 03, 2022) <a href="#id-2.6.5" id="id-2.6.5"></a>

#### Helm Option -- \`reinvocationPolicy\`

The `reinvocationPolicy` or the traffic-agent injector webhook can now be configured using the Helm chart.

#### Helm Option -- Proxy Certificate

The traffic manager now accepts a root CA for a proxy, allowing it to connect to ambassador cloud from behind an HTTPS proxy. This can be configured through the helm chart.

#### Helm Option -- Agent Injection

A policy that controls when the mutating webhook injects the traffic-agent was added, and can be configured in the Helm chart.

#### Windows Tunnel Version Upgrade

Telepresence on Windows upgraded wintun.dll from version 0.12 to version 0.14.1

#### Helm Version Upgrade

Telepresence upgraded its embedded Helm from version 3.8.1 to 3.9

#### Kubernetes API Version Upgrade

Telepresence upgraded its embedded Kubernetes API from version 0.23.4 to 0.24.1

#### Flag \`--watch\` Added to \`list\` Command

Added a `--watch` flag to `telepresence list` that can be used to watch interceptable workloads in a namespace.

#### Depreciated \`images.webhookAgentImage\`

The Telepresence configuration setting for \`images.webhookAgentImage\` is now deprecated. Use \`images.agentImage\` instead.

#### Default \`reinvocationPolicy\` Set to Never

The `reinvocationPolicy` or the traffic-agent injector webhook now defaults to `Never` insteadof `IfNeeded` so that `LimitRange`s on namespaces can inject a missing `resources` element into the injected traffic-agent container.

#### UDP

UDP based communication with services in the cluster now works as expected.

#### Telepresence \`--help\`

The command help will only show Kubernetes flags on the commands that supports them

#### Error Count

Only the errors from the last session will be considered when counting the number of errors in the log after a command failure.

### Version 2.6.4 (May 23, 2022) <a href="#id-2.6.4" id="id-2.6.4"></a>

#### Upgrade RBAC Permissions

The traffic-manager RBAC grants permissions to update services, deployments, replicatsets, and statefulsets. Those permissions are needed when the traffic-manager upgrades from versions < 2.6.0 and can be revoked after the upgrade.

### Version 2.6.3 (May 20, 2022) <a href="#id-2.6.3" id="id-2.6.3"></a>

#### Relative Mount Paths

The `--mount` intercept flag now handles relative mount points correctly on non-windows platforms. Windows still require the argument to be a drive letter followed by a colon.

#### Traffic Agent Config

The traffic-agent's configuration update automatically when services are added, updated or deleted.

#### Container Injection for Numeric Ports

Telepresence will now always inject an initContainer when the service's targetPort is numeric

#### Matching Services

Workloads that have several matching services pointing to the same target port are now handled correctly.

#### Unexpected Panic

A potential race condition causing a panic when closing a DNS connection is now handled correctly.

#### Mount Volume Cleanup

A container start would sometimes fail because and old directory remained in a mounted temp volume.

### Version 2.6.2 (May 17, 2022) <a href="#id-2.6.2" id="id-2.6.2"></a>

#### Argo Injection

Workloads controlled by workloads like Argo `Rollout` are injected correctly.

#### Agent Port Mapping

Multiple services appointing the same container port no longer result in duplicated ports in an injected pod.

#### GRPC Max Message Size

The `telepresence list` command no longer errors out with "grpc: received message larger than max" when listing namespaces with a large number of workloads.

### Version 2.6.1 (May 16, 2022) <a href="#id-2.6.1" id="id-2.6.1"></a>

#### KUBECONFIG environment variable

Telepresence will now handle multiple path entries in the KUBECONFIG environment correctly.

#### Don't Panic

Telepresence will no longer panic when using preview URLs with traffic-managers < 2.6.0

### Version 2.6.0 (May 13, 2022) <a href="#id-2.6.0" id="id-2.6.0"></a>

#### Intercept multiple containers in a pod, and multiple ports per container

Telepresence can now intercept multiple services and/or service-ports that connect to the same pod.

#### The Traffic Agent sidecar is always injected by the Traffic Manager's mutating webhook

The client will no longer modify `deployments`, `replicasets`, or `statefulsets` in order to inject a Traffic Agent into an intercepted pod. Instead, all injection is now performed by a mutating webhook. As a result, the client now needs less permissions in the cluster.

#### Automatic upgrade of Traffic Agents

When upgrading, all workloads with injected agents will have their agent "uninstalled" automatically. The mutating webhook will then ensure that their pods will receive an updated Traffic Agent.

#### No default image in the Helm chart

The helm chart no longer has a default set for the `agentInjector.image.name, and unless it's set, the traffic-manager will ask Ambassador Could for the preferred image.`

#### Upgrade to Helm version 3.8.1

The Telepresence client now uses Helm version 3.8.1 when auto-installing the Traffic Manager.

#### Remote mounts will now function correctly with custom securityContext

The bug causing permission problems when the Traffic Agent is in a Pod with a custom `securityContext` has been fixed.

#### Improved presentation of flags in CLI help

The help for commands that accept Kubernetes flags will now display those flags in a separate group.

#### Better termination of process parented by intercept

Occasionally an intercept will spawn a command using `--` on the command line, often in another console. When you use `telepresence leave` or `telepresence quit` while the intercept with the spawned command is still active, Telepresence will now terminate that the command because it's considered to be parented by the intercept that is being removed.

### Version 2.5.8 (April 27, 2022) <a href="#id-2.5.8" id="id-2.5.8"></a>

#### Folder creation on \`telepresence login\`

Fixed a bug where the telepresence config folder would not be created if the user ran `telepresence login` before other commands.

### Version 2.5.7 (April 25, 2022) <a href="#id-2.5.7" id="id-2.5.7"></a>

#### RBAC requirements

A namespaced traffic-manager will no longer require cluster wide RBAC. Only Roles and RoleBindings are now used.

#### Windows DNS

The DNS recursion detector didn't work correctly on Windows, resulting in sporadic failures to resolve names that were resolved correctly at other times.

#### Session TTL and Reconnect

A telepresence session will now last for 24 hours after the user's last connectivity. If a session expires, the connector will automatically try to reconnect.

### Version 2.5.6 (April 18, 2022) <a href="#id-2.5.6" id="id-2.5.6"></a>

#### Less Watchers

Telepresence agents watcher will now only watch namespaces that the user has accessed since the last `connect`.

#### More Efficient \`gather-logs\`

The `gather-logs` command will no longer send any logs through `gRPC`.

### Version 2.5.5 (April 08, 2022) <a href="#id-2.5.5" id="id-2.5.5"></a>

#### Traffic Manager Permissions

The traffic-manager now requires permissions to read pods across namespaces even if installed with limited permissions

#### Linux DNS Cache

The DNS resolver used on Linux with systemd-resolved now flushes the cache when the search path changes.

#### Automatic Connect Sync

The `telepresence list` command will produce a correct listing even when not preceded by a `telepresence connect`.

#### Disconnect Reconnect Stability

The root daemon will no longer get into a bad state when a disconnect is rapidly followed by a new connect.

#### Limit Watched Namespaces

The client will now only watch agents from accessible namespaces, and is also constrained to namespaces explicitly mapped using the `connect` command's `--mapped-namespaces` flag.

#### Limit Namespaces used in \`gather-logs\`

The `gather-logs` command will only gather traffic-agent logs from accessible namespaces, and is also constrained to namespaces explicitly mapped using the `connect` command's `--mapped-namespaces` flag.

### Version 2.5.4 (March 29, 2022) <a href="#id-2.5.4" id="id-2.5.4"></a>

#### Linux DNS Concurrency

The DNS fallback resolver on Linux now correctly handles concurrent requests without timing them out

#### Non-Functional Flag

The ingress-l5 flag will no longer be forcefully set to equal the --ingress-host flag

#### Automatically Remove Failed Intercepts

Intercepts that fail to create are now consistently removed to prevent non-working dangling intercepts from sticking around.

#### Agent UID

Agent container is no longer sensitive to a random UID or an UID imposed by a SecurityContext.

#### Gather-Logs Output Filepath

Removed a bad concatenation that corrupted the output path of `telepresence gather-logs`.

#### Remove Unnecessary Error Advice

An advice to "see logs for details" is no longer printed when the argument count is incorrect in a CLI command.

#### Garbage Collection

Client and agent sessions no longer leaves dangling waiters in the traffic-manager when they depart.

#### Limit Gathered Logs

The client's gather logs command and agent watcher will now respect the configured grpc.maxReceiveSize

#### In-Cluster Checks

The TUN device will no longer route pod or service subnets if it is running in a machine that's already connected to the cluster

#### Expanded Status Command

The status command includes the install id, user id, account id, and user email in its result, and can print output as JSON

#### List Command Shows All Intercepts

The list command, when used with the `--intercepts` flag, will list the users intercepts from all namespaces

### Version 2.5.3 (February 25, 2022) <a href="#id-2.5.3" id="id-2.5.3"></a>

#### TCP Connectivity

Fixed bug in the TCP stack causing timeouts after repeated connects to the same address

#### Linux Binaries

Client-side binaries for the arm64 architecture are now available for linux

### Version 2.5.2 (February 23, 2022) <a href="#id-2.5.2" id="id-2.5.2"></a>

#### DNS server bugfix

Fixed a bug where Telepresence would use the last server in resolv.conf

### Version 2.5.1 (February 19, 2022) <a href="#id-2.5.1" id="id-2.5.1"></a>

#### Fix GKE auth issue

Fixed a bug where using a GKE cluster would error with: No Auth Provider found for name "gcp"

### Version 2.5.0 (February 18, 2022) <a href="#id-2.5.0" id="id-2.5.0"></a>

#### Intercept specific endpoints

The flags `--http-path-equal`, `--http-path-prefix`, and `--http-path-regex` can can be used in addition to the `--http-match` flag to filter personal intercepts by the request URL path

#### Intercept metadata

The flag `--http-meta` can be used to declare metadata key value pairs that will be returned by the Telepresence rest API endpoint `/intercept-info`

#### Client RBAC watch

The verb "watch" was added to the set of required verbs when accessing services and workloads for the client RBAC `ClusterRole`

#### Dropped backward compatibility with versions <=2.4.4

Telepresence is no longer backward compatible with versions 2.4.4 or older because the deprecated multiplexing tunnel functionality was removed.

#### No global networking flags

The global networking flags are no longer used and using them will render a deprecation warning unless they are supported by the command. The subcommands that support networking flags are `connect`, `current-cluster-id`, and `genyaml`.

#### Output of status command

The `also-proxy` and `never-proxy` subnets are now displayed correctly when using the `telepresence status` command.

#### SETENV sudo privilege no longer needed

Telepresence longer requires `SETENV` privileges when starting the root daemon.

#### Network device names containing dash

Telepresence will now parse device names containing dashes correctly when determining routes that it should never block.

#### Linux uses cluster.local as domain instead of search

The cluster domain (typically "cluster.local") is no longer added to the DNS `search` on Linux using `systemd-resolved`. Instead, it is added as a `domain` so that names ending with it are routed to the DNS server.

### Version 2.4.11 (February 10, 2022) <a href="#id-2.4.11" id="id-2.4.11"></a>

#### Add additional logging to troubleshoot intermittent issues with intercepts

We've noticed some issues with intercepts in v2.4.10, so we are releasing a version with enhanced logging to help debug and fix the issue.

### Version 2.4.10 (January 13, 2022) <a href="#id-2.4.10" id="id-2.4.10"></a>

#### Feature: Application Protocol Strategy

The strategy used when selecting the application protocol for personal intercepts can now be configured using the `intercept.appProtocolStrategy` in the `config.yml` file.

#### Helm value for the Application Protocol Strategy

The strategy when selecting the application protocol for personal intercepts in agents injected by the mutating webhook can now be configured using the `agentInjector.appProtocolStrategy` in the Helm chart.

#### New --http-plaintext option

The flag `--http-plaintext` can be used to ensure that an intercept uses plaintext http or grpc when communicating with the workstation process.

#### Configure the default intercept port

The port used by default in the `telepresence intercept` command (8080), can now be changed by setting the `intercept.defaultPort` in the `config.yml` file.

#### Change: Telepresence CI now uses Github Actions

Telepresence now uses Github Actions for doing unit and integration testing. It is now easier for contributors to run tests on PRs since maintainers can add an "ok to test" label to PRs (including from forks) to run integration tests.

#### Check conditions before asking questions

User will not be asked to log in or add ingress information when creating an intercept until a check has been made that the intercept is possible.

#### Fix invalid log statement

Telepresence will no longer log invalid: `"unhandled connection control message: code DIAL_OK"` errors.

#### Log errors from sshfs/sftp

Output to `stderr` from the traffic-agent's `sftp` and the client's `sshfs` processes are properly logged as errors.

#### Don't use Windows path separators in workload pod template

Auto installer will no longer not emit backslash separators for the `/tel-app-mounts` paths in the traffic-agent container spec when running on Windows.

### Version 2.4.9 (December 09, 2021) <a href="#id-2.4.9" id="id-2.4.9"></a>

#### Helm upgrade nil pointer error

A helm upgrade using the `--reuse-values` flag no longer fails on a "nil pointer" error caused by a nil `telpresenceAPI` value.

### Version 2.4.8 (December 03, 2021) <a href="#id-2.4.8" id="id-2.4.8"></a>

#### Feature: VPN diagnostics tool

There is a new subcommand, `test-vpn`, that can be used to diagnose connectivity issues with a VPN. See the VPN docs for more information on how to use it.

#### Feature: RESTful API service

A RESTful service was added to Telepresence, both locally to the client and to the `traffic-agent` to help determine if messages with a set of headers should be consumed or not from a message queue where the intercept headers are added to the messages.

#### TELEPRESENCE\_LOGIN\_CLIENT\_ID env variable no longer used

You could previously configure this value, but there was no reason to change it, so the value was removed.

#### Tunneled network connections behave more like ordinary TCP connections.

When using Telepresence with an external cloud provider for extensions, those tunneled connections now behave more like TCP connections, especially when it comes to timeouts. We've also added increased testing around these types of connections.

### Version 2.4.7 (November 24, 2021) <a href="#id-2.4.7" id="id-2.4.7"></a>

#### Injector service-name annotation

The agent injector now supports a new annotation, `telepresence.getambassador.io/inject-service-name`, that can be used to set the name of the service to be intercepted. This will help disambiguate which service to intercept for when a workload is exposed by multiple services, such as can happen with Argo Rollouts

#### Skip the Ingress Dialogue

You can now skip the ingress dialogue by setting the ingress parameters in the corresponding flags.

#### Never proxy subnets

The kubeconfig extensions now support a `never-proxy` argument, analogous to `also-proxy`, that defines a set of subnets that will never be proxied via telepresence.

#### Daemon versions check

Telepresence now checks the versions of the client and the daemons and asks the user to quit and restart if they don't match.

#### No explicit DNS flushes

Telepresence DNS now uses a very short TTL instead of explicitly flushing DNS by killing the `mDNSResponder` or doing `resolvectl flush-caches`

#### Legacy flags now work with global flags

Legacy flags such as `--swap-deployment` can now be used together with global flags.

#### Outbound connection closing

Outbound connections are now properly closed when the peer closes.

#### Prevent DNS recursion

The DNS-resolver will trap recursive resolution attempts (may happen when the cluster runs in a docker-container on the client).

#### Prevent network recursion

The TUN-device will trap failed connection attempts that results in recursive calls back into the TUN-device (may happen when the cluster runs in a docker-container on the client).

#### Traffic Manager deadlock fix

The Traffic Manager no longer runs a risk of entering a deadlock when a new Traffic agent arrives.

#### webhookRegistry config propagation

The configured `webhookRegistry` is now propagated to the webhook installer even if no `webhookAgentImage` has been set.

#### Login refreshes expired tokens

When a user's token has expired, `telepresence login` will prompt the user to log in again to get a new token. Previously, the user had to `telepresence quit` and `telepresence logout` to get a new token.

### Version 2.4.6 (November 02, 2021) <a href="#id-2.4.6" id="id-2.4.6"></a>

#### Manually injecting Traffic Agent

Telepresence now supports manually injecting the traffic-agent YAML into workload manifests. Use the `genyaml` command to create the sidecar YAML, then add the `telepresence.getambassador.io/manually-injected: "true"` annotation to your pods to allow Telepresence to intercept them.

#### Telepresence CLI released for Apple silicon

Telepresence is now built and released for Apple silicon.

#### Change: Telepresence help text now links to telepresence.io

We now include a link to our documentation when you run `telepresence --help`. This will make it easier for users to find this page whether they acquire Telepresence through Brew or some other mechanism.

#### Fixed bug when API server is inside CIDR range of pods/services

If the API server for your kubernetes cluster had an IP that fell within the subnet generated from pods/services in a kubernetes cluster, it would proxy traffic to the API server which would result in hanging or a failed connection. We now ensure that the API server is explicitly not proxied.

### Version 2.4.5 (October 15, 2021) <a href="#id-2.4.5" id="id-2.4.5"></a>

#### Feature: Get pod yaml with gather-logs command

Adding the flag `--get-pod-yaml` to your request will get the pod yaml manifest for all kubernetes components you are getting logs for (`traffic-manager` and/or pods containing a `traffic-agent` container). This flag is set to `false` by default.

#### Feature: Anonymize pod name + namespace when using gather-logs command

Adding the flag `--anonymize` to your command will anonymize your pod names + namespaces in the output file. We replace the sensitive names with simple names (e.g. pod-1, namespace-2) to maintain relationships between the objects without exposing the real names of your objects. This flag is set to `false` by default.

#### Feature: Added context and defaults to ingress questions when creating a preview URL

Previously, we referred to OSI model layers when asking these questions, but this terminology is not commonly used. The questions now provide a clearer context for the user, along with a default answer as an example.

#### Support for intercepting headless services

Intercepting headless services is now officially supported. You can request a headless service on whatever port it exposes and get a response from the intercept. This leverages the same approach as intercepting numeric ports when using the mutating webhook injector, mainly requires the `initContainer` to have `NET_ADMIN` capabilities.

#### Use one tunnel per connection instead of multiplexing into one tunnel

We have changed Telepresence so that it uses one tunnel per connection instead of multiplexing all connections into one tunnel. This will provide substantial performance improvements. Clients will still be backwards compatible with older managers that only support multiplexing.

#### Added checks for Telepresence kubernetes compatibility

Telepresence currently works with Kubernetes server versions `1.17.0` and higher. We have added logs in the connector and `traffic-manager` to let users know when they are using Telepresence with a cluster it doesn't support.

#### Traffic Agent security context is now only added when necessary

When creating an intercept, Telepresence will now only set the traffic agent's GID when strictly necessary (i.e. when using headless services or numeric ports). This mitigates an issue on openshift clusters where the traffic agent can fail to be created due to openshift's security policies banning arbitrary GIDs.

### Version 2.4.4 (September 27, 2021) <a href="#id-2.4.4" id="id-2.4.4"></a>

#### Numeric ports in agent injector

The agent injector now supports injecting Traffic Agents into pods that have unnamed ports.

#### Feature: New subcommand to gather logs and export into zip file

Telepresence has logs for various components (the `traffic-manager`, `traffic-agents`, the root and user daemons), which are integral for understanding and debugging Telepresence behavior. We have added the `telepresence gather-logs` command to make it simple to compile logs for all Telepresence components and export them in a zip file that can be shared to others and/or included in a github issue. For more information on usage, run `telepresence gather-logs --help`.

#### Pod CIDR strategy is configurable in Helm chart

Telepresence now enables you to directly configure how to get pod CIDRs when deploying Telepresence with the Helm chart. The default behavior remains the same. We've also introduced the ability to explicitly set what the pod CIDRs should be.

#### Compute pod CIDRs more efficiently

When computing subnets using the pod CIDRs, the traffic-manager now uses less CPU cycles.

#### Prevent busy loop in traffic-manager

In some circumstances, the `traffic-manager`'s CPU would max out and get pinned at its limit. This required a shutdown or pod restart to fix. We've added some fixes to prevent the traffic-manager from getting into this state.

#### Added a fixed buffer size to TUN-device

The TUN-device now has a max buffer size of 64K. This prevents the buffer from growing limitlessly until it receies a PSH, which could be a blocking operation when receiving lots of TCP-packets.

#### Fix hanging user daemon

When Telepresence encountered an issue connecting to the cluster or the root daemon, it could hang indefintely. It now will error correctly when it encounters that situation.

#### Improved proprietary agent connectivity

To determine whether the environment cluster is air-gapped, the proprietary agent attempts to connect to the cloud during startup. To deal with a possible initial failure, the agent backs off and retries the connection with an increasing backoff duration.

#### Telepresence correctly reports intercept port conflict

When creating a second intercept targeting the same local port, it now gives the user an informative error message. Additionally, it tells them which intercept is currently using that port to make it easier to remedy.

### Version 2.4.3 (September 15, 2021) <a href="#id-2.4.3" id="id-2.4.3"></a>

#### Environment variable TELEPRESENCE\_INTERCEPT\_ID available in interceptor's environment

When you perform an intercept, we now include a `TELEPRESENCE_INTERCEPT_ID` environment variable in the environment.

#### Improved daemon stability

Fixed a timing bug that sometimes caused a "daemon did not start" failure.

#### Complete logs for Windows

Crash stack traces and other errors were incorrectly not written to log files. This has been fixed so logs for Windows should be at parity with the ones in MacOS and Linux.

#### Log rotation fix for Linux kernel 4.11+

On Linux kernel 4.11 and above, the log file rotation now properly reads the `birth-time` of the log file. Older kernels continue to use the old behavior of using the `change-time` in place of the `birth-time`.

#### Improved error messaging

When Telepresence encounters an error, it tells the user where they should look for logs related to the error. We have refined this so that it only tells users to look for errors in the daemon logs for issues that are logged there.

#### Stop resolving localhost

When using the overriding DNS resolver, it will no longer apply search paths when resolving `localhost`, since that should be resolved on the user's machine instead of the cluster.

#### Variable cluster domain

Previously, the cluster domain was hardcoded to `cluster.local`. While this is true for many kubernetes clusters, it is not for all of them. Now this value is retrieved from the `traffic-manager`.

#### Improved cleanup of traffic-agents

Telepresence now uninstalls `traffic-agents` installed via mutating webhook when using `telepresence uninstall --everything`.

#### More large file transfer fixes

Downloading large files during an intercept will no longer cause timeouts and hanging `traffic-agents`.

#### Setting --mount to false when intercepting works as expected

When using `--mount=false` while performing an intercept, the file system was still mounted. This has been remedied so the intercept behavior respects the flag.

#### Traffic-manager establishes outbound connections in parallel

Previously, the `traffic-manager` established outbound connections sequentially. This resulted in slow (and failing) `Dial` calls would block all outbound traffic from the workstation (for up to 30 seconds). We now establish these connections in parallel so that won't occur.

#### Status command reports correct DNS settings

`Telepresence status` now correctly reports DNS settings for all operating systems, instead of `Local IP:nil, Remote IP:nil` when they don't exist.

### Version 2.4.2 (September 01, 2021) <a href="#id-2.4.2" id="id-2.4.2"></a>

#### New subcommand to temporarily change log-level

We have added a new `telepresence loglevel` subcommand that enables users to temporarily change the log-level for the local demons, the `traffic-manager` and the `traffic-agents`. While the `logLevels` settings from the config will still be used by default, this can be helpful if you are currently experiencing an issue and want to have higher fidelity logs, without doing a `telepresence quit` and `telepresence connect`. You can use `telepresence loglevel --help` to get more information on options for the command.

#### All components have info as the default log-level

We've now set the default for all components of Telepresence (traffic-agent, traffic-manager, local daemons) to use `info` as the default log-level.

#### Updating RBAC in helm chart to fix cluster-id regression

In 2.4.1, we enabled the `traffic-manager` to get the cluster ID by getting the UID of the default namespace. The helm chart was not updated to give the `traffic-manager` those permissions, which has since been fixed. This impacted users who use licensed features of the Telepresence extension in an air-gapped environment.

#### Timeouts for Helm actions are now respected

The user-defined timeout for Helm actions wasn't always respected, causing the daemon to hang indefinitely when failing to install the `traffic-manager`.

### Version 2.4.1 (August 30, 2021) <a href="#id-2.4.1" id="id-2.4.1"></a>

#### Feature: External cloud variables are now configurable

We now support configuring the host and port for the cloud in your `config.yml`. These are used when logging in to utilize features provided by an extension, and are also passed along as environment variables when installing the `traffic-manager`. Additionally, we now run our testsuite with these variables set to localhost to continue to ensure Telepresence is fully functional without depending on an external service. The SYSTEMA\_HOST and SYSTEMA\_PORT environment variables are no longer used.

#### Helm chart can now regenerate certificate used for mutating webhook on-demand.

You can now set `agentInjector.certificate.regenerate` when deploying Telepresence with the Helm chart to automatically regenerate the certificate used by the agent injector webhook.

#### Traffic Manager installed via helm

The traffic-manager is now installed via an embedded version of the Helm chart when `telepresence connect` is first performed on a cluster. This change is transparent to the user. A new configuration flag, `timeouts.helm` sets the timeouts for all helm operations performed by the Telepresence binary.

#### traffic-manager gets cluster ID itself instead of via environment variable

The traffic-manager used to get the cluster ID as an environment variable when running `telepresence connect` or via adding the value in the helm chart. This was clunky so now the traffic-manager gets the value itself as long as it has permissions to "get" and "list" namespaces (this has been updated in the helm chart).

#### Telepresence now mounts all directories from /var/run/secrets

In the past, we only mounted secret directories in `/var/run/secrets/kubernetes.io`. We now mount \*all\* directories in `/var/run/secrets`, which, for example, includes directories like `eks.amazonaws.com` used for IRSA tokens.

#### Max gRPC receive size correctly propagates to all grpc servers

This fixes a bug where the max gRPC receive size was only propagated to some of the grpc servers, causing failures when the message size was over the default.

#### Updated our Homebrew packaging to run manually

We made some updates to our script that packages Telepresence for Homebrew so that it can be run manually. This will enable maintainers of Telepresence to run the script manually should we ever need to rollback a release and have `latest` point to an older version.

#### Telepresence uses namespace from kubeconfig context on each call

In the past, Telepresence would use whatever namespace was specified in the kubeconfig's current-context for the entirety of the time a user was connected to Telepresence. This would lead to confusing behavior when a user changed the context in their kubeconfig and expected Telepresence to acknowledge that change. Telepresence now will do that and use the namespace designated by the context on each call.

#### Idle outbound TCP connections timeout increased to 7200 seconds

Some users were noticing that their intercepts would start failing after 60 seconds. This was because the keep idle outbound TCP connections were set to 60 seconds, which we have now bumped to 7200 seconds to match Linux's `tcp_keepalive_time` default.

#### Telepresence will automatically remove a socket upon ungraceful termination

When a Telepresence process terminates ungracefully, it would inform users that "this usually means that the process has terminated ungracefully" and implied that they should remove the socket. We've now made it so Telepresence will automatically attempt to remove the socket upon ungraceful termination.

#### Fixed user daemon deadlock

Remedied a situation where the user daemon could hang when a user was logged in.

#### Fixed agentImage config setting

The config setting `images.agentImages` is no longer required to contain the repository, and it will use the value at `images.repository`.

### Version 2.4.0 (August 04, 2021) <a href="#id-2.4.0" id="id-2.4.0"></a>

#### Feature: Windows Client Developer Preview

There is now a native Windows client for Telepresence that is being released as a Developer Preview. All the same features supported by the MacOS and Linux client are available on Windows.

#### Feature: CLI raises helpful messages from Ambassador Cloud

Telepresence can now receive messages from Ambassador Cloud and raise them to the user when they perform certain commands. This enables us to send you messages that may enhance your Telepresence experience when using certain commands. Frequency of messages can be configured in your `config.yml`.

#### Improved stability of systemd-resolved-based DNS

When initializing the `systemd-resolved`-based DNS, the routing domain is set to improve stability in non-standard configurations. This also enables the overriding resolver to do a proper take over once the DNS service ends.

#### Fixed an edge case when intercepting a container with multiple ports

When specifying a port of a container to intercept, if there was a container in the pod without ports, it was automatically selected. This has been fixed so we'll only choose the container with "no ports" if there's no container that explicitly matches the port used in your intercept.

#### $(NAME) references in agent's environments are now interpolated correctly.

If you had an environment variable $(NAME) in your workload that referenced another, intercepts would not correctly interpolate $(NAME). This has been fixed and works automatically.

#### Telepresence no longer prints INFO message when there is no config.yml

Fixed a regression that printed an INFO message to the terminal when there wasn't a `config.yml` present. The config is optional, so this message has been removed.

#### Telepresence no longer panics when using --http-match

Fixed a bug where Telepresence would panic if the value passed to `--http-match` didn't contain an equal sign, which has been fixed. The correct syntax is in the `--help` string and looks like `--http-match=HTTP2_HEADER=REGEX`

#### Improved subnet updates

The `traffic-manager` used to update subnets whenever the `Nodes` or `Pods` changed, even if the underlying subnet hadn't changed, which created a lot of unnecessary traffic between the client and the `traffic-manager`. This has been fixed so we only send updates when the subnets themselves actually change.

### Version 2.3.7 (July 23, 2021) <a href="#id-2.3.7" id="id-2.3.7"></a>

#### Also-proxy in telepresence status

An `also-proxy` entry in the Kubernetes cluster config will show up in the output of the `telepresence status` command.

#### Feature: Non-interactive telepresence login

`telepresence login` now has an `--apikey=KEY` flag that allows for non-interactive logins. This is useful for headless environments where launching a web-browser is impossible, such as cloud shells, Docker containers, or CI.

#### Mutating webhook injector correctly hides named ports for probes.

The mutating webhook injector has been fixed to correctly rename named ports for liveness and readiness probes

#### telepresence current-cluster-id crash fixed

Fixed a regression introduced in 2.3.5 that caused `telepresence current-cluster-id` to crash.

#### Better UX around intercepts with no local process running

Requests would hang indefinitely when initiating an intercept before you had a local process running. This has been fixed and will result in an `Empty reply from server` until you start a local process.

#### Bug Fix: API keys no longer show as "no description"

New API keys generated internally for communication with Ambassador Cloud no longer show up as "no description" in the Ambassador Cloud web UI. Existing API keys generated by older versions of Telepresence will still show up this way.

#### Fix corruption of user-info.json

Fixed a race condition that logging in and logging out rapidly could cause memory corruption or corruption of the `user-info.json` cache file used when authenticating with Ambassador Cloud.

#### Improved DNS resolver for systemd-resolved

Telepresence's `systemd-resolved`-based DNS resolver is now more stable and in case it fails to initialize, the `overriding resolver` will no longer cause general DNS lookup failures when telepresence defaults to using it.

#### Faster telepresence list command

The performance of `telepresence list` has been increased significantly by reducing the number of calls the command makes to the cluster.

### Version 2.3.6 (July 20, 2021) <a href="#id-2.3.6" id="id-2.3.6"></a>

#### Fix preview URLs

Fixed a regression introduced in 2.3.5 that caused preview URLs to not work.

#### Fix subnet discovery

Fixed a regression introduced in 2.3.5 where the Traffic Manager's `RoleBinding` did not correctly appoint the `traffic-manager` `Role`, causing subnet discovery to not be able to work correctly.

#### Fix root-user configuration loading

Fixed a regression introduced in 2.3.5 where the root daemon did not correctly read the configuration file; ignoring the user's configured log levels and timeouts.

#### Fix a user daemon crash

Fixed an issue that could cause the user daemon to crash during shutdown, as during shutdown it unconditionally attempted to close a channel even though the channel might already be closed.

### Version 2.3.5 (July 15, 2021) <a href="#id-2.3.5" id="id-2.3.5"></a>

#### Feature: traffic-manager in multiple namespaces

We now support installing multiple traffic managers in the same cluster. This will allow operators to install deployments of telepresence that are limited to certain namespaces.

<div align="left"><figure><img src=".gitbook/assets/000 tp 1.png" alt="" width="213"><figcaption></figcaption></figure></div>

#### No more dependence on kubectl

Telepresence no longer depends on having an external `kubectl` binary, which might not be present for OpenShift users (who have `oc` instead of `kubectl`).

#### Feature: Agent image now configurable

We now support configuring which agent image + registry to use in the config. This enables users whose laptop is an air-gapped environment to create personal intercepts without requiring a login. It also makes it easier for those who are developing on Telepresence to specify which agent image should be used. Env vars TELEPRESENCE\_AGENT\_IMAGE and TELEPRESENCE\_REGISTRY are no longer used.

<div align="left"><figure><img src=".gitbook/assets/000 tp 2.png" alt="" width="563"><figcaption></figcaption></figure></div>

#### Feature: Max gRPC receive size now configurable

The default max size of messages received through gRPC (4 MB) is sometimes insufficient. It can now be configured.

<div align="left"><figure><img src=".gitbook/assets/000 tp 3.png" alt="" width="291"><figcaption></figcaption></figure></div>

#### Feature: CLI can be used in air-gapped environments

While Telepresence will auto-detect if your cluster is in an air-gapped environment, we've added an option users can add to their config.yml to ensure the cli acts like it is in an air-gapped environment. Air-gapped environments require a manually installed license.

<div align="left"><figure><img src=".gitbook/assets/000 tp 4.png" alt="" width="563"><figcaption></figcaption></figure></div>

### Version 2.3.4 (July 09, 2021) <a href="#id-2.3.4" id="id-2.3.4"></a>

#### Bug Fix: Improved IP log statements

Some log statements were printing incorrect characters, when they should have been IP addresses. This has been resolved to include more accurate and useful logging.

<div align="left"><figure><img src=".gitbook/assets/000 tp 5.png" alt="" width="375"><figcaption></figcaption></figure></div>

#### Bug Fix: Improved messaging when multiple services match a workload

If multiple services matched a workload when performing an intercept, Telepresence would crash. It now gives the correct error message, instructing the user on how to specify which service the intercept should use.

<div align="left"><figure><img src=".gitbook/assets/000 tp 6.png" alt="" width="563"><figcaption></figcaption></figure></div>

#### Traffic-manger creates services in its own namespace to determine subnet

Telepresence will now determine the service subnet by creating a dummy-service in its own namespace, instead of the default namespace, which was causing RBAC permissions issues in some clusters.

#### Telepresence connect respects pre-existing clusterrole

When Telepresence connects, if the `traffic-manager`'s desired `clusterrole` already exists in the cluster, Telepresence will no longer try to update the clusterrole.

#### Helm Chart fixed for clientRbac.namespaced

The Telepresence Helm chart no longer fails when installing with `--set clientRbac.namespaced=true`.

### Version 2.3.3 (July 07, 2021) <a href="#id-2.3.3" id="id-2.3.3"></a>

#### Feature: Traffic Manager Helm Chart

Telepresence now supports installing the Traffic Manager via Helm. This will make it easy for operators to install and configure the server-side components of Telepresence separately from the CLI (which in turn allows for better separation of permissions).

<div align="left"><figure><img src=".gitbook/assets/000 tp 7.png" alt="" width="366"><figcaption></figcaption></figure></div>

#### Feature: Traffic-manager in custom namespace

As the `traffic-manager` can now be installed in any namespace via Helm, Telepresence can now be configured to look for the Traffic Manager in a namespace other than `ambassador`. This can be configured on a per-cluster basis.

<div align="left"><figure><img src=".gitbook/assets/000 tp 8.png" alt="" width="284"><figcaption></figcaption></figure></div>

#### Feature: Intercept --to-pod

`telepresence intercept` now supports a `--to-pod` flag that can be used to port-forward sidecars' ports from an intercepted pod.

<div align="left"><figure><img src=".gitbook/assets/000 tp 9.png" alt="" width="375"><figcaption></figcaption></figure></div>

#### Change in migration from edgectl

Telepresence no longer automatically shuts down the old `api_version=1` `edgectl` daemon. If migrating from such an old version of `edgectl` you must now manually shut down the `edgectl` daemon before running Telepresence. This was already the case when migrating from the newer `api_version=2` `edgectl`.

#### Fixed error during shutdown

The root daemon no longer terminates when the user daemon disconnects from its gRPC streams, and instead waits to be terminated by the CLI. This could cause problems with things not being cleaned up correctly.

#### Intercepts will survive deletion of intercepted pod

An intercept will survive deletion of the intercepted pod provided that another pod is created (or already exists) that can take over.

### Version 2.3.2 (June 18, 2021) <a href="#id-2.3.2" id="id-2.3.2"></a>

#### Feature: Service Port Annotation

The mutator webhook for injecting traffic-agents now recognizes a `telepresence.getambassador.io/inject-service-port` annotation to specify which port to intercept; bringing the functionality of the `--port` flag to users who use the mutator webook in order to control Telepresence via GitOps.

<div align="left"><figure><img src=".gitbook/assets/000 tp 10.png" alt="" width="563"><figcaption></figcaption></figure></div>

#### Outbound Connections

Outbound connections are now routed through the intercepted Pods which means that the connections originate from that Pod from the cluster's perspective. This allows service meshes to correctly identify the traffic.

#### Inbound Connections

Inbound connections from an intercepted agent are now tunneled to the manager over the existing gRPC connection, instead of establishing a new connection to the manager for each inbound connection. This avoids interference from certain service mesh configurations.

#### Traffic Manager needs new RBAC permissions

The Traffic Manager requires [RBAC permissions](technical-reference/rbac.md) to list Nodes, Pods, and to create a dummy Service in the manager's namespace.

#### Reduced developer RBAC requirements

The on-laptop client no longer requires [RBAC permissions](technical-reference/rbac.md) to list the Nodes in the cluster or to create Services, as that functionality has been moved to the Traffic Manager.

#### Bug Fix: Able to detect subnets

Telepresence will now detect the Pod CIDR ranges even if they are not listed in the Nodes.

<div align="left"><figure><img src=".gitbook/assets/000 tp 11.png" alt="" width="375"><figcaption></figcaption></figure></div>

#### Dynamic IP ranges

The list of cluster subnets that the virtual network interface will route is now configured dynamically and will follow changes in the cluster.

#### No duplicate subnets

Subnets fully covered by other subnets are now pruned internally and thus never superfluously added to the laptop's routing table.

#### Change in default timeout

The `trafficManagerAPI` timeout default has changed from 5 seconds to 15 seconds, in order to facilitate the extended time it takes for the traffic-manager to do its initial discovery of cluster info as a result of the above bugfixes.

#### Removal of DNS config files on macOS

On macOS, files generated under `/etc/resolver/` as the result of using `include-suffixes` in the cluster config are now properly removed on quit.

#### Large file transfers

Telepresence no longer erroneously terminates connections early when sending a large HTTP response from an intercepted service.

#### Race condition in shutdown

When shutting down the user-daemon or root-daemon on the laptop, `telepresence quit` and related commands no longer return early before everything is fully shut down. Now it can be counted on that by the time the command has returned that all of the side-effects on the laptop have been cleaned up.

### Version 2.3.1 (June 14, 2021) <a href="#id-2.3.1" id="id-2.3.1"></a>

#### Feature: DNS Resolver Configuration

Telepresence now supports per-cluster configuration for custom dns behavior, which will enable users to determine which local + remote resolver to use and which suffixes should be ignored + included. These can be configured on a per-cluster basis.

<div align="left"><figure><img src=".gitbook/assets/000 tp 12.png" alt="" width="191"><figcaption></figcaption></figure></div>

#### Feature: AlsoProxy Configuration

Telepresence now supports also proxying user-specified subnets so that they can access external services only accessible to the cluster while connected to Telepresence. These can be configured on a per-cluster basis and each subnet is added to the TUN device so that requests are routed to the cluster for IPs that fall within that subnet.

<div align="left"><figure><img src=".gitbook/assets/000 tp 13.png" alt="" width="375"><figcaption></figcaption></figure></div>

#### Feature: Mutating Webhook for Injecting Traffic Agents

The Traffic Manager now contains a mutating webhook to automatically add an agent to pods that have the `telepresence.getambassador.io/traffic-agent: enabled` annotation. This enables Telepresence to work well with GitOps CD platforms that rely on higher level kubernetes objects matching what is stored in git. For workloads without the annotation, Telepresence will add the agent the way it has in the past

<figure><img src=".gitbook/assets/000 tp 14.png" alt=""><figcaption></figcaption></figure>

#### Change: Traffic Manager Connect Timeout

The trafficManagerConnect timeout default has changed from 20 seconds to 60 seconds, in order to facilitate the extended time it takes to apply everything needed for the mutator webhook.

<div align="left"><figure><img src=".gitbook/assets/000 tp 15.png" alt="" width="375"><figcaption></figcaption></figure></div>

#### Bug Fix: Fix for large file transfers

Fix a tun-device bug where sometimes large transfers from services on the cluster would hang indefinitely

<figure><img src=".gitbook/assets/000 tp 16.png" alt=""><figcaption></figcaption></figure>

#### Change: Brew Formula Changed

Now that the Telepresence rewrite is the main version of Telepresence, you can install it via Brew like so: `brew install datawire/blackbird/telepresence`.

<figure><img src=".gitbook/assets/000 tp 17.png" alt=""><figcaption></figcaption></figure>

### Version 2.3.0 (June 01, 2021) <a href="#id-2.3.0" id="id-2.3.0"></a>

#### Feature: Brew install Telepresence

Telepresence can now be installed via brew on macOS, which makes it easier for users to stay up-to-date with the latest telepresence version. To install via brew, you can use the following command: `brew install datawire/blackbird/telepresence2`.

<div align="left"><figure><img src=".gitbook/assets/000 tp 18.png" alt="" width="375"><figcaption></figcaption></figure></div>

#### Feature: TCP and UDP routing via Virtual Network Interface

Telepresence will now perform routing of outbound TCP and UDP traffic via a Virtual Network Interface (VIF). The VIF is a layer 3 TUN-device that exists while Telepresence is connected. It makes the subnets in the cluster available to the workstation and will also route DNS requests to the cluster and forward them to intercepted pods. This means that pods with custom DNS configuration will work as expected. Prior versions of Telepresence would use firewall rules and were only capable of routing TCP.

<div align="left"><figure><img src=".gitbook/assets/000 tp 19.png" alt="" width="563"><figcaption></figcaption></figure></div>

#### Change: SSH is no longer used

All traffic between the client and the cluster is now tunneled via the traffic manager gRPC API. This means that Telepresence no longer uses ssh tunnels and that the manager no longer have an `sshd` installed. Volume mounts are still established using `sshfs` but it is now configured to communicate using the sftp-protocol directly, which means that the traffic agent also runs without `sshd`. A desired side effect of this is that the manager and agent containers no longer need a special user configuration.

<div align="left"><figure><img src=".gitbook/assets/000 tp 20.png" alt="" width="191"><figcaption></figcaption></figure></div>

#### Feature: Running in a Docker container

Telepresence can now be run inside a Docker container. This can be useful for avoiding side effects on a workstation's network, establishing multiple sessions with the traffic manager, or working with different clusters simultaneously.

<div align="left"><figure><img src=".gitbook/assets/000 tp 21.png" alt="" width="311"><figcaption></figcaption></figure></div>

#### Feature: Configurable Log Levels

Telepresence now supports configuring the log level for Root Daemon and User Daemon logs. This provides control over the nature and volume of information that Telepresence generates in `daemon.log` and `connector.log`.

<div align="left"><figure><img src=".gitbook/assets/000 tp 22.png" alt="" width="195"><figcaption></figcaption></figure></div>

### Version 2.2.2 (May 17, 2021) <a href="#id-2.2.2" id="id-2.2.2"></a>

#### Feature: Legacy Telepresence subcommands

Telepresence is now able to translate common legacy Telepresence commands into native Telepresence commands. So if you want to get started quickly, you can just use the same legacy Telepresence commands you are used to with the new Telepresence binary.

<div align="left"><figure><img src=".gitbook/assets/000 tp 23.png" alt="" width="194"><figcaption></figcaption></figure></div>
