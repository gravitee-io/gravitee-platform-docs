---
description: How to build and deploy your own plugins
---

# Custom Plugins

## Overview

Gravitee API Management (APIM) plugins are additional components that can be _plugged into_ the Gravitee ecosystem. You can use plugins to extend and customize the behavior of Gravitee to meet your strategic needs.

APIM includes a default set of plugins with each distribution. You can also obtain and [deploy](custom-plugins.md#deployment) some additional Gravitee-maintained and third-party plugins from the plugin marketplace.

## Common structure

This section describes how to create your own custom plugins. Each plugin follows the following common structure:

```
-----------------
.
├── pom.xml
├── README.md
└── src
    ├── assembly
    │   └── <plugin>-assembly.xml
    ├── main
    │   ├── java
    │   │   └── <main java files>
    │   └── resources
    │       └── plugin.properties
    └── test
        └── java
            └── <test java files>
-----------------
```

The different key files are as follows:

| File                   | Description                                       |
| ---------------------- | ------------------------------------------------- |
| pom.xml                | The main Maven POM file                           |
| README.md              | The main entry point for the plugin documentation |
| \<plugin>-assembly.xml | The common Maven assembly descriptor              |
| plugin.properties      | The plugin descriptor file                        |

### `pom.xml`

Any plugins (and more generally any Gravitee projects) are [Maven](https://maven.apache.org/) managed. A plugin project is described by using the Maven [Project Object Model](https://maven.apache.org/pom.html) file.

### `README.md`

Each plugin should have a dedicated `README.md` file to document it. The `README.md` file should contain everything related to the use of your plugin: _What is its functionality? How can you use it? How can you configure it?_

### `<plugin>-assembly.xml`

In order to be plugged into the Gravitee ecosystem, a plugin needs to be deployed following a given file structure. The `<plugin>-assembly.xml` file is the [Maven Assembly](http://maven.apache.org/plugins/maven-assembly-plugin/) descriptor used to build the distribution file.

Commonly, a plugin distribution file is organized as follows:

```
-----------------
.
├── <main Jar file>.jar
└── lib
-----------------
```

The different files are as follows:

| File                 | Description                                                                          |
| -------------------- | ------------------------------------------------------------------------------------ |
| \<main Jar file>.jar | The plugin’s main Jar file                                                           |
| lib/                 | <p>A directory containing external libraries to correctly execute the</p><p>.jar</p> |

#### **`.jar`**

Each plugin has its main `.jar` file containing the business behavior _plus_ the[ plugin descriptor file](custom-plugins.md#plugin.properties).

#### **`lib/`**

This directory contains all the plugin's external dependencies (non-provided-scope Maven dependencies).

### `plugin.properties`

The `plugin.properties` file is the descriptor of the plugin. It acts as the _ID Card_ of the plugin and will be read by APIM Gateway during the plugin loading process.

The following parameters are included in the descriptor:

| Parameter   | Description                               |
| ----------- | ----------------------------------------- |
| id          | The plugin identifier                     |
| name        | The plugin name                           |
| version     | The plugin version                        |
| description | The plugin description                    |
| class       | The main plugin class                     |
| type        | The type of plugin (_policy_, _reporter_) |

{% hint style="warning" %}
The plugin identifier has to be unique to be correctly loaded by the APIM Gateway.
{% endhint %}

## Deployment, discovery, and loading

Head over to [the main plugins documentation](docs/apim/4.0/overview/plugins.md#deployment) to learn how to deploy your custom plugin.
