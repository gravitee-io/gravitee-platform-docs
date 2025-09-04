---
noIndex: true
---

# General

This reference provides a list of basic commands, arguments, and flags you can use to work with Blackbird.

## blackbird help

Provides a full list of available commands.

## blackbird login

Opens a new browser window for logging in to Blackbird. This command must be run prior to attempting any other commands.

## blackbird version

Shows the current version of Blackbird. View our [release-notes.md](../../release-notes.md "mention") for version details. To upgrade, download the latest binary of the CLI using the command in the [#download-the-cli-and-log-in-optional](../../quick-start/#download-the-cli-and-log-in-optional "mention") section.

## blackbird logout

Logs the current user out of Blackbird.

## blackbird subscription info

Shows detailed subscription information, including the status, current plan, start and end dates, limits, and usage.

## blackbird instance list

Lists the name, type, status, API key headers, URL, and user for deployment, mock, and code instances.

### Optional arguments

`name`

The name of the instance to list. Use the full name of the instance surrounded by double or single quotes.

### Optional flags

`-d`, `--deployments`

Shows only deployed instances.

`-m`, `--mocks`

Shows only mock instances.

`-c`, `--codes`

Shows only code instances.

`--mcp`

Shows only MCP (Model Context Protocol) instances.

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.

### Examples

The following example shows details for all instances.

```shell
blackbird instance list
```

The following example shows details for the instance named "Simple API Mock".

```shell
blackbird instance list “Simple API Mock”
```

The following example shows details for all mock instances.

```shell
blackbird instance list -m
```
