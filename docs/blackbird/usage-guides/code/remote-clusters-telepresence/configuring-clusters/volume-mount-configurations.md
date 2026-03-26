---
description: Overview of Volume Mount Configurations.
noIndex: true
---

# Volume Mount Configurations

Blackbird cluster (powered by Telepresence) supports locally mounting volumes that are mounted to your Pods. You can specify a command to run when starting the intercept, such as a subshell or local server (e.g., Python or Node).

In the following example, Blackbird creates the intercept, mounts the Pod's volumes locally to `/tmp`, and starts a Bash subshell.

```shell
blackbird cluster intercept <mysvc> --port <port> --mount=/tmp/ -- /bin/bash
```

Blackbird can also set a random mount point for you by using `--mount=true`. You can then find the mount point in the output of `blackbird cluster list` or using the `$TELEPRESENCE_ROOT` variable.

```
$ blackbird cluster intercept <mysvc> --port <port> --mount=true -- /bin/bash
Using Deployment <mysvc>
intercepted
    Intercept name    : <mysvc>
    State             : ACTIVE
    Workload kind     : Deployment
    Destination       : 127.0.0.1:<port>
    Volume Mount Point: /var/folders/cp/2r22shfd50d9ymgrw14fd23r0000gp/T/telfs-988349784
    Intercepting      : all TCP connections

bash-3.2$ echo $TELEPRESENCE_ROOT
/var/folders/cp/2r22shfd50d9ymgrw14fd23r0000gp/T/telfs-988349784
```

`--mount=true` is the default. If a `mount` option isn't specified, use `--mount=false` to disable mounting volumes. With either approach, the code you run locally—either from the subshell or from the intercept command—will need to be prepended with the `$TELEPRESENCE_ROOT` environment variable to utilize the mounted volumes. For example, Kubernetes mounts secrets to `/var/run/secrets/kubernetes.io`, even if no `mountPoint` for it exists in the Pod specification. To access them, you'd need to change your code to use `$TELEPRESENCE_ROOT/var/run/secrets/kubernetes.io`.

## Using Docker volumes

When you connect to a cluster using `blackbird cluster connect --docker` and then intercept using `--docker-run`, or when you use `docker` intercept handlers in an intercept specification, Blackbird will mount volumes using the [Telemount](https://github.com/datawire/docker-volume-telemount) Docker volume plugin. The mounts will use the same paths as the intercepted container. Telepresence will install the volume plugin on demand from `docker.io/datawire/telemount`.

## Hiding volumes

By default, all volumes mounted by an intercepted Pod are available locally. This behavior can be overridden by adding the `telepresence.getambassador.io/inject-ignore-volume-mounts` annotation to the workload defining the intercepting Pod. The annotation instructs the injector to ignore specific volume mounts. Its value is a comma-separated list of volume mount names to exclude. Any matching mounts won't be exposed to intercepting clients.

```diff
 spec:
   template:
     metadata:
       annotations:
+        telepresence.getambassador.io/inject-ignore-volume-mounts: "foo,bar"
     spec:
       containers:
```
