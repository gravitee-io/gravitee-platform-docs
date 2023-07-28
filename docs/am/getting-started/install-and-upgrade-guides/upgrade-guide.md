# 4.0 Upgrade Guide

## Overview

Upgrading to APIM 4.0 is deployment-specific. The 4.0 breaking changes cited below must be noted and/or adopted for a successful upgrade.

{% hint style="warning" %}
**If your upgrade will skip versions:** Read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.

**Run scripts on the correct database:** `gravitee` is not always the default database. Run `show dbs` to return your database name.
{% endhint %}



\


## MongoDB indexes



Starting from AM 4.0, the MongoDB indexes are now named using the first letter of the fields that compose the index. This change will allow to manage automatically indexes creation on DocumentDB. Before starting the Management API service, please execute the following link:https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/master/gravitee-am-repository/gravitee-am-repository-mongodb/src/main/resources/scripts/create-index.js\[script] to delete indexes and recreate them with the right convention.

