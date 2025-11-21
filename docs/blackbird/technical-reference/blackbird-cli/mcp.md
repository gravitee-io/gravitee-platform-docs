---
noIndex: true
---

# MCP

This reference provides a list of commands, arguments, and flags you can use to work with Model Context Protocol (MCP) servers in Blackbird.

## blackbird mcp catalog

### Description

Lists available MCP servers in the Blackbird MCP catalog. This command retrieves the catalog of MCPs and displays them in a structured format.

```shell
blackbird mcp catalog [--name <name>] [--output <format>]
```

### Optional Flags

`-n`, `--name=STRING`

Filters the catalog by MCP name.

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`. If not specified, defaults to `table`.

### Examples

The following example lists all available MCP servers.

```shell
blackbird mcp catalog
```

The following example lists the details of a specific MCP server.

```shell
blackbird mcp catalog --name my-mcp
```

The following example outputs the MCP catalog in JSON.

```shell
blackbird mcp catalog --output json
```

## blackbird mcp create

### Description

Containerizes and deploys code to a hosted environment.

```shell
blackbird mcp create --dockerfile=DOCKERFILE --context=STRING <name>
```

### Required Arguments

`name`

The name of the MCP server you want to create.

### Required Flags

`-d`, `--dockerfile=DOCKERFILE`

The path to a Dockerfile.

`-c`, `--context=STRING`

The path to the source code directory to include in the image.

### Optional Flags

`-e`, `--envfile=ENVFILE` The path to a .env file that contains lines of KEY=VALUE pairs.

`-n`, `--image-name=STRING`

The name of the image you want to deploy.

`-p`, `--port=PORT`

The port on which the container is listening for requests. If not specified, defaults to port 80.

`-t`, `--protocol=STRING`

The protocol you want to use for the deployment. Supported values include `HTTP` and `TCP`. The default is `HTTP`.

`-r`, `--registry=STRING`

The registry URL where deployment images are pushed.

`--apikey-header=STRING`

The name of an API key header you want to enable for this deployment.

`-w`, `--wait`

Waits for the operation to complete. If not specified, defaults to `true`.

### Examples

The following example creates a new MCP server using the default settings.

```shell
blackbird mcp create my-mcp -d Dockerfile -c .
```

The following example creates an MCP server with a custom portal and protocol.

```shell
blackbird mcp create my-mcp -d Dockerfile -c . -p 8080 -t HTTP
```

The following example creates an MCP server with environment variables.

```shell
blackbird mcp create my-mcp -d Dockerfile -c . -e .env
```

## blackbird mcp delete

### Description

Deletes an MCP deployment from the Blackbird catalog.

```shell
blackbird mcp delete <name>
```

### Required Arguments

`name` The name of the MCP server you want to delete.

### Examples

The following example deletes an MCP server called `my-mcp` from the Blackbird catalog.

```shell
blackbird mcp delete my-mcp
```

## blackbird mcp export

### Description

Generates connection details for an MCP server. This command retrieves the connection details for the specified MCP server and displays them in a structured format that you can import into your MCP client.

```shell
blackbird mcp export [--name <name>] [--path <path>] [--style <style>]
```

### Optional Flags

`-n`, `--name=STRING`

The name of one or more MCP servers for which you want to create connection details.

`-p`, `--path=STRING`

The path to save the MCP configuration file.

`-s`, `--style=STRING`

The style of the configuration file you want to generate. Supported values include `vscode`, `cursor`, and `claude`. If not specified, defaults to `vscode`.

### Examples

The following example exports connection details for a single MCP server.

```shell
blackbird mcp export --name my-mcp
```

The following example exports connection details for multiple MCP servers, including `my-mcp1` and `my-mcp2`.

```shell
blackbird mcp export --name my-mcp1 --name my-mcp2
```

The following example exports the connection details with a custom style and saves it to a specified path.

```shell
blackbird mcp export --name my-mcp --style cursor --path ./config.json
```

## blackbird mcp list

### Description

Lists all MCP deployments.

```shell
blackbird mcp list
```

### Optional Flags

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`. If not specified, defaults to `table`.

### Examples

The following example lists all MCP servers.

```shell
blackbird mcp list
```

The following example lists all MCP servers using JSON format.

```shell
blackbird mcp list --output json
```

## blackbird mcp run

### Description

Runs a new MCP server from the catalog. This command deploys a new MCP server with specified parameters and configurations.

```shell
blackbird mcp run <name> [--image <image>] [--secure=<true|false>] [--wait=<true|false>] [--param <key=value>]...
```

### Required Arguments

`name`

The name of the MCP server you want to run.

### Optional Flags

`-i`, `--image=STRING`

The name of the MCP image you want to create.

`-p`, `--=STRING`

Key=value deployment variable parameters. Can be specified multiple times.

`-s`, `--secure`

Enables secure mode for the MCP server using an API key header. If not specified, defaults to `true`.

`-w`, `--wait`

Waits for the operation to complete. If not specified, defaults to `true`.

### Examples

The following example runs a new MCP server with the default settings.

```shell
blackbird mcp run my-mcp
```

The following example runs a new MCP server with custom parameters.

```shell
blackbird mcp run my-mcp
```

The following example runs a new MCP server with a custom image.

```shell
blackbird mcp run my-mcp --image custom-mcp-image
```

## blackbird mcp update

### Description

Updates an existing MCP deployment in the hosted environment.

```shell
blackbird mcp update --dockerfile=DOCKERFILE --context=STRING <name>
```

### Required Arguments

`name`

The name of the MCP server you want to update.

### Required Flags

`-d`, `--dockerfile=DOCKERFILE`

The path to a Dockerfile.

`-c`, `--context=STRING`

The path to the source code directory you want to include in the image.

### Optional Flags

`-e`, `--envfile=ENVFILE`

The path to as `.env` file containing KEY=VALUE pairs.

`-p`, `--port=PORT`

The port on which the container is listening for requests. If not specified, defaults to port 80.

`-t`, `--protocol=STRING`

The protocol you want to use for the deployment. Supported values include `HTTP` and `TCP`. The default is `HTTP`.

`-r`, `--registry=STRING`

The registry URL where deployment images are pushed.

`--apikey-header=STRING`

The name of an API key header you want to enable for this deployment.

### Examples

The following example updates an MCP server with new code.

```shell
blackbird mcp update my-mcp -d Dockerfile -c .
```

The following example updates an MCP server with new environment variables.

```shell
blackbird mcp update my-mcp -d Dockerfile -c . -e .env
```

The following example updates an MCP server with a new port and protocol.

```shell
blackbird mcp update my-mcp -d Dockerfile -c . -p 8080 -t HTTP
```

## Help

Display all available MCP subcommands and flags.

```shell
blackbird mcp --help
```

## End-to-End usage example

This example demonstrates a complete workflow for using MCP servers to integrate with external services like GitHub and Slack.

1.  Discover which MCP servers are available in the catalog.

    ```shell
    # List all available MCP servers
    blackbird mcp catalog

    # Output might look like:
    # NAME                DESCRIPTION
    # github             GitHub API integration server
    # slack              Slack API integration server
    ```
2.  Deploy servers for GitHub and Slack with their specific configurations.

    > **Note:** By default, your MCP server is secured using an API key header. If you don't want to secure your server using an API key header, use the `--secure=false` flag.

    ```shell
    # Deploy GitHub integration server
    blackbird mcp run github \
      -- GITHUB_TOKEN=your_token 

    # Deploy Slack integration server
    blackbird mcp run slack \
      -- SLACK_BOT_TOKEN=your_token \
      -- SLACK_CHANNEL=general 

    # Wait for the deployments to complete...
    # Deployments successful! Your MCP servers are running.
    ```
3.  Export the connection details for each service.

    ```shell
    # Export connection details for all services
    blackbird mcp export --name github --name slack --style vscode --path ./mcp-config.json

    # The configuration file will contain:
    # - Server URLs for each service
    # - API Keys and tokens
    # - Database connection strings
    # - Service-specific parameters
    ```
4.  (Optional) Update the configurations.

    ```shell
    # Update GitHub server with new organization
    blackbird mcp update github \
      -d Dockerfile \
      -c . \
      -e .env \
      -- GITHUB_ORG=new_org

    # Update the Slack server with a new channel.
    blackbird mcp update slack \
      -d Dockerfile \
      -c . \
      -e .env \
      -- SLACK_CHANNEL=updates

    ```
5.  Monitor the status of your MCP servers at any time.

    ```shell
    # List all running MCP servers
    blackbird mcp list

    # Output might look like:
    # NAME         STATUS    
    # github       Ready   
    # slack        Ready   
    ```
6.  When you're ready, delete the servers.

    ```shell
    # Delete all MCP servers
    blackbird mcp delete github
    blackbird mcp delete slack

    # Wait for deletion to complete...
    # MCP servers deleted successfully.
    ```

This completes the full lifecycle of MCP servers for common service integrations.

Consider the following when managing MCP servers:

* Always use secure mode in production environments.
* Keep your API keys and tokens secure.
* Use environment variables for sensitive information.
* Clean up unused MCP servers to avoid unnecessary costs.
* Export configuration details before making significant changes.
* Consider using different MCP servers for different environments (dev/staging/prod).
