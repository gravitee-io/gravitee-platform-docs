---
description: Overview of Developer Contributions.
---

# Developer Contributions

## Overview

This page explains how to set up your environment to start contributing to AM.

## Prerequisites

You will need the following tools on your computer:

* Java (JDK >= 11)
* Maven
* Docker
* NPM (preferably NVM)

## Download the AM image

Download the latest AM full distribution available: [https://download.gravitee.io/graviteeio-am/distributions/graviteeio-am-full-3.21.0.zip](https://download.gravitee.io/graviteeio-am/distributions/graviteeio-am-full-3.21.0.zip). Unzip it into the directory of your choice. You will need these files later on to copy plugins into your local repository.

## Projects to clone

Clone the following repositories in your workspace

* [https://github.com/gravitee-io/graviteeio-access-management](https://github.com/gravitee-io/graviteeio-access-management)

If you are using IntelliJ, create a new project from existing sources and select your `graviteeio-access-management` folder.

## Prepare for launch

We will run AM Gateway standalone using a **Run configuration** in IntelliJ.

You first need to copy all the plugins in the distribution you downloaded earlier to the `/resources` directory of the standalone project.

For instance if your download is in the `Downloads` folder and your project is in `~/dev/gravitee-am-gateway`, run:

{% code overflow="wrap" %}
```sh
cp ~/Downloads/graviteeio-am-full-3.21.0/graviteeio-am-gateway-3.21.0/plugins/* ~/dev/gravitee-am-gateway/gravitee-am-gateway-standalone/gravitee-am-gateway-standalone-distribution/src/main/resources/plugins
```
{% endcode %}

Repeat the previous step for `gravitee-am-management-rest-api`:

{% code overflow="wrap" %}
```sh
cp ~/Downloads/graviteeio-am-full-3.21.0/graviteeio-am-management-api-3.21.0/plugins/* ~/dev/gravitee-am-management-api/gravitee-am-management-api-standalone/gravitee-am-management-api-standalone-distribution/src/main/resources/plugins
```
{% endcode %}

### Run prerequisites

Before starting the AM Gateway, you need to start Mongo.

* Mongo:

```sh
docker run -p 27017:27017 --name local-mongo -d mongo:3
```

### Run configuration

#### **AM Gateway**

Create a new Run configuration in IntelliJ:

1. Click **Run → Edit configurations → + → Application**.
2. Name it as required.
3. Choose **Use classpath of module**: `gravitee-am-gateway-standalone-container`.
4. Select **Main class**: `io.gravitee.am.gateway.container.GatewayContainer`.
5. In the VM options, add the following (change the path to point to your project):

{% code overflow="wrap" %}
```sh
-Dgravitee.home=/home/user/dev/gravitee-am-gateway/gravitee-am-gateway-standalone/gravitee-am-gateway-standalone-distribution/src/main/resources
```
{% endcode %}

#### **AM API**

Repeat the steps above for `gravitee-management-rest-api`.

#### **AM Console**

Run `npm install` from the `gravitee-am-ui` directory.

Then run `npm run start` to start AM Console.
