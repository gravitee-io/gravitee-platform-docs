---
description: Documentation about upgrade guides in the context of APIs.
metaLinks:
  alternates:
    - ./
---

# Upgrade Guides

Gravitee includes [Release Notes](../release-information/release-notes/README.md) and [Changelogs](../release-information/changelog/README.md) for each release to keep you apprised of features and fixes and to help you navigate version upgrades. When upgrading your version of APIM, consider the following guidelines.

* **Upgrading APIM is deployment-specific:** The [4.0 breaking changes](../release-information/breaking-changes-and-deprecations.md#id-4.0-breaking-changes) must be noted and/or adopted for a successful upgrade.
* **Ensure that you are aware of the breaking changes and deprecated functionality:** For more information about the breaking changes and deprecated functionality, see [Breaking Changes and Deprecations](../release-information/breaking-changes-and-deprecations.md).
* **If your upgrade will skip versions:** Read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.
* **Migrate v1 APIs before you upgrade to 4.12.0 or later:** From version 4.12.0, APIM no longer supports v1 APIs, and the migration tooling isn't included. Migrate v1 APIs to at least a v2 definition while your installation runs version 4.11.x or earlier. For the migration steps, see [Migrate v1 APIs to v2](migrate-v1-apis-to-v2.md).
* **Upgrade your license file:** If you are an existing Gravitee Enterprise customer upgrading to 4.x, you must upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support to receive a new 4.x license.
* **Run scripts on the correct database:** `gravitee` is not always the default database. Run `show dbs` to return your database name.

## Upgrade components in order

An APIM upgrade touches several components. Upgrade them in the following order:

1. Upgrade the Management API first, and let it finish starting before you upgrade the other components. The Management API applies the data migrations for the new version on startup, and each migration runs once.
2. Upgrade the Console and the Developer Portal.
3. Upgrade the Gateways. Recommended: upgrade Gateways progressively instead of stopping the whole fleet at once. Before you upgrade a hybrid Gateway, confirm that the Gateway and control plane versions are compatible: Classic Cloud deployments follow the [Gateway and Bridge compatibility tables](../hybrid-installation-and-configuration-guides/classic-cloud/README.md#gateway-and-bridge-compatibility-versions), and Next-Gen Cloud hybrid Gateways match the Control Plane version.
4. If you manage APIs with the Gravitee Kubernetes Operator (GKO), upgrade GKO after APIM. Keep your APIM version equal to or newer than your GKO version at every step. For the supported version window, see [GKO Compatibility and Limitations](../../../gko/4.12/overview/compatibility-and-limitations.md).

Validate each environment before you move to the next one: upgrade and test a non-production environment first, and then repeat the same sequence in production.

## Downgrades aren't supported

Gravitee supports upgrades only. After you upgrade an installation, don't roll it back to an earlier version.

APIM applies data migrations the first time the new version of the Management API starts. Those migrations run forward only, and the new version writes values that an earlier version doesn't recognize. Pointing an earlier version of APIM at a database that a later version has already migrated leads to startup failures and data errors.

To move back to an earlier version, restore the backup of your database that you took before the upgrade, and then start the earlier version against the restored database. Take that backup before every upgrade, and confirm that it restores into an empty instance.

To evaluate an earlier version alongside your current installation, point the earlier version at a separate, empty database, or at a restored copy of a pre-upgrade backup. Never point it at your current database.

## Upgrade articles

For more information about upgrading your APIM environment, see the following articles:

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Upgrade APIM from 4.8.x to 4.10.x</td><td><a href="upgrade-apim-from-4.8.x-to-4.10.x.md">upgrade-apim-from-4.8.x-to-4.10.x.md</a></td></tr><tr><td>Update the Connection to the Cloud</td><td><a href="update-the-connection-to-cloud.md">update-the-connection-to-cloud.md</a></td></tr><tr><td>APIM 4.4+ &#x26; Hybrid Gateways</td><td><a href="apim-4.4.+-and-hybrid-gateways.md">apim-4.4.+-and-hybrid-gateways.md</a></td></tr><tr><td>Upgrade with RPM</td><td><a href="upgrade-with-rpm.md">upgrade-with-rpm.md</a></td></tr><tr><td>APIM 4.12 Elasticsearch Index Template Changes</td><td><a href="apim-4.12-elasticsearch-index-template-changes.md">apim-4.12-elasticsearch-index-template-changes.md</a></td></tr><tr><td>Migrate v1 APIs to v2</td><td><a href="migrate-v1-apis-to-v2.md">migrate-v1-apis-to-v2.md</a></td></tr></tbody></table>
