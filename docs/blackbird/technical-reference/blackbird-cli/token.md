---
noIndex: true
---

# Token

This reference provides a list of commands, arguments, and flags you can use to work with tokens in Blackbird.

## blackbird token create

Creates a headless token to use in Blackbird. If the user belongs to multiple organizations, the token is created in the active organization.

```shell
blackbird token create <name>
```

### Required arguments

`name`

The name you want to use for the token you're creating.

### Examples

The following example creates a token named "ci-token".

```shell
blackbird token create ci-token
```

## blackbird token list

Lists the name of the token matching the provided token name, if it exists. If a name isn't provided, all tokens display.

```shell
blackbird token list <name>
```

### Optional arguments

`token name`

The name of the token, if it exists.

### Optional Flags

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.

### Examples

The following example returns a list of all token names.

```shell
blackbird token list
```

This example returns the name of the token named "ci-token", if it exists.

```shell
blackbird token list ci-token
```

## blackbird token delete

Deletes a token.

```shell
blackbird token delete <name>
```

## Required arguments

`token name`

The name of the token you want to delete.

## Examples

The following example deletes the token named "ci-token".

```shell
blackbird token delete ci-token
```
