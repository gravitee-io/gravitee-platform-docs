# Copy of Plugins

## Overview

Plugins bring Gravitee APIM to life. They provide functionality ranging from connectors (for example, Kafka) to tracers (for example, Jaeger) and everything in between. A special mention goes to policies - these are plugins that provide you with options to shape and control the flow of your APIs.

A lot of plugins are part of the Gravitee APIM installation. Ones that are not generally applicable, can be added. You can even write your own plugins! This document explains how you can install and upgrade additional plugins.

## In a nutshell - Option I

1. Get your plugin zip-file ready. The supported plugins for Gravitee APIM can be found [here](https://download.gravitee.io/#graviteeio-apim/plugins/).
2. Drop the plugin zip file in the plugins folder of the relevant component. This could be the APIM REST API, the APIM Gateway, or both!
3. Restart the component. !!! note At this time installing and updating plugins requires a restart of the component.

## In a nutshell - Option II

1. Get your plugin zip-file ready. The supported plugins for Gravitee APIM can be found [here](https://download.gravitee.io/#graviteeio-apim/plugins/).
2. Drop the plugin zip file in a plugins folder of your own choosing.
3. Modify the `gravitee.yml` configuration file of the relevant component (APIM REST API / APIM Gateway / both) to take the additional folder into account.
4. Restart the component. !!! note At this time installing and updating plugins requires a restart of the component.

## Details for .ZIP installations

### Option I

1. Locate the plugins folder of the component

* APIM REST API - `<your installation folder>/graviteeio-apim-rest-api-{{ site.products.apim._3x.version }}/plugins`
* APIM Gateway - `<your installation folder>/graviteeio-apim-gateway-{{ site.products.apim._3x.version }}/plugins`

2. Drop the plugin zip file into the folder.
3. Restart the component.

### Option II

1. Create custom locations for plugins

```
mkdir /customlocation/gateway/plugins
mkdir /customlocation/rest-api/plugins
```

!!! note This are example locations, yours can differ. 2. Drop the plugin zip file into the relevant folder(s). 3. Modify the `gravitee.yml` configuration file of the component **APIM REST API** - `<your installation folder>/graviteeio-apim-rest-api-{{ site.products.apim._3x.version }}/config`:

```
  # Plugins repository
  plugins:
    path:
      - ${gravitee.home}/plugins
      - /customlocation/rest-api/plugins
```

**APIM Gateway** - `<your installation folder>/graviteeio-apim-gateway-{{ site.products.apim._3x.version }}/config`:

```
  # Plugins repository
  plugins:
    path:
      - ${gravitee.home}/plugins
      - /customlocation/gateway/plugins
```

4. Restart the component.

## Details for package installations (Amazon Linux, RHEL, CentOS)

### Option I

1. Locate the plugins folder of the component:

* APIM REST API - `/opt/graviteeio/apim/rest-api/plugins`
* APIM Gateway - `/opt/graviteeio/apim/gateway/plugins`

2. Drop the plugin zip file into the folder.
3. Restart the component.

### Option II

1. Create custom locations for plugins

```
mkdir /customlocation/gateway/plugins
mkdir /customlocation/rest-api/plugins
```

!!! note This are example locations, yours can differ. 2. Drop the plugin zip file into the relevant folder(s). 3. Modify the `gravitee.yml` configuration file of the component: **APIM REST API** - `/opt/graviteeio/apim/rest-api/config`

```
# Plugins repository
plugins:
  path:
    - ${gravitee.home}/plugins
    - /customlocation/rest-api/plugins
```

**APIM Gateway** - `/opt/graviteeio/apim/gateway/config`

```
# Plugins repository
plugins:
  path:
    - ${gravitee.home}/plugins
    - /customlocation/gateway/plugins
```

4. Restart the component

## Details for Docker installations

!!! note **Option I** is not available for Docker installations as there is no direct access to the inside of the container.

### Option II

1. Create custom locations for plugins.

```
mkdir /customlocation/gateway/plugins
mkdir /customlocation/rest-api/plugins
```

!!! note This are example locations, yours can differ. 2. Drop the plugin zip file into the relevant folder(s). 3. Customize the Docker command to provide: \*\* The custom location as a `volume` that overrides the internal `/opt/graviteeio-management-api/plugins-ext` folder. \*\* Two environment variables (`gravitee_plugins_path_0` and `gravitee_plugins_path_1`) that specify both plugin folders (by default only one is used).

```
# APIM REST API
docker run --publish 8083:8083 \
  --volume /customlocation/rest-api/plugins:/opt/graviteeio-management-api/plugins-ext \
  --env gravitee_management_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim" \
  --env gravitee_analytics_elasticsearch_endpoints_0="http://gravitee-elasticsearch:9200" \
  --env gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins \
  --env gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext \
  --name gravitee-apim-rest-api  \
  --detach graviteeio/apim-management-api:latest

# APIM Gateway
docker run --publish 8082:8082 \
  --volume /customlocation/gateway/plugins:/opt/graviteeio-gateway/plugins-ext \
  --env gravitee_management_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim" \
  --env gravitee_ratelimit_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim" \
  --env gravitee_reporters_elasticsearch_endpoints_0="http://gravitee-elasticsearch:9200" \
  --env gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins \
  --env gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext \
  --name gravitee-apim-gateway \
  --detach graviteeio/apim-gateway:latest
```

!!! note This is an example, your ports and URLs may differ.

## Details for Kubernetes installations

!!! note

```
**Option I** is not available for Kubernetes installations as there is no direct access to the inside of the pods.
```

### Option II

1. Provide an URL to the plugin zip file.
2. Modify the `value.yaml` file that you pass in with the Helm chart.

```
api:
  additionalPlugins:
    - https://download.gravitee.io/graviteeio-apim/plugins/policies/gravitee-policy-javascript/gravitee-policy-javascript-1.1.0.zip
    - https://download.gravitee.io/graviteeio-apim/plugins/services/gravitee-kubernetes-controller/gravitee-kubernetes-controller-0.1.0.zip

gateway:
  additionalPlugins:
    - https://download.gravitee.io/graviteeio-apim/plugins/policies/gravitee-policy-javascript/gravitee-policy-javascript-1.1.0.zip
```

!!! note This is an example, your plugins may differ.
