---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/getting-started/install-and-upgrade-guides/upgrade-guide
description: Upgrading Access Management 4.13 creates application table indexes automatically. Follow the upgrade steps for your version and deployment.
---
# Upgrade guide

{% hint style="warning" %}
**If your upgrade skips versions:** Read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.

**Run scripts on the correct database:** `gravitee` is not always the default database. Run `show dbs` to return your database name.
{% endhint %}

## 4.13 Upgrade guide

### Before the upgrade

Find applications that define their own password policy if any. This feature is removed 4.13. Recreate them as domain or identity-provider password policies to make sure that a password policy will be applied.

Some internal interface have been moved or evolved, if you managed to create custom policies make sure that you are not using AuthenticationFlowContextService or ExtensionGrantProvider interfaces. If you are using them you may have to adapt and rebuilt your plugin.

### Configuration to adapt

#### Management API gravitee.yml

Remove the `repositories.gateway`, `repositories.oauth2` and `ratelimit` blocks. The Management API now handles only the management scope.
Set `console.ui.url correctly`, the Console now uses it as the redirect after login, instead of a hard-coded `localhost:4200`.

`domains.identities.default.useSystemCluster` (default true): behaviour change. A new domain’s default identity provider is now bound to the system cluster instead of copying the management MongoDB URI. Set it to false to keep the 4.12 behaviour. Existing identity providers are not affected.

`repositories.system-cluster-restricted (default false)`: prevent an admin to define database and collection name when "use system cluster" option is used in MongoDB IDP.

#### Gateway gravitee.yaml:

Liquibase has to be enabled if you are using RDMS. `repositories.<scope>.jdbc.liquibase.enabled` turns Liquibase on or off per scope, overriding the global `liquibase.enabled`.

#### Helm

`console.ui.url` and `console.api.url` are now always written. When left empty they are built as `https://<first ingress host><path>`. Set them explicitly if you use plain http or the first host is not the right one.

On JDBC, Gateway has to run the oauth2 and gateway database migrations. Make sure liquibase is active.

### Upgrade Order

{% hint style="warning" %}
Before upgrading, create a backup of the database
{% endhint %}

Management API first.

This step:

* applies 13 management schema changes on JDBC. All are additive and can be re-run safely.
* creates the new trusted_domains structures.
* migrates each domain’s inline trusted issuers into trusted domains (DomainTrustedIssuerUpgrader) and moves the SPIFFE settings into keyRetrievalSettings.

Roll the gateways. You don’t need to stop all nodes at once. During the rollout, 4.12 gateways still read the old trust_domains, so trust changes made in 4.13 are invisible to them.

### After the upgrade

Check the Management API logs:

* WARN lines for trusted issuers that were not migrated (name too long or already taken).
* customised consent pages: they still work, but scopes can now be selected one by one; mark scopes required where needed

### Rollback

The schema stays readable by 4.12, but some data written in 4.13 is lost to it:

* new trusted domains (SPIFFE only)

If you created custom claims for the new IDJag token at application level, rollback can only be done on the latest 4.12, 4.11,  4.10 or 4.9.


## 4.12 Upgrade guide

### Application table indexes

In AM 4.12.0 and later, database indexes are created automatically on the JDBC applications table or MongoDB collection during upgrade to support cursor pagination by `updatedAt` and `name` fields. No manual migration steps are required.

## 4.7 Upgrade guide 

For the 4.7 upgrade guide, see [4.7 Upgrade guide](4.7-upgrade-guide.md)

### 4.5 Upgrade guide

### General

Upgrading to AM 4.5 is deployment-specific. The [4.0 breaking changes](https://documentation.gravitee.io/am/v/4.0/releases-and-changelog/changelog/am-4.0.x#gravitee-access-management-4.0.0-july-20-2023) must be noted and/or adopted for a successful upgrade.

### MongoDB indices

Starting with AM 4.0, the MongoDB indices are now named using the first letters of the fields that compose the index. This change will allow automatic management of index creation on DocumentDB.

Before starting the Management API service, please execute the following [script](https://github.com/gravitee-io/gravitee-access-management/blob/master/gravitee-am-repository/gravitee-am-repository-mongodb/src/main/resources/scripts/create-index.js) to delete and recreate indices with the correct convention. If this script is not executed, the service will start, but there will be errors in the logs.
