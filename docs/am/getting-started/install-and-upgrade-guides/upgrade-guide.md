# 4.0 Upgrade Guide

{% hint style="warning" %}
**If your upgrade will skip versions:** Read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.

**Run scripts on the correct database:** `gravitee` is not always the default database. Run `show dbs` to return your database name.
{% endhint %}

## General

Upgrading to APIM 4.0 is deployment-specific. The [4.0 breaking changes](../../releases-and-changelog/changelogs/am-4.x.x-2023-07-26.md#breaking-changes) must be noted and/or adopted for a successful upgrade.

## MongoDB indexes

Starting with AM 4.0, the MongoDB indices are now named using the first letters of the fields that compose the index. This change will allow automatic management of index creation on DocumentDB. Before starting the Management API service, please execute the following [script](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/master/gravitee-am-repository/gravitee-am-repository-mongodb/src/main/resources/scripts/create-index.js) to delete and recreate indices with the correct convention.

