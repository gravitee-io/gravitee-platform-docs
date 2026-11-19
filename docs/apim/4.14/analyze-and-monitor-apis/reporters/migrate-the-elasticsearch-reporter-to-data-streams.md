---
description: Migrate the Elasticsearch reporter in API Management 4.14 from daily or ILM-managed indices to data streams. Follow the steps to switch or to revert.
---

# Migrate the Elasticsearch Reporter to Data Streams

## Overview

This guide moves an installation whose Elasticsearch reporter writes in the `daily` or `ilm` index mode to the `data_stream` index mode. For a new installation, see [Write analytics to data streams](elasticsearch-reporter.md#write-analytics-to-data-streams).

{% hint style="warning" %}
APIM doesn't move existing analytics to the data streams. In data stream mode, the Management API reads only the data streams, so the analytics written before the switch no longer appear in the Management Console. The previous indices keep their data under their own names until you delete them, or until their lifecycle policy deletes them.
{% endhint %}

## Prerequisites

* Every Gateway and the Management API run APIM 4.14 or later.
* The cluster runs Elasticsearch 7.9 or later, or OpenSearch. To set a retention, you need Elasticsearch 8.14 or later.
* The lifecycle of the data streams is ready before the switch. For more information, see [Set the lifecycle of the data streams](elasticsearch-reporter.md#set-the-lifecycle-of-the-data-streams).
  * An existing ILM policy can be reused on the data streams. A rollover action works without a rollover alias.
  * A type takes either a lifecycle policy or a retention. The reporter stops at startup when a type has both. Check the policies that your configuration already sets before you add a retention. With Helm, `es.lifecycle.enabled: true` sets a policy for four keys by default. For more information, see [Configure data streams with Helm](elasticsearch-reporter.md#configure-data-streams-with-helm).
  * On OpenSearch, the ISM policies with an `ism_template` exist before the data streams are created. For more information, see [Data streams on OpenSearch](elasticsearch-reporter.md#data-streams-on-opensearch).

## Switch every writer at once

Switch every Gateway that writes to the cluster with the same `index` prefix, and the Management API, at the same time. Never run the `data_stream` mode and another index mode on the same cluster with the same `index` prefix.

The index templates of the `daily` and `ilm` modes and the data stream templates have the same names, `<index>-<type>`, for example `gravitee-request`, and each reporter registers its own at startup. The following cases apply:

* Before a data stream exists, the templates replace each other. A Gateway still in the `daily` mode when the data stream templates replace its own creates its next dated index, for example after midnight UTC, with no Gravitee mapping.
* Once a data stream exists, Elasticsearch refuses a template with the same name that doesn't declare a data stream. A Gateway that restarts in the `daily` or `ilm` mode afterward keeps its reporter inactive. The data streams aren't affected.

## Migrate from the `daily` index mode

1. Set `index_mode` to `data_stream` on every Gateway and on the Management API, and then restart them. With Helm, set `es.index_mode: data_stream`.
2. When you no longer need their data, delete the dated indices, named `<index>-<type>-YYYY.MM.DD`. They don't conflict with the data streams.

## Migrate from the `ilm` index mode

The `ilm` index mode leaves a rollover alias named like each data stream, for example `gravitee-request` on `gravitee-request-000001`. Elasticsearch writes the documents to the indices of the alias instead of creating the data stream, so the reporter stops at startup while such an alias exists. Its error names the aliases.

{% hint style="warning" %}
The check needs the reporter's user to read the aliases named `<index>-<type>`, for example with the `view_index_metadata` privilege on them. Without this privilege, the check finds no alias, without a warning, and the reporter starts as if no alias existed. Remove the aliases before the switch, as the following steps describe.
{% endhint %}

To migrate, complete the following steps in order:

1.  Stop every Gateway from writing in `ilm` mode. Use one of the following methods:
    * Deploy every Gateway with `index_mode: data_stream`. While the aliases exist, the reporter of each Gateway stays inactive. The Gateways serve API traffic but don't report analytics.
    * Scale the Gateways down.
2.  Once no Gateway writes in `ilm` mode, for each alias, mark its write index as complete, and then remove the alias. The following example uses the `gravitee-request` alias:
    1.  Find the write index of the alias, which has `is_write_index` set to `true`:

        ```json
        GET _alias/gravitee-request
        ```
    2.  Mark the write index as complete, for example `gravitee-request-000003`:

        ```json
        PUT gravitee-request-000003/_settings
        {
          "index.lifecycle.indexing_complete": true
        }
        ```

        Without this setting, ILM stops in error on the rollover of this index, because the alias no longer points to it, and the index is never deleted. With this setting, ILM skips the rollover and applies the rest of the policy.
    3.  Remove the alias:

        ```json
        DELETE gravitee-request-*/_alias/gravitee-request
        ```

    To remove all the aliases in one call, use the `remove` actions of `POST _aliases`. The previous indices stay and keep their data under their own names.
3.  Restart the Gateways. A reporter that stopped at startup stays inactive until its Gateway restarts.
4.  Set `analytics.elasticsearch.index_mode` to `data_stream` on the Management API, and then restart it. With Helm, `es.index_mode: data_stream` sets both the Gateways and the Management API.

Alternatively, keep the aliases and write the data streams with another `index` prefix. Set the same prefix in `reporters.elasticsearch.index` for every Gateway and in `analytics.elasticsearch.index` for the Management API. With Helm, set `es.index`.

## Migrate on OpenSearch

Follow the same steps. In the reporter configuration, leave the `lifecycle.policies` and `lifecycle.retention` settings unset. With `index_mode: data_stream` on OpenSearch, the reporter stops at startup when one of them is set. The `ism_template` of the ISM policies replaces them.

## Verify the migration

After the switch, send a few API calls through each Gateway, and then check the following points:

1.  The reporter starts in the `data_stream` mode. At startup, the log of each Gateway contains the following lines:

    ```
    Elasticsearch reporter: flavor [classic] (detected), authentication [...], index mode [data_stream], disabled by the flavor [none]
    Starting Elastic reporter engine... DONE
    ```

    No ERROR line contains `The Elasticsearch reporter is disabled`. Such a line names the setting or the alias that stops the reporter. A WARN line that lists data streams whose documents are never deleted means that their types have no lifecycle.
2.  The data streams exist. Run the following request:

    ```json
    GET _data_stream/gravitee-*
    ```

    The response lists the data streams named `<index>-<type>`, for example `gravitee-request` and `gravitee-v4-metrics`. Each data stream is created with the first document of its type. A type without traffic, for example `gravitee-v4-message-metrics`, appears only after its first document.
3.  The new documents go to the data streams. Run the following request:

    ```json
    GET gravitee-request/_search?size=1&sort=@timestamp:desc
    ```

    The `_index` of the hit starts with `.ds-gravitee-request-`. The following request lists no index created after the switch:

    ```json
    GET _cat/indices/gravitee-request-*?v&h=index,creation.date.string
    ```
4.  The lifecycle is attached. Run the following request:

    ```json
    GET _data_stream/gravitee-request
    ```

    With a lifecycle policy, the response shows `ilm_policy` with the name of the policy. With a retention, the response shows `lifecycle.data_retention` with its value. On OpenSearch, `GET _plugins/_ism/explain/gravitee-request` shows the `policy_id` of the ISM policy whose `ism_template` matches the data stream.
5.  The Management Console shows the new analytics. Open the analytics and the logs of an API that received calls after the switch. These calls appear. The calls made before the switch don't appear, because the Management API reads only the data streams.

## Revert to dated or ILM-managed indices

While the data streams exist, you can't revert to the `daily` or `ilm` mode with the same `index` prefix. Elasticsearch refuses the index templates of these modes, and an alias named like a data stream. To revert, use one of the following methods:

* Set `index_mode` back to `daily` or `ilm` with another `index` prefix, on every Gateway and on the Management API. The data streams stay, but the Gateways and the Management API no longer write or read them.
* Delete the data streams, and their documents, before you set `index_mode` back to `daily` or `ilm` with the same prefix.
