---
description: Getting started with Code Quickstart.
noIndex: true
---

# Code Quickstart

Using this quickstart guide, you can quickly:

* **Generate code:** Generating client or server code from an API specification allows you to interact with your API more efficiently during development and testing. By automating the creation of request and response handling, you can test endpoints without manually coding requests, saving time and reducing errors. If errors occur during code generation, you can refine the API specification to ensure it's complete and accurate.
* **Run and debug your code:** Running and debugging your code allows you to test the behavior of your API, analyze request and response data, and troubleshoot issues throughout the development process.
* **Connect to a Kubernetes cluster:** Connecting to a cluster allows you to monitor, configure, update, or troubleshoot it without changing how it functions. With a direct connection using Blackbird (powered by Telepresence), you can check logs, adjust settings, and manage resources without affecting the normal traffic flow.

## Prerequisites

Before you get started:

* Download the CLI. For more information, see [#download-the-cli-and-log-in-optional](./#download-the-cli-and-log-in-optional "mention").
* Add or create an API. For more information, see [#add-an-api](./#add-an-api "mention").
* Open your preferred IDE, such as Visual Studio Code.
* Install Docker. For more information, see [Get Docker](https://docs.docker.com/get-started/get-docker/).

## Generating code

After you have an API in the Blackbird catalog, you can generate code for the simple API project. Blackbird uses [OpenAPI Generator](https://openapi-generator.tech/) to generate client or server code for the API description. For the purpose of this quickstart guide, you can use the `go-server` server template. However, you can also reference any of the available client or server generators. For more information, see the [OpenAPI Generators List](https://openapi-generator.tech/docs/generators).

**To generate code:**

1.  Run the code generate command.

    ```shell
    blackbird code generate server go-server --spec-path ./simpleapi.yaml --output go-simple-api
    ```
2.  The CLI prompts you for variables. Provide the package version and package name.

    ```shell
    Enter the package version [1.0.0]:
    Enter the package name [simple_api]:
    ```

    When the simple API project is generated, it creates a new directory with all the necessary modules and Go files for the projects, including the Dockerfile you'll use to run and debug the code.

## Running and testing the code locally

Using the new simple API project, run the code locally and curl the `say-hello` endpoint.

**To run and test the code locally:**

1.  Run the following command.

    ```shell
    cd go-simple-api
    ```
2.  In `go.mod`, replace `module //` with `module github.com/your-username/simple-api` or another module name of your choice. Then, in `main.go`, replace `simple_api "///go"` on line 17 with `github.com/your-username/simple-api/go`.

    ```shell
    go mod tidy
    go run main.go

    curl localhost:80/say-hello
    ```

    Although you curled the endpoint, you'll need to containerize the code to implement the `say-hello` endpoint.

## Containerizing the code

After the project runs locally, you can fix the unimplemented `say-hello` endpoint by using a combination of the `code run` and `code debug` commands. You'll containerize the code, run it locally, and then intercept traffic to the API in a hosted environment.

**To containerize the code:**

1.  Run the `code run` command.

    ```shell
    blackbird code run simple-api --dockerfile Dockerfile --context . --local-port 80
    ```

    A Docker container spins up, so you can test the API code beyond localhost.
2.  Run the following commands to verify the publicly available URL and curl the endpoint. If you followed the [mock-quickstart.md](mock-quickstart.md "mention") guide, you'll notice that the mocked hostname has been reused for the code instance.

    ```shell
    blackbird instance list simple-api
    ```

    ```shell
    curl https://<host-name>/simple-api/say-hello
    ```

## Debugging the code

After you containerize the code, you can debug the `say-hello` endpoint using the `code debug` command.

**To debug the code:**

1.  Edit the `GetHello` method in `go/api_default_service.go` to return the proper message.

    ```go
    // Get a hello message
    func (s *DefaultAPIService) GetHello(ctx context.Context) (ImplResponse, error) {
       message := "Hello World!"
       return Response(200, GetHello200Response{message}), nil
    }
    ```
2.  Set up debugging in your IDE. If you're using Visual Studio Code, use the following `launch.json` file in the `.vscode` directory.

    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Connect to server",
                "type": "go",
                "request": "attach",
                "mode": "remote",
                "port": 2345,
                "host": "127.0.0.1"
            }
        ]
    }
    ```
3.  In the `Dockerfile`, we'll add a debug stage to build the code with debugging flags and run the `dlv` debugger. You can find the complete Dockerfile below.

    ```dockerfile
    FROM golang:1.23 AS base

    RUN go install github.com/go-delve/delve/cmd/dlv@latest

    WORKDIR /go/src
    COPY go ./go
    COPY main.go .
    COPY go.sum .
    COPY go.mod .

    ENV CGO_ENABLED=0

    FROM base AS debug

    RUN go build -gcflags="all=-N -l" -o simple_api .
    ENV DEBUG_PORT=2345
    EXPOSE $DEBUG_PORT
    ENTRYPOINT /go/bin/dlv --listen=:$DEBUG_PORT --headless=true --api-version=2 --accept-multiclient exec simple_api

    FROM base AS run

    RUN go build -o simple_api .
    EXPOSE 80/tcp
    USER 1001
    ENTRYPOINT ["./simple_api"]
    ```
4.  Run the debug command.

    ```shell
    blackbird code debug simple-api --dockerfile Dockerfile --context . --local-port 80 --target="debug:2345"
    ```

    The API server starts listening and the `go-simple-api` server starts up.
5. Attach a debugger. If you're using Visual Studio Code, you can find the [VSCode debugger](https://code.visualstudio.com/docs/editor/debugging) under the **Run** tab.
6. Set a breakpoint in the code (for example, in the edited `GetHello` method).
7.  Curl the `say-hello` endpoint to see that the breakpoint is hit.

    ```shell
    curl https://<host-name>/simple-api/say-hello
    ```

Use the `code run` and `code debug` commands to develop using a hybrid model. Your teams can collaborate on code that runs on a user's machine using the public URL. You can also use the hybrid model in CI pipelines where a virtual machine (VM) checks out the code and starts a code run session.

## Connecting to a cluster

When managing a Kubernetes cluster, you might want to monitor, configure, update, or troubleshoot it without changing how it functions. A direct connection allows you to check logs, adjust settings, and manage resources without affecting the normal traffic flow.

> **Note:** For detailed information about cluster commands, see _Clusters_ in the Blackbird CLI Reference.

**To connect to a cluster:**

1.  Install the Helm package manager.

    ```shell
    blackbird cluster helm install
    ```
2.  Connect to your cluster.

    ```shell
    blackbird cluster connect
    ```
3. Verify that you can reach the cluster's API or another internal service. For example, run a `curl` command to a service endpoint. You should see the expected response or a 401 response. The 401 response is expected if you are't providing credentials. If you can reach the endpoint, it was successful.
4.  When you're ready, end the connection and all daemons.

    ```shell
    blackbird cluster quit
    ```

After you set up your connection, you can create intercepts to route traffic for your cluster's service to your local machine.
