---
description: Overview of Organization.
noIndex: true
---

# Organization

This reference provides a list of commands, arguments, and flags you can use to work with organizations in Blackbird.

## blackbird organization list

Lists the organizations you belong to.

### Optional Flags

`-o`, `--output=STRING`

Renders the output from the command in the requested format. Supported values include `json`, `yaml`, and `table`.

## blackbird organization users

Lists all users associated with your current organization.

## blackbird organization set

Sets an organization as your active organization. All commands will target this organization.

```shell
blackbird organization set <name>
```

### Required flags

`-n`, `--name`

The name of the organization you want to switch to.
