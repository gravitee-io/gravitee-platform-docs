---
description: An overview about deployment.
metaLinks:
  alternates:
    - deployment.md
---

# Deployment

## Overview

Deploying a plugin is as easy as copying the plugin archive (zip) into the dedicated directory. By default, you need to deploy the archives in `${GRAVITEE_HOME/plugins}`. Refer to [APIM Gateway Configuration ](../configure-and-manage-the-platform/gravitee-gateway/#configure-the-plugins-directory)for more information on modifying the directory structure.

{% hint style="warning" %}
You must restart APIM nodes when applying new or updated plugins.
{% endhint %}

## Plugins directory

The plugins directory can be configured via either local installation or Helm.

{% tabs %}
{% tab title="Local installation" %}
You can configure the APIM Gateway [plugins](./) directory with `plugins.path` configuration property:

```yaml
plugins:
  path: ${gravitee.home}/plugins
```

Users can add plugins not included in APIM's default distribution to this directory. This includes different versions of Gravitee plugins or their own [custom plugins](customization/).

{% hint style="info" %}
To understand how Gravitee handles duplicate plugins, see plugins [discovery and loading.](deployment.md#discovery-and-loading)
{% endhint %}

If you do not wish to modify the default directory, Gravitee also lets you specify additional folders in an array:

```yaml
plugins:
  path:
  - ${gravitee.home}/plugins
  - ${gravitee.home}/plugins-ext 
```

In this example, bundled plugins remain in the default directory. This configuration adds an additional `plugins-ext` directory for the user to add plugins not included in APIM's default distribution.
{% endtab %}

{% tab title="Helm Chart" %}
Gravitee's Helm Chart protects the bundled plugins directory by default. This is a sample configuration of how to add additional plugins:

{% code title="value.yaml" %}
```yaml
gateway:
  additionalPlugins:
  - http://host:port/path/to/my-plugin.zip
  - http://host:port/path/to/my-gateway-plugin.zip
api:
  additionalPlugins:
  - http://host:port/path/to/my-plugin.zip
```
{% endcode %}

The property `removePlugins` has been removed from the Helm chart as it is no longer necessary. See [plugin discovery and loading](deployment.md#discovery-and-loading) for more information.
{% endtab %}
{% endtabs %}



### **Air-gapped clusters and environments without internet access**

`additionalPlugins` relies on an initContainer that uses `wget` to download each URL into `/tmp/plugins-ext` before the Gateway or Management API starts. The initContainer needs network egress to every URL you list, so it isn't suitable when the cluster can't reach an external host or when initContainers aren't permitted. For those cases, mount the plugin archives directly into the `plugins-ext` directory using `extraVolumes` and `extraVolumeMounts`.

The chart sets `GRAVITEE_PLUGINS_PATH_0` to `${gravitee.home}/plugins` and `GRAVITEE_PLUGINS_PATH_1` to `${gravitee.home}/plugins-ext`. Inside the container, `plugins-ext` resolves to `/opt/graviteeio-gateway/plugins-ext` for the Gateway and `/opt/graviteeio-management-api/plugins-ext` for the Management API. Mount your plugin archives at either path.

#### **Option 1: Mount plugins from a ConfigMap or Secret**

Use this option for small plugin archives. For larger archives, use Option 2.

1.  Create the ConfigMap from the plugin `.zip` files:

    ```bash
    kubectl create configmap gravitee-plugins \
      --from-file=my-plugin.zip=/path/to/my-plugin.zip \
      --from-file=my-other-plugin.zip=/path/to/my-other-plugin.zip \
      -n gravitee
    ```
2.  Reference the ConfigMap in `values.yaml`:

    ```yaml
    gateway:
      extraVolumes: |
        - name: gravitee-plugins
          configMap:
            name: gravitee-plugins
      extraVolumeMounts: |
        - name: gravitee-plugins
          mountPath: /opt/graviteeio-gateway/plugins-ext
          readOnly: true

    api:
      extraVolumes: |
        - name: gravitee-plugins
          configMap:
            name: gravitee-plugins
      extraVolumeMounts: |
        - name: gravitee-plugins
          mountPath: /opt/graviteeio-management-api/plugins-ext
          readOnly: true
    ```

#### **Option 2: Mount plugins from a PersistentVolume**

Use this option for larger plugin archives, or when you want to update plugins without re-templating the chart.

1. Pre-populate a PersistentVolume with the plugin `.zip` files using a mechanism supported by your storage class (for example, a storage admin copying the archives onto the underlying disk, or a one-off Job that runs before the APIM release).
2.  Bind the PVC in `values.yaml`:

    ```yaml
    gateway:
      extraVolumes: |
        - name: gravitee-plugins
          persistentVolumeClaim:
            claimName: gravitee-plugins-pvc
      extraVolumeMounts: |
        - name: gravitee-plugins
          mountPath: /opt/graviteeio-gateway/plugins-ext
          readOnly: true
    ```

#### **Option 3: Pull plugins with a custom initContainer**

Use this option when the cluster can reach an internal artifact store (for example, an internal S3 bucket, Nexus, or Artifactory) but can't reach the public internet. Replace the default download initContainer with one that targets your internal source.

1.  Leave `additionalPlugins` empty and define an `extraInitContainers` block:

    ```yaml
    gateway:
      extraInitContainers: |
        - name: fetch-plugins
          image: amazon/aws-cli:2.15.0
          command:
            - sh
            - -c
            - aws s3 cp s3://internal-gravitee-plugins/ /tmp/plugins-ext/ --recursive
          volumeMounts:
            - name: gravitee-plugins
              mountPath: /tmp/plugins-ext
      extraVolumes: |
        - name: gravitee-plugins
          emptyDir: {}
      extraVolumeMounts: |
        - name: gravitee-plugins
          mountPath: /opt/graviteeio-gateway/plugins-ext
    ```
2. Ensure the custom image is pullable from a registry the cluster can reach. Apply the same pattern to the `api` section if the Management API also needs plugins.

{% hint style="info" %}
Plugins mounted via `extraVolumeMounts` follow the same discovery and loading rules as plugins downloaded by `additionalPlugins`. A plugin in `plugins-ext` with the same ID as a bundled plugin takes precedence because its file modification time is more recent.
{% endhint %}

## Discovery and loading

Plugin discovery and loading occurs regardless of APIM license type. If a plugin is not included with your license, then it will be loaded but it will not be functional.

### Phase 1: Discover plugins

When APIM starts, all plugin zip files are read from the list of plugin directories set in the `gravitee.yaml` configuration file.

{% hint style="info" %}
This operation is completed asynchronously for performance benefits.
{% endhint %}

If duplicate plugins are found (same type and ID), the plugin with the most recent update date on the file system is loaded, regardless of its version. This ensures that newer plugin zip files automatically take precedence over older ones.

This behavior is particularly useful when deploying with Helm with the `additionalPlugins` capability. Since plugins added through this method are downloaded and placed in the `/plugin-ext` folder, they always have a more recent update date than the plugins bundled within APIM. As a result, they are the ones effectively loaded.

This mechanism simplifies plugin management by eliminating the need to manually remove older versions. It is especially beneficial for Kubernetes-based deployments and plugin developers, as they can update a plugin by simply copying the new file without additional scripting for removal.

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
