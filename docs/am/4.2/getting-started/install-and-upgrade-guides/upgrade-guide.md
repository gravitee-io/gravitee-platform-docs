# 4.2 Upgrade Guide

{% hint style="warning" %}
**If your upgrade will skip versions:** Read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.

**Run scripts on the correct database:** `gravitee` is not always the default database. Run `show dbs` to return your database name.
{% endhint %}

## General

Upgrading to AM 4.2 is deployment-specific. If you are upgrading from AM 3.x, the [4.0 breaking changes](https://documentation.gravitee.io/am/4.0/releases-and-changelog/changelog/am-4.0.x#gravitee-access-management-4.0.0-july-20-2023) must be noted and/or adopted for a successful upgrade. In addition the [upgrade guide](https://documentation.gravitee.io/am/4.0/getting-started/install-and-upgrade-guides/upgrade-guide) for AM 4.0 needs to be followed. If you are upgrading from AM 4.x, no specific actions are required.