---
description: Overview of Volume Mounts.
noIndex: true
---

# Volume Mounts

Telepresence supports locally mounting of volumes that are mounted to your Pods. You can specify a command to run when starting the intercept, this could be a subshell or local server such as Python or Node.

```
telepresence intercept <mysvc> --port <port> --mount=/tmp/ -- /bin/bash
```

In this case, Telepresence creates the intercept, mounts the Pod's volumes to locally to `/tmp`, and starts a Bash subshell.

Telepresence can set a random mount point for you by using `--mount=true` instead, you can then find the mount point in the output of `telepresence list` or using the `$TELEPRESENCE_ROOT` variable.

```
$ telepresence intercept <mysvc> --port <port> --mount=true -- /bin/bash
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

{% hint style="info" %}
`--mount=true` is the default if a `mount` option is not specified, use `--mount=false` to disable mounting volumes.
{% endhint %}

With either method, the code you run locally either from the subshell or from the intercept command will need to be prepended with the `$TELEPRESENCE_ROOT` environment variable to utilize the mounted volumes.

For example, Kubernetes mounts secrets to `/var/run/secrets/kubernetes.io` (even if no `mountPoint` for it exists in the Pod spec). Once mounted, to access these you would need to change your code to use `$TELEPRESENCE_ROOT/var/run/secrets/kubernetes.io`.

{% hint style="info" %}
If using `--mount=true` without a command, you can use either [environment variable](environment-variables.md) flag to retrieve the variable.
{% endhint %}

## Docker volumes

When connecting to a cluster using `telepresence connect --docker` and then intercepting using `--docker-run`, or when using `docker` intercept handlers in an [Intercept Specification](intercepts/configure-intercept-using-specifications.md), telepresence will mount volumes using the [Telemount](https://github.com/datawire/docker-volume-telemount) Docker volume plugin. The mounts will use the same paths as the intercepted container.

Telepresence will install the volume-plugin on demand from `docker.io/datawire/telemount`.

## Hide Certain Volumes

Telepresence's default behavior is to make all volumes that an intercepted pod mounts available locally. This behavior can be overridden by adding the annotation `telepresence.getambassador.io/inject-ignore-volume-mounts` to the workload that describes the intercepted pod. The annotation will make the injector ignore certain volume mounts. The annotation value is a comma-separated list, where each item is the `name` of a volume mount that should be ignored. The matching mounts will never be exposed to intercepting clients.

```diff
 spec:
   template:
     metadata:
       annotations:
+        telepresence.getambassador.io/inject-ignore-volume-mounts: "foo,bar"
     spec:
       containers:
```
