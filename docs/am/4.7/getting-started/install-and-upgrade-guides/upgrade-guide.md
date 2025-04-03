# 4.5 Upgrade Guide

{% hint style="warning" %}
**If your upgrade will skip versions:** Read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.

**Run scripts on the correct database:** `gravitee` is not always the default database. Run `show dbs` to return your database name.
{% endhint %}

## General

Upgrading to AM 4.5 is deployment-specific. The [4.0 breaking changes](https://documentation.gravitee.io/am/v/4.0/releases-and-changelog/changelog/am-4.0.x#gravitee-access-management-4.0.0-july-20-2023) must be noted and/or adopted for a successful upgrade.

## MongoDB indices

Starting with AM 4.0, the MongoDB indices are now named using the first letters of the fields that compose the index. This change will allow automatic management of index creation on DocumentDB.&#x20;

Before starting the Management API service, please execute the following [script](https://github.com/gravitee-io/gravitee-access-management/blob/master/gravitee-am-repository/gravitee-am-repository-mongodb/src/main/resources/scripts/create-index.js) to delete and recreate indices with the correct convention. If this script is not executed, the service will start, but there will be errors in the logs.
