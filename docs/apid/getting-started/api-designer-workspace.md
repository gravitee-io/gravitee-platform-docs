---
description: Learn how to use the API Designer Workspace to create an API
---

# API Designer Workspace

Navigating to the API Designer in Gravitee Cloud opens the API Designer Workspace, the administrative interface to the API Designer. Use the workspace to manage existing API designs, create new designs, and configure settings.

<figure><img src="../.gitbook/assets/apid_workspace.png" alt=""><figcaption><p>API Designer Workspace</p></figcaption></figure>

{% hint style="info" %}
The workspace is organization-centric. API designs and settings exist within the context of the selected organization.
{% endhint %}

## Workspace Actions

The workspace menu divides administrative tasks into two sections: API Designs and Settings.

### **API Designs**

Click on API Designs in the left-hand nav to create or manage an API.

**Create an API:** When creating an API, you will be prompted to provide a name and a description. The name will be used as the context path, in accordance with the case rules configured in Settings.

**Manage an API:** The card representing an existing API includes the following icons, which correspond to click, push, export, and info, respectively. Click on an icon to trigger its management functionality.

<div align="left" data-full-width="false">

<figure><img src="../.gitbook/assets/apid-click.png" alt="" width="38"><figcaption></figcaption></figure>

 

<figure><img src="../.gitbook/assets/apid-push.png" alt="" width="32"><figcaption></figcaption></figure>

 

<figure><img src="../.gitbook/assets/apid-export.png" alt="" width="31"><figcaption></figcaption></figure>

 

<figure><img src="../.gitbook/assets/apid-options.png" alt="" width="32"><figcaption></figcaption></figure>

</div>

<table data-header-hidden><thead><tr><th width="119.5">Icon</th><th>Function</th></tr></thead><tbody><tr><td><strong>Click</strong></td><td>Opens the design interface</td></tr><tr><td><strong>Push</strong></td><td>Opens the push interface</td></tr><tr><td><strong>Export</strong></td><td>Exports the API definition</td></tr><tr><td><strong>Info</strong></td><td>Provides options to push, export, or delete the API</td></tr></tbody></table>

### **Settings**

Click on the following Settings options in the left-hand nav to customize API settings.

<table><thead><tr><th width="207.5">Option</th><th>Description</th></tr></thead><tbody><tr><td><strong>Case</strong></td><td>Indicate how case should be applied to paths, objects, and parameters.</td></tr><tr><td><strong>Target Environment</strong></td><td>Select the environment to which the API design will be deployed.</td></tr><tr><td><strong>Legend</strong></td><td>Define the visual cues to distinguish between design attributes.</td></tr></tbody></table>

{% hint style="warning" %}
Only environments linked to active API Management installations will be shown.
{% endhint %}

