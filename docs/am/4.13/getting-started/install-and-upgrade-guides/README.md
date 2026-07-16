---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/getting-started/install-and-upgrade-guides
---

# Install & Upgrade Guides

{% hint style="warning" %}
**Changes to Gravitee distribution bundle**

Version 3.18.0 of the Gravitee platform (released on 7th July 2022) has introduced a unified, single distribution bundle for all features available in the Community Edition (CE) and the Enterprise Edition (EE) of Gravitee APIM. This provides a smooth transition from CE to EE functionality and allows you to trial EE features without requiring migration or a standalone EE installation.

If you are a Gravitee CE user and you want to try out EE features, install the unified bundle, request an EE license, apply it to the installation, and restart. You no longer need to download a new EE version of APIM!

In addition, you can now [register for a free time-limited Gravitee Cockpit trial directly on the web](https://cockpit.gravitee.io/register). Registration allows you to access a full EE-grade API Management trial (including Alert Engine), manage Gravitee environments and installations, and design APIs with the Gravitee API Designer (also included in the trial).

For more information about Enterprise Edition licenses, installation, and versioning, see the Enterprise Edition section.
{% endhint %}

As described in the Introduction to Gravitee Access Management (AM), AM is split into three main components:

* AM Gateway
* AM Management API
* AM Management Console

The guides in this section provide the details of how you can setup, configure, and upgrade your AM environment.

## Downgrades aren't supported

Gravitee supports upgrades only. After you upgrade an installation, don't roll it back to an earlier version.

AM applies data migrations the first time the new version starts. Those migrations run forward only, and the new version writes values that an earlier version doesn't recognize. For example, AM 4.9.0 added the MFA challenge and MFA enrollment flows. A security domain that uses one of those flows can't be read by AM 4.8.x, and the earlier version fails when it loads the domain. Pointing an earlier version of AM at a database that a later version has already migrated leads to startup failures and data errors.

To move back to an earlier version, restore the backup of your database that you took before the upgrade, and then start the earlier version against the restored database. Take that backup before every upgrade, and confirm that it restores into an empty instance.

To evaluate an earlier version alongside your current installation, point the earlier version at a separate, empty database, or at a restored copy of a pre-upgrade backup. Never point it at your current database.

For the changes that each version introduces, see [Breaking changes for Access Management](breaking-changes-for-access-management.md).
