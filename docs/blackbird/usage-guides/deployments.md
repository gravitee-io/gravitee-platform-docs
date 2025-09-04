---
noIndex: true
---

# Deployments

Blackbird provides non-production deployments that allow you to test and validate changes to your API specifications in an isolated environment without impacting production systems. This ensures safe iteration, supports team collaboration, and enables secure, consistent testing using Docker. You can use and manage deployments in the Blackbird UI and CLI.

> **Note:** Blackbird deployments route traffic through a fixed set of static IP addresses. If your infrastructure restricts access based on IP, you can allowlist the following addresses to permit traffic from your deployment: `35.225.75.92`, `34.44.86.39`, `34.170.27.7`, `35.239.47.110`, `35.192.6.178`

## Prerequisites

* You have an API in your Blackbird catalog.
* You installed the Blackbird CLI. For more information see [#getting-started-with-the-blackbird-cli](../technical-reference/blackbird-cli/#getting-started-with-the-blackbird-cli "mention").
* You installed Docker. For more information, see [Get Docker](https://docs.docker.com/get-started/get-docker/).

## Using deployments in the UI

The Blackbird UI provides a user-friendly interface to help you interact with Blackbird deployments.

### View a deployment in the UI

To view your deployments and their details in the UI, choose **Deployments** in the left pane.

## Using deployments with the CLI

The Blackbird CLI provides a fast and flexible way to interact with your deployments directly from the command line.

> **Note:** For a full list of CLI commands, see [deployment.md](../technical-reference/blackbird-cli/deployment.md "mention") in the _Blackbird CLI Reference_.

### Create a deployment with the CLI

You can use the CLI to create a new deployment by running the following command.

```shell
blackbird deployment create --dockerfile=<DOCKERFILE> --context=PATH --port=<CONTAINER_PORT> <name>
```

### Communicate across deployments

If you want your deployments to reference one another, use the following process.

1.  Create an `.env` file and define environment variables that specify the name and port of each target service.

    ```env
    SERVICE_B_URL=http://service-b:80
    ```
2.  Deploy the service using the `--envfile` flag.

    ```shell
    blackbird deployment create --dockerfile=DOCKERFILE --context=STRING <name> --envfile=FILE
    ```

### View a list of your deployments in the CLI

You can use the CLI to list your deployments using the following command.

```shell
blackbird deployment list
```

### Update a deployment with the CLI

You can update a deployment using the following command.

```shell
blackbird deployment update --dockerfile=<DOCKERFILE> --context=PATH --port=<CONTAINER_PORT> <name>
```

### Check a deployment's status with the CLI

You can check the status of a running deployment using one of the following options.

To check the status without application logs, use the following command.

```shell
blackbird deployment status <name>
```

To check the status with application logs, use the following command.

```shell
blackbird deployment status <name> -l
```

### Delete a deployment with the CLI

You can delete a running deployment using the following command.

```shell
blackbird deployment delete <name>
```

### Secure a deployment with the CLI

By default, deployment endpoints are publicly available. However, you can secure the endpoints by using API keys or creating and automatically applying API keys when you create a deployment.

To create and apply an API key when you create a deployment, use the API key header flag in the following command.

```shell
blackbird deployment create --dockerfile=<DOCKERFILE> --context=STRING --api-name=<SLUG_NAME> --apikey-header=<HeaderKey> <name>
```

> **Note:** For information on how to secure an existing mock endpoint, see [secure-instances-on-blackbird.md](../technical-reference/secure-instances-on-blackbird.md "mention").

## Understanding limitations

Consider the following limitation while working with deployments.

### Containers can't run as root

Deployment images aren't allowed to run as the root user. You can use the root user during the image build process, but you must switch to a non-root user before the final image is run.

For example:

```dockerfile
FROM alpine:latest

COPY /build/server /usr/bin/server
RUN chmod +x /usr/bin/server

USER 1000

ENTRYPOINT ["/usr/bin/server"]
```

## Troubleshooting deployments

### Deployment state never changes to `ready`

If a deployment remains in a pending or non-ready state, it may be due to one of the following issues:

* **The container is running as root** – Blackbird deployments don't support containers running as the root user. Switch to a non-root user in your Dockerfile.
* **There's no process running, or the process runs but exits** – If your container exits immediately after starting, it might not have a defined entry point or the process it runs terminated.
  * Ensure your Dockerfile includes a valid `ENTRYPOINT`.
  *   Use the deployment logs to diagnose the issue.

      ```shell
      blackbird deployment status <name> -l
      ```

### Upstream connect error

`upstream connect error or disconnect/reset before headers. reset reason: connection failure, transport failure reason: delayed connect error: 111`

This error typically indicates that the port specified in the `deployment create` or `deployment update` command doesn't match the container's port.
