---
description: Bootstrap your developer environment
---

# Developer Contributions

This section explains how to set up your environment to start contributing to Gravitee API Management (APIM) development.

## Prerequisites

You will need the following tools installed on your computer:

* Java (JDK >= 17)
* Maven
* Docker
* NPM (preferably managed with NVM)

## Clone the project and prepare your workspace

Use the following code to clone the project in your workspace:

```sh
git clone https://github.com/gravitee-io/gravitee-api-management
```

Next, build APIM's Management API and Gateway components:

```sh
mvn clean install -T 2C
```

{% hint style="info" %}
You can use \`-Dskip.validation=true\` to skip license validation and prettier checks.
{% endhint %}

This command will create a `distribution` folder in the `target` folder of each module. These folders contain a full distribution of Management API and Gateway, with default plugins. These `distribution` folders should be used as the `gravitee.home` environment variable

## Prepare APIM Console UI and Portal UI

Run `npm install` from the `gravitee-api-management/gravitee-apim-console-webui` and `gravitee-api-management/gravitee-apim-portal-webui` directories.

{% hint style="info" %}
You can use \`nvm use\` to switch to the appropriate version of npm to build the UIs.
{% endhint %}

## Run Prerequisites

Before starting APIM Management API and Gateway, you need to start MongoDB and ElasticSearch. You can, for instance, use docker.

#### MongoDB

```sh
docker run -p 27017:27017 --name local-mongo -d mongo:3
```

#### ElasticSearch

{% code overflow="wrap" %}
```sh
docker run -d --name local-es7 -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.0
```
{% endcode %}

## Run Configuration

### APIM Gateway (gravitee-apim-gateway)

#### **CLI Version**

Run `./gravitee` from the `${GRAVITEE_HOME}/bin` directory. `${GRAVITEE_HOME}` refers to the `target/distribution` folder created previously when cloning the project.

#### **IntelliJ configuration**

The project includes by default the configuration `Gateway - MongoDB` to run the Gateway.

It contains by default the following configuration:

1. **Use classpath of module**: `gravitee-apim-gateway-standalone-container`.
2. **Main class**: `io.gravitee.gateway.standalone.GatewayContainer`.
3. In the VM options, add the following (change the path to point to your project):

{% code overflow="wrap" %}
```
-Dgravitee.home="/home/user/dev/gravitee-api-management/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/target/distribution"
```
{% endcode %}

### APIM Management API

#### **CLI Version**

Run `./gravitee` from the `${GRAVITEE_HOME}/bin` directory. `${GRAVITEE_HOME}` refers to the `target/distribution` folder created previously when cloning the project.

#### **IntelliJ configuration**

The project includes by default the configuration `Rest API - MongoDB` to run the Rest API.

It contains by default the following configuration:

1. **Use classpath of module**: `gravitee-apim-rest-api-standalone-container`.
2. **Main class**: `io.gravitee.rest.api.standalone.GraviteeApisContainer`.
3. In the VM options, add the following (change the path to point to your project):

{% code overflow="wrap" %}
```
-Dgravitee.home="/home/user/dev/gravitee-api-management/gravitee-apim-rest-api/gravitee-apim-rest-api-standalone/gravitee-apim-rest-api-standalone-distribution/target/distribution"
```
{% endcode %}

### APIM Console

#### **CLI Version**

Run `npm run serve` from the `gravitee-api-management/gravitee-apim-console-webui` directory to start the UI.

#### **IntelliJ configuration**

Create a new Run configuration in IntelliJ:

1. Click **Run → Edit configurations → ✚ → npm**.
2. Name it as required.
3. Choose **package.json: gravitee-api-management/gravitee-apim-console-webui/package.json**.
4. Select **Command: run**.
5. Select **Script: serve**.

To `npm install`, you can duplicate this configuration and choose **Command > Install**.

### APIM Developer Portal

#### **CLI Version**

Run `npm run serve` from the `gravitee-api-management/gravitee-apim-portal-webui` directory to start the UI.

#### **IntelliJ Configuration**

Create a new Run configuration in IntelliJ:

1. Click **Run → Edit configurations → ✚ → npm**.
2. Name it as required.
3. Choose **package.json: gravitee-api-management/gravitee-apim-portal-webui/package.json**.
4. Select **Command: run**.
5. Select **Script: serve**.

To `npm install`, you can duplicate this configuration and choose **Command > Install**.

{% hint style="success" %}
Congratulations, you are now ready to contribute to Gravitee!
{% endhint %}
