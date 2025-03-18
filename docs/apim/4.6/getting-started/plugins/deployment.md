# Deployment

## Overview

Deploying a plugin is as easy as copying the plugin archive (zip) into the dedicated directory. By default, you need to deploy the archives in `${GRAVITEE_HOME/plugins}`. Refer to [APIM Gateway Configuration ](../../configure-apim/apim-components/gravitee-gateway.md#configure-the-plugins-directory)for more information on modifying the directory structure.

{% hint style="warning" %}
You must restart APIM nodes when applying new or updated plugins.
{% endhint %}

## Discovery and loading

Plugin discovery and loading occurs regardless of APIM license type. If a plugin is not included with your license, then it will be loaded but it will not be functional.

### Phase 1: Discover plugins

When APIM starts, all plugin zip files are read from the list of plugin directories set in the `gravitee.yaml` configuration file.&#x20;

{% hint style="info" %}
This operation is completed asynchronously for performance benefits.
{% endhint %}

If duplicate plugins are found (same type and ID), the plugin with the most recent update date on the file system is loaded, regardless of its version. This ensures that newer plugin zip files automatically take precedence over older ones.

\
This behavior is particularly useful when deploying with Helm with the `additionalPlugins` capability. Since plugins added through this method are downloaded and placed in the `/plugin-ext` folder, they always have a more recent update date than the plugins bundled within APIM. As a result, they are the ones effectively loaded.

\
This mechanism simplifies plugin management by eliminating the need to manually remove older versions. It is especially beneficial for Kubernetes-based deployments and plugin developers, as they can update a plugin by simply copying the new file without additional scripting for removal.

### Phase 2: Load plugins

After APIM finishes traversing the plugin directories, the plugins are loaded.&#x20;

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

* `plugin3` (because plugin 2 depends on it,  even if it is #4 in the type priority list)
* `plugin2` (because plugin 1 depends on it, even if it is #2 in the type priority list)
* `plugin1`
