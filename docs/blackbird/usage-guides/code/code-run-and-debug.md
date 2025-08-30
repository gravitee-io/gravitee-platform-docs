# Code Run and Debug

Running and debugging your API specification or mock instance allows you to test the behavior of your API, analyze request and response data, and troubleshoot issues throughout the development process.

> **Note:** You must install Docker to use code run and code debug commands with Blackbird. For more information, see [Get Docker](https://docs.docker.com/get-started/get-docker/).

## Building and running a local container with a remote server

To start debugging an API or mock, pass the instance name as well as the path to the dockerfile and context.

```shell
blackbird code run --dockerfile=<DOCKERFILE> --context=STRING --local-port=INT <name>
```

## Building and debugging a local container with a remote server

Use the following command, which is similar to the `run` command, but it attaches a debugger to the container:

```shell
blackbird code debug --dockerfile=<DOCKERFILE> --context=STRING --local-port=INT <name>
```

## Securing a code instance

By default, the remote code instance server endpoints are available publicly. To secure these endpoints, you can use API keys as shown in [secure-instances-on-blackbird.md](../../technical-reference/secure-instances-on-blackbird.md "mention"). You can also create and set an API key on creation with the `--apikey-header` flag. The following templates show the valid ways to enable an API key for code instance servers.

```shell
blackbird code run --dockerfile=<DOCKERFILE> --context=STRING --local-port=INT --apikey-header=<HeaderKey> <name>
```

```shell
blackbird code debug --dockerfile=<DOCKERFILE> --context=STRING --local-port=INT --apikey-header=<HeaderKey> <name>
```

```shell
blackbird apikey enable <HeaderKey> <codeInstance>
```
