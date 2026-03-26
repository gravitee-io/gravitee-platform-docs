---
description: Learn how to build and deploy your own plugins
---

# Custom Plugins

## Overview

Gravitee API Management (APIM) plugins extend and customize component behavior to meet your strategic needs. Each APIM distribution includes a default set of plugins. You can also [deploy](custom-plugins.md#deployment) additional Gravitee-maintained and third-party plugins from the plugin marketplace.

## Common structure

Plugins follow a common structure:

```bash
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

Below are the different key files:

<table><thead><tr><th width="264">File</th><th>Description</th></tr></thead><tbody><tr><td><code>pom.xml</code></td><td>The main Maven POM file</td></tr><tr><td><code>README.md</code></td><td>The main entry point for the plugin documentation</td></tr><tr><td><code>&#x3C;plugin>-assembly.xml</code></td><td>The common Maven assembly descriptor</td></tr><tr><td><code>plugin.properties</code></td><td>The plugin descriptor file</td></tr></tbody></table>

{% tabs %}
{% tab title="pom.xml" %}
Gravitee projects are [Maven](https://maven.apache.org/)-managed. A plugin project is described via the Maven [Project Object Model](https://maven.apache.org/pom.html) file.
{% endtab %}

{% tab title="README.md" %}
Each plugin should by documented by a dedicated `README.md` file that contains comprehensive information related to the use of your plugin.
{% endtab %}

{% tab title="<plugin>-assembly.xml" %}
To integrate with the Gravitee ecosystem, a plugin needs to be deployed with a given file structure. The `<plugin>-assembly.xml` file is the [Maven Assembly](http://maven.apache.org/plugins/maven-assembly-plugin/) descriptor used to build the distribution file, which has the following structure:

```bash
-----------------
.
├── <main Jar file>.jar
└── lib
-----------------
```

The different files/folders are described below:

<table><thead><tr><th width="244">File</th><th>Description</th></tr></thead><tbody><tr><td><code>&#x3C;main Jar file>.jar</code></td><td>The plugin’s main Jar file</td></tr><tr><td><code>lib/</code></td><td>A directory containing external libraries to correctly execute the .jar</td></tr></tbody></table>

{% tabs %}
{% tab title=".jar" %}
The main `.jar` file of each plugin contains information on the business behavior and the[ plugin descriptor file](custom-plugins.md#plugin.properties).
{% endtab %}

{% tab title="lib/" %}
This directory contains all of the plugin's external dependencies (non-provided-scope Maven dependencies).
{% endtab %}
{% endtabs %}
{% endtab %}

{% tab title="plugin.properties" %}
The `plugin.properties` file is the plugin descriptor, which acts as an ID card and is read by APIM Gateway during the plugin loading process. The descriptor includes the following parameters:

| Parameter   | Description                                 |
| ----------- | ------------------------------------------- |
| id          | The plugin identifier                       |
| name        | The plugin name                             |
| version     | The plugin version                          |
| description | The plugin description                      |
| class       | The main plugin class                       |
| type        | The type of plugin (e.g., policy, reporter) |

{% hint style="warning" %}
The plugin identifier must be unique for the APIM Gateway to load it correctly
{% endhint %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
See [this page](deploying-plugins.md#deployment) to learn how to deploy your custom plugin
{% endhint %}
