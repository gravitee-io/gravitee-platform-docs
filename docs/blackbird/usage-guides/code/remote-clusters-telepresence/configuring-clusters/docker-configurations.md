---
description: Overview of Docker Configurations.
noIndex: true
---

# Docker Configurations

When used with Docker, Blackbird cluster (powered by Telepresence) enables a container running on your local machine to act as if it were inside the cluster. This allows you to accelerate your development cycles by providing a fast and efficient way to iterate code changes without requiring administrative access on your machines.

Using this page, you can learn about:

* [Using Docker with Blackbird](docker-configurations.md#using-docker-with-blackbird)
* [Using Docker Compose with Blackbird](docker-configurations.md#using-docker-compose-with-blackbird)

## Using Docker with Blackbird

You can run a single service locally while seamlessly connecting it to a remote Kubernetes cluster.

### Prerequisites

* You can access a Kubernetes cluster using the Kubernetes CLI (kubectl).
* Your application is deployed in a remote cluster and accessible using a Kubernetes service.
* You have access to the Docker Desktop, which is a tool for building and sharing containerized applications and microservices. You'll use Docker Desktop to run a local development environment.

### Enable Docker

To use Docker with Blackbird, add the Docker flag to any Blackbird cluster command, and it will start your daemon in a container. This removes the need for root access, making it easier to adopt.

**To enable Docker:**

1.  Log into the Blackbird CLI and confirm the daemons aren't running.

    ```shell
    blackbird cluster status
    ```

    > **Note:** If you're a macOS user and you receive an error saying that the developer cannot be verified, open **System Preferences>Security & Privacy>General**. Then, choose **Open Anyway** to bypass the security block and retry the command.
2.  Install the Helm chart and quit Blackbird.

    ```shell
    blackbird cluster helm install
    blackbird cluster quit -s
    ```
3.  Connect to the remote cluster using Docker.

    ```shell
    blackbird connect --docker
    ```
4.  Verify that you're connected to the remote cluster by listing your Docker containers.

    ```shell
    docker ps
    ```

    > **Note:** This method limits the scope of potential networking issues because your artifacts stay inside Docker.

### Using intercepts with Docker

To use intercepts with Docker, you can use an intercept specification or flags.

You can use the following flags when working with intercepts with Docker.

#### --docker

You can start the Blackbird daemon in a Docker container on your laptop using the following command: `blackbird cluster connect --docker`

The `--docker` flag is a global flag, and you can pass it directly (similar to `blackbird cluster intercept --docker`). The implicit connect that takes place if no connections is active will use a container-based daemon.

#### ---docker-run

If you want your intercept to go to another Docker container, you can use the `--docker-run` flag. It creates the intercept, runs your container, and then automatically ends the intercept when the container exits. For example:

```shell
blackbird cluster intercept <service_name> --port <port> --docker-run -- <docker run arguments> <image> <container arguments>
```

In the example, `--` separates the flags for `blackbird cluster intercept` and the flags intended for Docker. We recommend that you always use the `--docker-run` command with the global `--docker` flag, because it minimizes interference. When you use both flags, the network for the intercept handler will be set to the same network used by the daemon. This guarantees that the intercept handler can access the Blackbird virtual network interface (VIF) the cluster. Volume mounts are automatic and made using the Telemount Docker volume plugin so all volumes exposed by the intercepted container are mounted on the intercept handler container. The environment of the intercepted container becomes the environment of the intercept handler container.

> **Note:** You don't need administrative user access to use these commands, because network modifications are confined to a Docker network. Also, you don't need a special filesystem mount software like MacFUSE or WinFSP. The volume mounts happen in the Docker engine.

#### --docker-build

You can allow the intercept command to build containers dynamically using the `--docker-build <docker context>` and `docker-build-opt key=value` flags. When using `--docker-build`, the image name used in the argument list must be `IMAGE`. The word acts as a placeholder and will be replaced by the ID of the image that's built.

> **Note:** The `--docker-build` flag implies `--docker-run`.

#### --docker run (without Docker)

You can use the `--docker-run` flag with a daemon running on your local host, which is Blackbird's default behavior. However, we recommend that you don't do this, because while your intercept runs in a container, the daemon will modify the host network, and if remote mounts are desired, they may require extra software.

#### Automatic flags

Blackbird automatically passes several relevant flags to Docker to connect the container with the intercept. The flags are combined with arguments provided after `--` on the command line.

The following flags are automatic:

* `--env-file <file>`: Loads the intercepted environment.
* `--name intercept-<intercept name>-<intercept port>`: Names the Docker container. This flag is omitted if explicitly provided on the command line.
* `-v <local mount dir:docker mount dir>`: The volume mount specification.

The following flags are automatic when used with a container-based daemon:

* `--rm`: This is mandatory, because the volume mounts can't be removed until the container is removed
* `-v <telemount volume>:<docker mount dir>`: The volume mount specifications propagated from the intercepted container.

The following flags are automatic when used with a daemon that isn't container-based:

* `--dns-search tel2-search`: Enables single-label name lookups in intercepted namespaces
* `-p <port:container-port>`: The local port for the intercept and the container port.

## Using Docker Compose with Blackbird

When running an existing Docker Compose specification locally, testing it within a cluster by intercepting services presents several issues. The cluster's network configuration, intercepted Pods, environment variables, volume mounts, and specific services you want to redirect are unknown to Docker Compose. Additionally, environment variables and volume mounts are only determined at the time of an active intercept.

Blackbird addresses this by generating a temporary, modified version of the Compose file when you create an intercept. This ephemeral configuration ensures compatibility with the cluster environment while maintaining the original Compose structure. Use this page to learn how to modify Blackbird during this process.

### Service behavior

You can start by declaring how each service in the Docker Compose file is intended to behave. You can declare these intentinos directly in the intercept specification so the Docker Compose file is left untouched, or they can be added to the docker compose spec. in the form of `x-telepresence` extensions.

The intended behavior can be one of `interceptHandler`, `remote`, or `local`, where `local` is the default that applies to all services that have no intended behavior specified.

#### interceptHandler behavior

A Docker Compose service using the `interceptHandler` behavior will handle traffic from the intercepted Pod, remotely mount the volumes of the intercepted Pod, and have access to the environment variables of the intercepted Pod. This means that Blackbird will:

* Modify the network-mode of the Docker Compose service so that it shares the network of the containerized Blackbird daemon.
* Modify the environment of the service to include the environment variables exposed by the intercepted Pod.
* Create volumes that correspond to the volumes of the intercepted pod and replace volumes on the Docker Compose service that have overlapping targets.
* Delete any networks from the service and, instead, attach those networks to the daemon.
* Delete any exposed ports and, instead, expose them using the Blackbird network.

#### Remote behavior

A Docker Compose service using the remote behavior won't run locally. Instead, Blackbird will:

* Remove the service from the Docker Compose specification.
* Reassign any `depends_on` references for that service to the dependencies of that services instead.
* Inform the containerized Blackbird daemon about the mapping that was declared in the service intent.
