---
description: Configuration guide for Deploying plugins.
---

# Deploying plugins

## Deployment

Deploying a plugin is as easy as copying the plugin archive (zip) into the dedicated directory. By default, you need to deploy the archives in `${GRAVITEE_HOME/plugins}`. Refer to [APIM Gateway Configuration ](../../../using-the-product/using-the-gravitee-api-management-components/general-configuration/README.md#configure-the-plugins-directory)for more information on modifying the directory structure.

{% hint style="warning" %}
You must restart APIM nodes when applying new or updated plugins.
{% endhint %}

## Discovery and loading

Plugin discovery and loading occurs regardless of APIM license type. If a plugin is not included with your license, then it will be loaded but it will not be functional.

### Phase 1: Discover plugins

When APIM starts, all plugin zip files are read from the list of plugin directories set in the `gravitee.yaml` configuration file.

{% hint style="info" %}
This operation is completed asynchronously for performance benefits.
{% endhint %}

If duplicates are found (same type and ID), the most recent file is kept regardless of the plugin's version. This allows for easily overriding plugins.

Plugin override circumvents the need to remove plugins to use a newer version, which is a huge benefit for Kubernetes deployments via Gravitee's Helm Chart. This also benefits plugin developers, as they can pack and copy an updated plugin without having to script the removal of the old version.

### Phase 2: Load plugins

After APIM finishes traversing the plugin directories, the plugins are loaded.

Plugins are immediately initialized by a specialized handler. If an error occurs while unpacking a plugin zip file, the faulty plugin is ignored. An error will be reported in the logs and the loading of the remaining plugins will resume.

The loading process is sequential and adheres to the following order based on plugin type:

1. Cluster
2. Cache
3. Repository
4. Alert
5. Cockpit
6. Any other types

The rest of the plugins are loaded in no particular order, except if they have dependencies. If a plugin depends on another plugin, that takes precedence over type ordering.

For example, if `plugin1 (type:cluster)` depends on `plugin2 (type:cache)` which depends on `plugin3(type:alert)`, then the plugins are loaded in the following order:

* `plugin3` (because plugin 2 depends on it, even if it is #4 in the type priority list)
* `plugin2` (because plugin 1 depends on it, even if it is #2 in the type priority list)
* `plugin1`
