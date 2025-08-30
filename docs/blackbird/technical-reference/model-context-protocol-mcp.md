# Model Context Protocol (MCP)

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is a framework that delivers contextual data to AI clients in real time. It acts as a bridge that provides AI models with the information they need to improve accuracy and relevance. For example, if you’re developing an AI client that conducts code reviews, it may require specific context from your GitHub repository. To provide this context, you can run the GitHub MCP server and have your AI client query the endpoint.

You can run MCP servers locally or as a hosted service. Local servers use STDIO for communication and are limited to a single user, which means they can't be shared. Hosted servers use server-sent events (SSE), so anyone with the server's URL can access them.

Using Blackbird, you can deploy an MCP server in a hosted, non-production environment for testing purposes. This can reduce local resource usage, streamline your workflow, allow for collaboration, and enhance security. This is particularly useful for smaller teams or individuals working in limited environments where running multiple local services can cause performance issues. For larger teams, hosting an MCP server improves security by centralizing key and token management, which is important when working with sensitive data or maintaining security compliance with requirements such as SOC 2.

Use the following procedures and resources in this guide to learn how to host an MCP server in Blackbird and share it with your team.

* [Hosting a third-party MCP server in Blackbird using the CLI](model-context-protocol-mcp.md#hosting-a-third-party-mcp-server-in-blackbird-using-the-cli)
* [Hosting a third-party MCP server in Blackbird using Visual Studio Code](model-context-protocol-mcp.md#hosting-a-third-party-mcp-server-in-blackbird-using-visual-studio-code)
* [Example - Hosting an MCP server in Blackbird](model-context-protocol-mcp.md#example---hosting-an-mcp-server-in-blackbird)

## Hosting a third-party MCP server in Blackbird using the CLI

You can host a third-party MCP server in Blackbird using the Blackbird CLI. The MCP catalog offers several options to fit different use cases. In this procedure, you'll browse the catalog, select a server, deploy it in your environment, and export the connection details to use in a compatible client (e.g., VS Code or Cursor).

> **Note:** The following procedure provides key arguments and flags related to the CLI commands, but you can find more information and examples in the [Blackbird CLI](https://www.getambassador.io/docs/blackbird/latest/reference/cli-commands).

### Prerequisites

* You installed the Blackbird CLI. For more information, see [#getting-started-with-the-blackbird-cli](blackbird-cli/#getting-started-with-the-blackbird-cli "mention").
* You installed Docker and it's actively running. For more information, see [Get Docker](https://docs.docker.com/get-started/get-docker/).

**To host an MCP server using the CLI:**

1.  View the MCP server catalog to determine which server you want to deploy. This procedure uses the GitHub MCP server.

    ```shell
    blackbird mcp catalog
    ```

    The catalog includes the server names, tags, descriptions, and required parameters. Note the parameters for the server you want to deploy (e.g., GITHUB\_PERSONAL\_ACCESS\_TOKEN for GitHub). You’ll input these parameters in the next step.
2.  Run an MCP server deployment.

    ```shell
    blackbird mcp run <name> [--image <image>] [--param <key=value>]... [flags]
    ```

    Key arguments and flags include:

    * `<name>` – The name you want to use for your server.
    * `--image` – The name of the third-party MCP server you want to use (e.g., github).
    *   `--param` – The required parameters from the previous step (e.g., GITHUB\_PERSONAL\_ACCESS\_TOKEN=your-token).

        > **Note:** By default, your MCP server is secured using an API key header. If you don't want to secure your server using an API key header, use the `--secure=false` flag. When the deployment completes, a URL displays.
3.  View your MCP server to ensure it deployed successfully. When the deployment is successful, the status is **Ready**.

    ```shell
    blackbird mcp list
    ```
4.  Export connection details in a structured format that you can add to your MCP client.

    ```shell
    blackbird mcp export [--name <name>] [--path <path>] [--style <style>]
    ```

    Key arguments and flags include:

    * `--name` – The name of one or more MCP servers for which you want to export details (e.g., github).
    * `--path` – The location where you want to save the exported file (e.g., ./config.json).
    * `--style` – The style of the configuration file you want to export (e.g, vscode).

### Next steps

Now that you have the MCP server running in Blackbird, you can query your AI chatbot using context specific to the server you deployed.

## Hosting a third-party MCP server in Blackbird using Visual Studio Code

You can use the Visual Studio Code (VS Code) integration to host a third-party MCP server in Blackbird. Our MCP catalog offers several options to fit different use cases. In this procedure, you'll browse the catalog, select a server, and deploy it in your environment.

### Prerequisites

* You installed Docker and it's actively running. For more information, see [Get Docker](https://docs.docker.com/get-started/get-docker/).
* You installed the Visual Studio Code extension. For more information, see [visual-studio-code.md](integrations/visual-studio-code.md "mention").

**To host an MCP server using VS Code:**

1. Make sure the [Hosted Dev Environment with Blackbird](https://marketplace.visualstudio.com/items?itemName=Ambassador.blackbird-plugin) extension is running in VS Code.
2. In the side bar under Blackbird, expand **MCP Catalog** to view available servers.
3. Hover over the server you want to deploy and select the **Run** icon to launch it.
4. The input box prompts you for each required parameter. Provide the requested parameters.
5. When the MCP server deployment completes, expand **MCP Deployments** in the side bar to view your deployed server and its endpoint.
6. In the side bar, hover over the deployed **MCP server** and choose the **Export MCP Connection** icon. The configuration details are added to your workspace (e.g., `.vscode/mcp.json`).

### Next steps

Now that you have the MCP server running in Blackbird, you can query your AI chatbot using context specific to the server you deployed.

## Example - Hosting an MCP server in Blackbird

The steps in the following example workflow use the GitHub MCP client and Cursor integrated development environment (IDE). However, you can adapt them to use other MCP servers or MCP-compatible IDEs or clients as needed.

### Prerequisites

Before following the example workflow, ensure you meet the following requirements:

* You installed the Blackbird CLI. For more information, see [#getting-started-with-the-blackbird-cli](blackbird-cli/#getting-started-with-the-blackbird-cli "mention").
* You installed Docker and it's actively running. For more information, see [Get Docker](https://docs.docker.com/get-started/get-docker/).
* You installed the Cursor MCP client. For more information, see Download [Cursor](https://www.cursor.com/en/downloads).

**To host a GitHub MCP server:**

1.  Create a Dockerfile with the following content:

    ```dockerfile
     FROM node:alpine
     
     WORKDIR /app
     
     # Required by SuperGateway to run the server
     ARG PORT
     ENV PORT=$PORT
     
     ARG BASE_URL
     ENV BASE_URL=$BASE_URL
     
     USER 1000:1000
     
     EXPOSE ${PORT}
     
     ENTRYPOINT npx -y supergateway --stdio "npx -y @modelcontextprotocol/server-github" --port "$PORT" --baseUrl "$BASE_URL"
    ```

    > **Note:** Docker containers run as the `root` user by default, which can introduce security vulnerabilities and cause your deployment to fail. To avoid this, configure your Dockerfile to run as a non-`root` user.
2.  Create an `.env` file alongside the Dockerfile with the following entries. Replace `<BLACKBIRD_ENV_HOST>` with the unique hostname of your Blackbird environment. To find this, you can either check the URL of any existing mock or deployment instance in Blackbird or run the following command from the CLI: `blackbird instance list`

    ```ini
     PORT=80
     BASE_URL=https://<BLACKBIRD_ENV_HOST>/github-mcp
    ```

    > **Important:** You can adapt this Dockerfile to run any prebuilt MCP server. Currently, the GitHub MCP server uses STDIO, which doesn't support remote HTTP connections. This example uses SuperGateway to transform MCP servers from STDIO to SSE.
3.  In the same directory as your Dockerfile and `.env` file, run the following command using the Blackbird CLI:

    ```shell
    blackbird deployment create github-mcp -d Dockerfile -c . -e .env
    ```

    After the deployment completes, you'll see a Blackbird URL for your hosted GitHub MCP server.
4.  Locate or create the MCP server configuration file in Cursor, which is typically called `mcp.json`. Add your hosted GitHub MCP server URL from Blackbird to the config and add `/sse` to the URL:

    ```json
     {
       "mcpServers": {
         "githubMcp": {
           "url": "https://<BLACKBIRD_ENV_HOST>/github-mcp/sse"
         }
       }
     }
    ```
5. In Cursor, navigate to **Settings>MCP** to verify that the MCP server exists and enable it. Your chat conversations with the Cursor LLM will now use the remote GitHub MCP server.
