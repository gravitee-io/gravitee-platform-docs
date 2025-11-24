---
description: Overview of Jetbrains.
noIndex: true
---

# Jetbrains

## Telepresence plugin for Jetbrains IDEs

The Telepresence plugin allows you to create your intercepts using a GUI, and integrate it with your workflow.

### Installation

{% hint style="warning" %}
You need a CLI using 2.16 or higher, in its proprietary version.
{% endhint %}

You need to have the Telepresence command line installed on your machine. If that's not the case, [please proceed first](../../install-telepresence/install.md).

You can install the plugin directly from the [Jetbrains marketplace](https://plugins.jetbrains.com/search?search=telepresence), or from your IDE menu in **Settings > Plugins**.

Look for Telepresence, and click **Install**.

### Intercept your service

Start by opening the Telepresence tool menu:

<figure><img src="../../.gitbook/assets/00 tp 16.png" alt=""><figcaption></figcaption></figure>

Then you can select the context / namespace you want to connect to, and connect by using a right click:

<div align="left"><figure><img src="../../.gitbook/assets/00 tp 17.png" alt="" width="344"><figcaption></figcaption></figure></div>

If Telepresence wasn't running, it will open a terminal asking for your password.

<figure><img src="../../.gitbook/assets/00 tp 18.png" alt=""><figcaption></figcaption></figure>

### Run your application

Telepresence is also integrated with the Runner function of the IDE.

To properly run in your cluster context, your code needs to be populated with the environment variables & volumes in use in the cluster. To achieve that, the plugin adds a tab in your language's runner to select the intercept to extract the environment variables from.

* Tick the checkbox to enable it, and specify the name of the intercept to use as a source.
* Start the runner, and the environment variables used by the real pod in your cluster should be available to your program.

<figure><img src="../../.gitbook/assets/00 tp 19.png" alt=""><figcaption></figcaption></figure>

### Settings

#### Alternate Telepresence installation

If the plugin can't find your command line installation path, you can define another one in the IDE settings. Look for Telepresence, and select the binary you want to use.

<figure><img src="../../.gitbook/assets/00 tp 20.png" alt=""><figcaption></figcaption></figure>

Then click apply to save your changes.
