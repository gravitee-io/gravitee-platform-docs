---
description: >-
  A checklist for upgrading Gravitee API Management from 4.8.x to 4.10.x,
  covering pre-upgrade checks, breaking changes, and post-upgrade validation.
---

# Upgrade APIM from 4.8.x to 4.10.x

## Overview

This checklist covers the upgrade path from APIM 4.8.x to 4.10.x. It collects the checks to run before you upgrade, the breaking changes introduced in 4.9.0 and 4.10.0, and the steps that confirm the upgrade succeeded.

The upgrade crosses two minor versions, so the breaking changes of both 4.9.0 and 4.10.0 apply. Read the [Breaking Changes and Deprecations](../release-information/breaking-changes-and-deprecations.md) page in full before you start.

{% hint style="warning" %}
Downgrades aren't supported. Take a backup of your database before you upgrade. For more information, see [Downgrades aren't supported](README.md#downgrades-arent-supported).
{% endhint %}

## Before you upgrade

Complete each of the following checks against your current 4.8.x installation.

### Back up your data

Back up your management database and your analytics store, and confirm that the backup restores into an empty instance. APIM applies data migrations the first time the new version of the Management API starts. Those migrations run forward only, so the backup is the only way back to 4.8.x.

### Check your Java version

APIM 4.8.x and 4.10.x both run on Java 21. The upgrade doesn't require a Java upgrade. If you run APIM from the `.zip` distribution on your own JVM, confirm that the JVM is Java 21 before you upgrade.

### Check your database version

Confirm that your database version is supported by 4.10.x:

<table>
    <thead>
        <tr>
            <th width="200">Database</th>
            <th>Versions tested with 4.10.x</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>MongoDB</td>
            <td>4.4.x, 5.0.x, 6.0.x, 7.0.x, and 8.0.x</td>
        </tr>
        <tr>
            <td>PostgreSQL</td>
            <td>11.x to 17.x</td>
        </tr>
        <tr>
            <td>MariaDB</td>
            <td>10.4.x to 11.x</td>
        </tr>
        <tr>
            <td>MySQL</td>
            <td>8.0.x and 8.2.x</td>
        </tr>
        <tr>
            <td>Microsoft SQL Server</td>
            <td>2017, 2019, and 2022</td>
        </tr>
    </tbody>
</table>

For the full details, see [MongoDB](../prepare-a-production-environment/repositories/mongodb.md) and [JDBC](../prepare-a-production-environment/repositories/jdbc.md).

### Check your analytics store version

Confirm that your analytics store version is supported by 4.10.x:

<table>
    <thead>
        <tr>
            <th width="200">Analytics store</th>
            <th>Versions tested with 4.10.x</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Elasticsearch</td>
            <td>7.17.x, 8.19.x, and 9.3.x</td>
        </tr>
        <tr>
            <td>OpenSearch</td>
            <td>1.x, 2.x, and 3.x</td>
        </tr>
    </tbody>
</table>

For the full details, see [Elasticsearch](../prepare-a-production-environment/repositories/elasticsearch.md).

### Check your license

Confirm that your Enterprise license is valid and isn't about to expire. Contact your Customer Success Manager or Gravitee Support to renew it. For more information, see [Enterprise Edition](../introduction/enterprise-edition.md).

### Plan for the Elasticsearch index template change

APIM 4.9.0 changed the Elasticsearch index templates. Applying the new templates is a manual step, and analytics data doesn't display correctly until you complete it. Read [APIM 4.9 Elasticsearch Index Template Changes](apim-4.9-elasticsearch-index-template-changes.md) before you upgrade, and schedule the template update as part of the upgrade window.

## Breaking changes to review

The following breaking changes land between 4.8.x and 4.10.x. Each entry links to the detailed description on the [Breaking Changes and Deprecations](../release-information/breaking-changes-and-deprecations.md) page.

### Introduced in 4.9.0

* **Elasticsearch template updates required.** The index templates changed. Apply the new templates as described in [APIM 4.9 Elasticsearch Index Template Changes](apim-4.9-elasticsearch-index-template-changes.md).
* **OpenShift compatibility update.** Review this change if you deploy APIM on OpenShift.
* **Customization on Federation ingress.** Review this change if you customized the Federation ingress in your Helm values.

### Introduced in 4.10.0

* **Kafka Native APIs analytics.** Review this change if you run native Kafka APIs and rely on their analytics data.

## Upgrade

Follow the upgrade procedure for your deployment method. The procedure itself doesn't change for this version pair:

* For Helm and Kubernetes, update the chart version and the image tags, and then roll out the release.
* For Docker, update the image tags, and then recreate the containers.
* For RPM, see [Upgrade with RPM](upgrade-with-rpm.md).

Start the Management API first and let it finish starting before you start the other components. The Management API applies the data migrations for the new version on startup, and each migration runs once.

## Validate the upgrade

Run these checks after every component restarts.

1. Confirm that each component reports the new version. The Console displays the APIM version in the footer.
2. Open the Console and confirm that your APIs, applications, and subscriptions are listed.
3. Call an API through the Gateway and confirm that you receive the expected response.
4. Open the analytics dashboard of an API that receives traffic and confirm that new requests appear. Analytics data that doesn't appear after the upgrade usually means the Elasticsearch index templates aren't updated.
5. Confirm that your Enterprise features are still active, which confirms that the license loaded.

## What to watch for after the upgrade

* **Analytics dashboards are empty or incomplete.** The 4.9.0 Elasticsearch index templates aren't applied. See [APIM 4.9 Elasticsearch Index Template Changes](apim-4.9-elasticsearch-index-template-changes.md).
* **Analytics data for native Kafka APIs looks different.** This is expected. See the 4.10.0 breaking change on the [Breaking Changes and Deprecations](../release-information/breaking-changes-and-deprecations.md) page.
* **MongoDB index changes.** APIM creates new indexes on startup. On a large database, index creation adds time to the first startup of the Management API. For more information, see [MongoDB Index Management](mongodb-index-management.md).
* **A hybrid Gateway doesn't reconnect.** Confirm that the Gateway version and the control plane version are compatible. See [APIM 4.4.+ & Hybrid Gateways](apim-4.4.+-and-hybrid-gateways.md).
