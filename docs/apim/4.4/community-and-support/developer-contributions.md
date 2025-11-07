---
description: Bootstrap your developer environment
---

# Contributing to the Gravitee API Management development

## Overview

This section explains how to set up your environment to start contributing to Gravitee API Management (APIM) development.

## Prerequisites

You will need the following tools installed on your computer:

* Java (JDK >= 17)
* Maven
* Docker
* NPM (preferably managed with NVM)

## 1. Clone the project and prepare your workspace

Create a `distribution` folder in the `target` folder of each module. These `distribution` folders contain a complete Management API and Gateway distribution (with default plugins) and should be used as the `gravitee.home` environment variable.

1.  Use the following code to clone the project in your workspace:

    ```bash
    git clone https://github.com/gravitee-io/gravitee-api-management
    ```
2.  Build APIM's Management API and Gateway components:

    ```bash
    mvn clean install -T 2C
    ```

{% hint style="info" %}
Use `-Dskip.validation=true` to skip license validation and Prettier checks
{% endhint %}

## 2. Prepare APIM Console UI and Portal UI

1. Run `npm install` from the `gravitee-api-management/gravitee-apim-console-webui` directory
2. Run `npm install` from the `gravitee-api-management/gravitee-apim-portal-webui` directory

{% hint style="info" %}
Use `nvm use` to switch to the appropriate version of NPM to build the UIs
{% endhint %}

## 3. Run prerequisites

Before starting APIM Management API and Gateway, run MongoDB and ElasticSearch, e.g., with Docker.

{% tabs %}
{% tab title="MongoDB" %}
```sh
docker run -p 27017:27017 --name local-mongo -d mongo:3
```
{% endtab %}

{% tab title="ElasticSearch" %}
{% code overflow="wrap" %}
```sh
docker run -d --name local-es7 -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.0
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 4. Run configurations

### APIM Gateway (gravitee-apim-gateway)

{% tabs %}
{% tab title="CLI version" %}
Run `./gravitee` from the `${GRAVITEE_HOME}/bin` directory. `${GRAVITEE_HOME}` refers to the `target/distribution` folder created previously when cloning the project.
{% endtab %}

{% tab title="IntelliJ configuration" %}
By default, the project includes the configuration `Gateway - MongoDB` to run the Gateway.

1. Use classpath of module: `gravitee-apim-gateway-standalone-container`
2. Main class: `io.gravitee.gateway.standalone.GatewayContainer`
3.  In the VM options, change the path to point to your project:&#x20;

    {% code overflow="wrap" %}
    ```bash
    -Dgravitee.home="/home/user/dev/gravitee-api-management/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/target/distribution"
    ```
    {% endcode %}
{% endtab %}
{% endtabs %}

### APIM Management API

{% tabs %}
{% tab title="CLI version" %}
Run `./gravitee` from the `${GRAVITEE_HOME}/bin` directory. `${GRAVITEE_HOME}` refers to the `target/distribution` folder created previously when cloning the project.
{% endtab %}

{% tab title="IntelliJ configuration" %}
By default, the project includes the configuration `Rest API - MongoDB` to run the Rest API.

1. Use classpath of module: `gravitee-apim-rest-api-standalone-container`
2. Main class: `io.gravitee.rest.api.standalone.GraviteeApisContainer`.
3.  In the VM options, change the path to point to your project:&#x20;

    {% code overflow="wrap" %}
    ```bash
    -Dgravitee.home="/home/user/dev/gravitee-api-management/gravitee-apim-rest-api/gravitee-apim-rest-api-standalone/gravitee-apim-rest-api-standalone-distribution/target/distribution"
    ```
    {% endcode %}
{% endtab %}
{% endtabs %}

### APIM Console

{% tabs %}
{% tab title="CLI version" %}
To start the UI, run `npm run serve` from the `gravitee-api-management/gravitee-apim-console-webui` directory.
{% endtab %}

{% tab title="IntelliJ configuration" %}
Create a new Run configuration in IntelliJ:

1. Click **Run → Edit configurations → ✚ → npm**
2. Name it as required
3. Choose **package.json: gravitee-api-management/gravitee-apim-console-webui/package.json**
4. Select **Command: run**
5. Select **Script: serve**

To `npm install`, you can duplicate this configuration and choose **Command > Install**.
{% endtab %}
{% endtabs %}

### APIM Developer Portal

{% tabs %}
{% tab title="CLI version" %}
To start the UI, run `npm run serve` from the `gravitee-api-management/gravitee-apim-portal-webui` directory.
{% endtab %}

{% tab title="IntelliJ configuration" %}
Create a new Run configuration in IntelliJ:

1. Click **Run → Edit configurations → ✚ → npm**
2. Name it as required
3. Choose **package.json: gravitee-api-management/gravitee-apim-portal-webui/package.json**
4. Select **Command: run**
5. Select **Script: serve**

To `npm install`, you can duplicate this configuration and choose **Command > Install**.
{% endtab %}
{% endtabs %}

{% hint style="success" %}
Congratulations, you are now ready to contribute to Gravitee!
{% endhint %}
