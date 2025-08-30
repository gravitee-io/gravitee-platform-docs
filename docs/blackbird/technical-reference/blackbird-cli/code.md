# Code

## Code

This reference provides a list of commands, arguments, and flags you can use to work with code in Blackbird.

### blackbird code generate

Locally generates code in Go for an API. You can utilize an existing template from Blackbird, use your own, or use none. Using a template allows you to customize the generated code by adding variables, configuring renames, and choosing which modules to enable. An existing API in the Blackbird API catalog is required to generate code.

The command consists of 2 subcommands: `server` and `client`.

```shell
blackbird code generate server <template> -o <output>
```

```shell
blackbird code generate client <template> -o <output>
```

#### Required flags

`-o`, `--output=STRING`

The destination directory where you want to store the generated project. Folders will be created if they don't exist.

#### Optional flags

`--gen-config-path=STRING`

Path to the generator configuration file with template values.

`--gen-config-values=stringToString`

Key-value pairs to override the generator configuration values. The values here take precedence over the configuration file.

#### Conditional flags

`-s`, `--spec-path=STRING`

The path to an OpenAPI spec file to use with the code generator.

`-n`, `--api-name=STRING`

The slug name of the existing API you want to use with the code generator.

#### Configuration options

Most of available templates offer a set of configuration options that you can use to customize the generated code. You can find the list of available templates and their configuration options in the [OpenAPI Generators List](https://openapi-generator.tech/docs/generators). `--gen-config-path` and `--gen-config-values` flags allow you to provide the configuration values to the generator. You can use the configuration file to provide a reasonable base configuration for consumption by multiple projects. `--gen-config-values` flag comes useful if it is desired to override a value on a per-project basis with values unique to a given project, such as name, version, etc.

For instance, `typescript-fetch` client target accepts the following [options](https://openapi-generator.tech/docs/generators/typescript-fetch/)

```yaml
"importFileExtension": ".ts"
"legacyDiscriminatorBehavior": false
"license": "MIT"
```

```shell
blackbird code generate client typescript-fetch -s simple-api.yaml -o ./client --gen-config-path blackbird-typescript-fetch-config.yaml --gen-config-values npmName=my-api-client --gen-config-values npmVersion=1.1.2
```

#### Examples

The following example generates a code project located at `~/Documents/blackbird/simple-api-test` using an OpenAPI specification file located at `simple-api.yaml` with the existing Go template.

```shell
blackbird code generate server go-server -s simple-api.yaml -o ~/Documents/blackbird/simple-api-test
```

This example generates a code project located at `~/Documents/blackbird/simple-api-test/client`.

```shell
blackbird code generate client typescript-fetch -s simple-api.yaml -o ~/Documents/blackbird/simple-api-test/client
```

### blackbird code run

Containerizes code and runs it locally. This spins up a container with your code, and you can utilize the same endpoint from our mock server to reach your code.

```shell
blackbird code run <name> --context=STRING
```

#### Required arguments

`name`

The name of the application you want to run. This must be all lowercase.

#### Required flags

`-c`, `--context=STRING`

The path to the source code directory you want to include in the image.

#### Optional flags

`-d`, `--dockerfile=STRING`

The name of your Dockerfile in the current directory.

`-e`, `--envfile=ENVFILE`

The path to a .env file that contains lines of KEY=VALUE.

`--expose=EXPOSE`

The port to expose from the container network. The format should be ADDRESS:LOCAL-PORT:PORT or LOCAL-PORT:PORT.

`-p`, `--port="80"`

The service port or port name.

`-l`, `--local-port=8080`

The local port to forward to.

`--apikey-header=STRING`

The name of one of your API key headers to enable for this code instance.

#### Examples

The following examples builds and runs a local container with a remote server named "simple-api" from the Dockerfile located in the current directory, accessible via port 80.

```shell
blackbird code run simple-api -d Dockerfile -c . -l 80
```

### blackbird code debug

Uses the same functionality as `blackbird code run`, but also starts a debugger and waits for a debugger frontend to attach.

```shell
blackbird code debug <name> --context=STRING
```

#### Arguments

| Arguments | Required? | Description                                                              |
| --------- | --------- | ------------------------------------------------------------------------ |
| Name      | No        | The name of the application you want to run. This must be all lowercase. |

#### Required flags

`-c`, `--context=STRING`

The path to the source code directory you want to include in the image.

#### Optional flags

`-d`, `--dockerfile=STRING`

The name of your Dockerfile in the current directory.

`-e`, `--envfile=ENVFILE`

The path to a .env file that contains lines of KEY=VALUE.

`--expose=EXPOSE`

The port to expose from the container network. The format should be ADDRESS:LOCAL-PORT:PORT or LOCAL-PORT:PORT.

`-p`, `--port="80"`

The service port or port name.

`-l`, `--local-port=8080`

The local port to forward to.

`--apikey-header=STRING`

The name of one of your API key headers to enable for this code instance.

`--target="debug:2345"`

Builds the target stage and port to attach to the debugger. The default can be overridden using ':'.

#### Examples

The following example builds and runs a local container with a remote server and attached debugger front-end named "simple-api" from the Dockerfile located in the current directory, accessible via port 80.

```shell
blackbird code debug simple-api -d Dockerfile -c . -l 80
```

## blackbird code list

Lists the name, type, status, API key headers, URL, and user who created the instance for any active instances of code run using the `blackbird code run` or `blackbird code debug` command in your organization.

#### Optional Flags

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.
