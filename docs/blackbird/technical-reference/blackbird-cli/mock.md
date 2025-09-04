---
noIndex: true
---

# Mock

This reference provides a list of commands, arguments, and flags you can use to work with mock instances in Blackbird.

## blackbird mock create

Creates a new mock using an existing API or a file path to an OpenAPI specification.

```shell
blackbird mock create [name]
```

### Required arguments

`name`

The name of the new mock instance.

### Optional flags

`-n`, `--api-name=STRING`

The slug name of the existing API you want to use to create the mock instance.

`--apikey-header=STRING`

Enables an existing API key header for the mock. After enabling an API key header for a mock, all future requests to the mock must contain the API key header.

`-s, --spec-path=STRING`

The path to the OpenAPI file you want to use to create the mock instance. Use this flag if you're creating a mock instance for an API that you didn't create using Blackbird.

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.

`-w`, `--wait`

Waits for the operation to complete (default true)

### Examples

The following example creates a mock named "simple-api-mock" from an existing API with the slug name "simple-api".

```shell
blackbird mock create simple-api-mock -n simple-api
```

The following example creates a mock named "simple-api-mock" from an OpenAPI specification file.

```shell
blackbird mock create simple-api-mock -s ./simple-api.yaml
```

## blackbird mock list

Lists the name, type, status, API key headers, URL, and user who created the mock for every mock in your organization.

### Optional Flags

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.

## blackbird mock update

Updates an existing mock instance for an API.

```shell
blackbird mock update name
```

### Required arguments

`name`

The name of the mock instance you want to update.

### Optional flags

`-n`, `--api-name=STRING`

The slug name of the existing API you want to use to update the mock instance.

`--apikey-header=STRING`

Enables an existing API key header for the mock. After enabling an API key header for a mock, all future requests to the mock must contain the API key header.

`-s`, `--spec-path=STRING`

The path to an OpenAPI file to update the mock instance with.

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.

`-w`, `--wait`

Waits for the operation to complete (default true)

### Examples

The following example updates an existing mock named "simple-api-mock" using the existing API with the slug name "another-api".

```shell
blackbird mock update simple-api-mock -n another-api
```

## blackbird mock delete

Deletes a mock instance for an API. If the mock instance is associated with an API, a prompt will appear asking if you want to remove all associated APIs.

```shell
blackbird mock delete name
```

### Required arguments

`name`

The name of the mock instance you want to delete.

### Optional Flags

`-f`, `--force`

If present, the `blackbird mock delete` command also deletes the parent API without prompting you for confirmation.

### Examples

The following example deletes the mock named "simple-api-mock".

```shell
blackbird mock delete simple-api-mock
```

The following example deletes the mock named "simple-api-mock" and the API from which the mock was derived.

```shell
blackbird mock delete simple-api-mock -f
```

## blackbird mock config get name

Obtains the configuration of a mock instance.

```shell
blackbird mock config get name
```

### Required arguments

`name`

The name of the mock instance.

### Examples

The following example returns the configuration for the mock instance named "simple-api-mock".

```shell
blackbird mock config get simple-api-mock
```

## blackbird mock config set name

Sets the configuration of a mock instance.

```shell
blackbird mock config set name <config-parameter>
```

### Required arguments

`name`

The name of the mock instance.

`configuration parameters`

The configuration parameters you want to set.

### Examples

The following example enables dynamic data generation for the mock instance named "simple-api-mock".

```shell
blackbird mock config set simple-api-mock dynamic=true
```
