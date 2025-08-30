# API Key

This reference provides a list of commands, arguments, and flags you can use to work with API keys in Blackbird.

## blackbird apikey create

Creates an API key header to secure an instance.

```shell
blackbird apikey create <header name> <value>
```

> **Important:** Save the name of your API key so you can access it in the future.

### Required arguments

`header name`

The name of the API key header.

`value`

The value of the API key. This value can be any string.

### Examples

The following example creates an API key with the name "simple-key" and value "thisismyvalue".

```shell
blackbird apikey create simple-key thisismyvalue
```

## blackbird apikey delete

Deletes an existing API key header.

```shell
blackbird apikey delete <header-name>
```

### Required arguments

`header name`

The name of the API key header you want to delete.

### Examples

The following example deletes the API key named "simple-key".

```shell
blackbird apikey delete simple-key
```

## blackbird apikey enable

Enables an API key header for a mock or deployment. Requests can't access the mock or deployment instance without the API key header in the request.

```shell
blackbird apikey enable <header-key> <instance-name>
```

### Required arguments

`header key`

The name of the existing API key header.

`instance name`

The name of the mock or deployment instance for which you want to enable the API key header. Use the full name of the instance surrounded by double or single quotes.

### Examples

The following example enables the API key "simple-key" for the instance "Simple API Mock".

```shell
blackbird apikey enable simple-key “Simple API Mock”
```

## blackbird apikey disable

Disables an API key header for a mock or deployment. When the API key is disabled for a mock or deployment, any request can access the mock or deployment instance.

```shell
blackbird apikey disable <header-key> <instance-name>
```

### Required arguments

`header key`

The name of the existing API key header.

`instance name`

The name of the mock or deployment instance for which you want to disable the API key header. Use the full name of the instance surrounded by double or single quotes.

### Examples

The following example disables the API key "simple-key" for the instance "Simple API Mock".

```shell
blackbird apikey disable simple-key “Simple API Mock”
```

## blackbird apikey list

Lists all API key headers, mock or deployment instances for which each header is enabled, and when each header was created.

### Optional flags

`-a`, `--active`

Lists API key headers that have been enabled for one or more instances.

`-i`, `--inactive`

Lists API key headers that haven't been enabled for one or more instances.

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.
