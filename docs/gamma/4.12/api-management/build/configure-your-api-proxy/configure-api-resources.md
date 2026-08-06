---
description: >-
  Create API-level resources, such as caches and OAuth providers, that policies
  reference at runtime.
hidden: false
noIndex: false
---

# Configure API resources

The **Resources** page creates and manages resources that the policies of this API use at runtime. Resources such as caches, OAuth providers, and authentication adapters hold shared connection details, so each policy references the resource instead of embedding its own configuration.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Resources** in the API proxy sidebar.

Managing resources requires the `api-definition-u` permission.

<!-- TODO: Screenshot of the Resources page with configured resources -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-resources-page.png" alt=""><figcaption><p>The Resources page</p></figcaption></figure>

{% hint style="info" %}
When the API proxy is managed by the Kubernetes operator, resources are read-only.
{% endhint %}

Once resources exist, the page shows the **Total resources** and **API-level** counters, and a locked **Environment references** counter marked **Coming soon**. The resource table lists each resource's **Resource**, **Type**, and **Status** columns, and a search field filters the list.

## Add a resource

To add a resource, follow these steps:

1. Click **Add Resource**.
2. In the **Select Resource Type** step, select a resource type. The available types are the resource plugins installed on your platform.
3. Click **Next**.
4. Enter a **Resource name**. Names are unique per API.
5. Complete the **Configuration** form. The fields depend on the selected resource type.
6. In the **Review & Create** step, confirm the resource details.

## Manage existing resources

The actions menu of each resource row offers the following actions:

* **Edit**. Update the configuration of the resource.
* **Disable** or **Enable**. Toggle the resource. The **Status** column shows **Enabled** or **Disabled**.
* **Remove**. Delete the resource from the API.

{% hint style="warning" %}
Removing a resource breaks the policies that reference it. The **Remove resource** dialog warns that policies referencing the resource will fail until they're updated.
{% endhint %}

## Verification

To verify a resource is working as expected, follow these steps:

1. Add a resource and leave it enabled.
2. Reference the resource by name from a policy that supports it, for example a cache policy or an OAuth2 validation policy.
3. Deploy the API and send a request that triggers the policy. The policy uses the resource configuration at runtime.

<!-- TODO: Screenshot of a policy referencing the resource by name -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-resources-policy-ref.png" alt=""><figcaption><p>A policy referencing an API resource</p></figcaption></figure>
