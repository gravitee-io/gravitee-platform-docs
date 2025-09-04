---
noIndex: true
---

# Deployment

This reference provides a list of commands, arguments, and flags you can use to work with deployment instances in Blackbird.

## blackbird deployment create

### Description

Containerizes and deploys code to your Blackbird-hosted environment.

```shell
blackbird deployment create <name> --dockerfile=DOCKERFILE --context=STRING
```

### Required arguments

`name`

The name of the deployment you want to create.

### Required flags

`-d`, `--dockerfile=DOCKERFILE`

The path to a Dockerfile.

`-c`, `--context=STRING`

The path to the source code directory you want to include in the image.

### Optional flags

`--build-arg`

A build-time variable for Docker using a `KEY=VALUE` format. You can set this flag multiple times to pass multiple variables (e.g., `--build-arg KEY=VALUE` `--build-arg KEY=VALUE`).

`-e`, `--envfile=ENVFILE`

The path to a .env file that contains lines of `KEY=VALUE`.

`-n`, `--image-name`

The name of the Docker image you want to deploy. The format must be `REGISTRY/IMAGE`.

`-p`, `--port=CONTAINER_PORT`

The port on which the container is listening for requests. If not specified, defaults to port 80.

`-t`, `--protocol=STRING`

The protocol you want to use for the deployment. Supported values include `HTTP` and `TCP`. The default is `HTTP`.

TCP deployments are only accessible within the hosted environment by other Blackbird deployments. These deployments are useful for services that communicate over TCP, such as PostgreSQL, and don't expose a public URL. HTTP deployments are reachable from outside the hosted environment and include a publicly accessible URL.

`--apikey-header=STRING`

The name of the API key header you want to enable for this deployment.

`-w`, `--wait`

Waits for the operation to complete (default true)

### Examples

The following example containerizes and deploys an application named "simple-api" using a Dockerfile and source code in the current directory.

```shell
blackbird deployment create simple-api -d Dockerfile -c .
```

The following example creates a new deployment using the NGINX Docker image provided by the `--image-name` flag.

```shell
blackbird deployment create simple-api --image-name docker/nginx:latest
```

## blackbird deployment list

### Description

Lists all deployments.

### Optional Flags

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.

## blackbird deployment status

### Description

Shows detailed information about a deployment.

```shell
blackbird deployment status <name>
```

### Required arguments

`name`

The name of the deployment for which you want to show details.

### Optional flags

`-l`, `--logs`

Shows application logs for the deployment.

## blackbird deployment update

Updates an existing deployment in the hosted environment.

```shell
blackbird deployment update <name> --dockerfile=DOCKERFILE --context=STRING
```

### Required arguments

`name`

The name of the deployment you want to update.

### Required flags

`--build-arg`

A build-time variable for Docker using a `KEY=VALUE` format. You can set this flag multiple times to pass multiple variables (e.g., `--build-arg KEY=VALUE` `--build-arg KEY=VALUE`).

`-d`, `--dockerfile=DOCKERFILE`

The path to a Dockerfile.

`-c`, `--context=STRING`

The path to the source code directory you want to include in the image.

### Optional flags

`-e`, `--envfile=ENVFILE`

The path to a .env file that contains lines of KEY=VALUE.

`--apikey-header=STRING`

The name of the API key header you want to enable for this deployment.

### Examples

The following example updates a deployment named "simple-api" using a Dockerfile named "Dockerfile" and source code in the current directory. This builds a new image and replaces the existing image in the hosted environment.

```shell
blackbird deployment update simple-api -d Dockerfile -c .
```

## blackbird deployment delete

Removes a deployment.

```shell
blackbird deployment delete <name>
```

### Required arguments

`name`

The name of the deployment you want to delete.
