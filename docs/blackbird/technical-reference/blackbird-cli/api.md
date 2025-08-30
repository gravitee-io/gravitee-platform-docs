# API

This reference provides a list of commands, arguments, and flags you can use to work with APIs in Blackbird.

## blackbird api create

Creates an API within Blackbird.

```shell
blackbird api create <name> –-spec-path=STRING
```

### Required arguments

`name`

The name of the API you're creating.

### Required flags

`-s`, `–-spec-path=STRING`

The path to an OpenAPI file.

### Examples

The following example creates an API named Simple API using the OpenAPI file located at ./simple-api.yaml.

```shell
blackbird api create "Simple API" --spec-path=./simple-api.yaml
```

## blackbird api list

Lists the name, slug name, spec file, and user who created the API for each API matching the given API slug name. If no name is given, all APIs will be returned.

```shell
blackbird api list <slug-name>
```

### Optional arguments

`slug name`

The slug name of the API for which you want to see details.

### Optional flags

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.

### Examples

The following example returns details for all APIs.

```shell
blackbird api list
```

The following example returns details for an API named "simple-api" using YAML as the output format.

```shell
blackbird api list simple-api -o yaml
```

## blackbird api update

Updates an existing API in Blackbird.

```shell
blackbird api update <name> --spec-path=STRING
```

### Required arguments

`name`

The name of the API you want to update.

### Required flags

`-s`, `–-spec-path=STRING`

The path to an OpenAPI file.

### Examples

The following example updates an existing API named "Simple API" using the OpenAPI file located at ./simple-api-updated.yaml.

```shell
blackbird api update "Simple API" --spec-path=./simple-api-updated.yaml
```

## blackbird api delete

Deletes an API. If the API is associated with any mocks or deployments, a prompt will display asking if you want to remove all associated instances.

```shell
blackbird api delete <slug-name>
```

### Required arguments

`slug name`

The slug name of the API you want to delete.

### Optional Flags

`-f`, `--force`

If present, the `blackbird api delete` command also deletes all associated mock instances without prompting you for confirmation.

### Examples

The following example deletes the API named "simple-api".

```shell
blackbird api delete simple-api
```

The following example deletes the API named "simple-api" and all associated mock instances.

```shell
blackbird api delete simple-api -f
```
