# Configure Reporters

## Overview

_Reporters_ are used by AM Gateway and API instances to report many types of events:

* Administration metrics: administrative tasks (CRUD on resources)
* Authentication / Authorization metrics: (sign-in activity, sign-up activity)

A default reporter is created using a MongoDB or JDBC implementation according to the backend configured in the `gravitee.yml` file.

From AM version 3.6, you can create additional reporters.

## File reporter

This implementation is a file-based reporter for writing events to a dedicated file. You can use it for ingesting events into a third party system.

### aConfiguration

File reporters are configurable in the `gravitee.yml` file `reporter` section with the following properties:

| property  | type   | required | description                                                                                             |
| --------- | ------ | -------- | ------------------------------------------------------------------------------------------------------- |
| directory | string | N        | Path to the file creation directory. The directory must exist (default: `${gravitee.home}/audit-logs/`) |
| output    | string | N        | Format used to export events. Possible values: JSON, MESSAGE\_PACK, ELASTICSEARCH, CSV (default: JSON)  |

```yaml
reporters:
  file:
    #directory:  # directory where the files are created (this directory must exist): default value = ${gravitee.home}/audit-logs/
    #output: JSON # JSON, ELASTICSEARCH, MESSAGE_PACK, CSV
```

Audit logs will be created in a directory tree that represents the resource hierarchy from the organization to the domain. For example, audit logs for domain `my-domain` in environment `dev` and organization `my-company` will be created in the following directory tree: `${reporters.file.directory}/my-company/dev/my-domain/audit-2021_02_11.json`

{% hint style="warning" %}
There is currently no retention period for the audit logs, so you need to create a separate process to remove old logs.
{% endhint %}

For details on how to create a file reporter for a domain, see [Audit log file.](../../guides/audit-trail/storage/file.md)
