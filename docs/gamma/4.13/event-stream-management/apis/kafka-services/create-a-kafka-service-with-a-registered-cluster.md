---
hidden: false
noIndex: false
description: Create a Kafka Service in Event Stream Management with the five-step wizard, bound to bootstrap servers, a registered cluster, or a Virtual Cluster, or import one from a definition. Follow the steps to create one.
---

# Create a Kafka Service with a registered cluster

A Kafka Service is the client-facing Kafka API that Gravitee manages. Kafka clients connect to it with the Kafka protocol, and the Event Gateway applies its plans and policies before it forwards their requests to the Kafka cluster behind it.

This page describes every option of the creation wizard. The binding to a connection of a registered cluster is the **Managed Cluster** mode of the **Endpoint** step. The wizard also binds a Kafka Service to bootstrap servers that you enter, or to a Virtual Cluster.

{% hint style="info" %}
For a simplified walkthrough that covers only the basics, see [Create your first Kafka Service](../../get-started/create-your-first-kafka-service.md).
{% endhint %}

## How Kafka Services work

When you create a Kafka Service, you define the **Listener** that clients connect to, and the **Endpoint binding** that decides how the Kafka Service reaches Kafka. The Event Gateway routes each client connection by its SNI host name, and every produce and consume operation passes through the gateway, where the plans and the policies of the Kafka Service apply.

A Kafka Service can reach several clusters through a Virtual Cluster. Several Kafka Services can also bind to the same cluster, each with its own plans and policies.

## Prerequisites

* Access to a running Gamma console instance, with an environment role that can create APIs.
* For the **Managed Cluster** mode, a registered cluster with connections, deployed. See [Register your Kafka clusters](../../kafka-infrastructure/clusters/register-your-kafka-clusters.md).
* For the **Virtual Cluster** mode, a deployed Virtual Cluster. See [Create a Kafka Service with a Virtual Cluster](create-a-kafka-service-with-a-virtual-cluster.md).
* For the **Standalone** mode, the address of Kafka brokers that the Event Gateway can reach.

## Open the wizard

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click **Create Kafka Service**.

The wizard has five steps:

1. [Identity](#identity)
2. [Listener](#listener)
3. [Endpoint](#endpoint)
4. [Security](#security)
5. [Review](#review)

The button that moves forward names the next step, for example **Next: Listener**. It stays disabled until the current step is complete. **Back** returns to the previous step.

To leave the wizard, click **Cancel**. When you have entered something, the console asks **Discard changes?**. Click **Discard changes** to leave, or **Keep editing** to stay.

### Identity

<table>
    <thead>
        <tr>
            <th width="160">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Name</strong></td>
            <td>Required. Up to 255 characters. Shown in the Kafka Service list and detail views.</td>
        </tr>
        <tr>
            <td><strong>Version</strong></td>
            <td>Required. Pre-filled with <code>1.0</code>.</td>
        </tr>
        <tr>
            <td><strong>Description</strong></td>
            <td>Optional. What the Kafka Service is used for.</td>
        </tr>
    </tbody>
</table>

### Listener

The listener is the address that Kafka clients connect to. Enter the **Host prefix** only. The Event Gateway builds the full bootstrap host name by appending its configured domain, and clients connect on the gateway's SNI port, for example `orders.<gateway-domain>:<sni-port>`. The port is a gateway setting, so the wizard doesn't ask for it.

The host prefix follows these rules:

* It uses lowercase letters, digits, hyphens, and underscores, with dots to separate labels. Each label starts and ends with a letter or a digit, and has at most 63 characters.
* Its first label has at most 49 characters. A longer first label shows **First segment must be less than 50 characters**.
* The whole prefix has at most 241 characters.
* No other API in the environment uses it. Once you stop typing, the console checks the host and shows **Checking host availability…**, then **This host is already in use.** when another API holds it.

A prefix that breaks the format shows **Host is not valid**.

### Endpoint

The **Endpoint binding** step decides how the Kafka Service reaches Kafka. Select one of the three modes:

<table>
    <thead>
        <tr>
            <th width="170">Mode</th>
            <th>Fields</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Standalone</strong></td>
            <td><strong>Bootstrap servers</strong>: required, a comma-separated list of <code>host:port</code> Kafka brokers. A broker without a port uses <code>9092</code>. <strong>Security</strong>: the security protocol of the brokers, and the SASL or SSL settings that the protocol needs. The default protocol is <code>PLAINTEXT</code>.</td>
        </tr>
        <tr>
            <td><strong>Managed Cluster</strong></td>
            <td><strong>Cluster</strong> and <strong>Connection</strong>: both required. Select a registered cluster, then one of its connections. The Kafka Service uses the security settings of the cluster.</td>
        </tr>
        <tr>
            <td><strong>Virtual Cluster</strong></td>
            <td><strong>Virtual Cluster</strong>: required. The Kafka Service uses the backends of the Virtual Cluster. See <a href="create-a-kafka-service-with-a-virtual-cluster.md">Create a Kafka Service with a Virtual Cluster</a>.</td>
        </tr>
    </tbody>
</table>

Only deployed clusters and Virtual Clusters are listed. **Managed Cluster** lists the deployed clusters with connections. **Virtual Cluster** lists the Virtual Clusters in the **Deployed** state, so a Virtual Cluster that is undeployed, or has changes waiting to be deployed, doesn't appear. With none to pick, the step shows **No deployed Clusters. Deploy a Kafka cluster first, then bind to it here.** or **No deployed Virtual Clusters. Deploy a Virtual Cluster first, then bind to it here.**

In the **Standalone** security settings, an SSL truststore or key store set to **None** means that the Kafka Service has no truststore or no key store. A truststore in PEM format needs no password.

### Security

The **Security** step lists the plans that the Kafka Service gets at creation. Plans are optional, and you can add more later from the **Plans** page.

On your first visit, the step adds a **Keyless plan**. A Keyless plan needs no configuration, so it's published as soon as the Kafka Service is created, and clients can connect without credentials right away.

To add a plan, select its type in **Plan type**, then click **Add plan**. The types are **Keyless**, **API key**, **OAuth2**, **JWT**, and **mTLS**. A plan added here is named after its type, for example **API key plan**. Every plan other than Keyless is created in **Staging**, because its security configuration is set on the **Plans** page after creation. Finish it there, then publish it.

The live plans of a Kafka Service all belong to one category: Keyless, mTLS, or authentication (API key, OAuth2, and JWT). Authentication plans of different types can be live together, but a Kafka Service has at most one live Keyless plan. The picker follows these rules:

* While the list holds the Keyless plan, the other types are disabled, because they could never be published next to it. To start with a secured plan, remove the Keyless plan with its delete icon, then add the plan you need.
* **Keyless** leaves the picker once the list holds a Keyless plan.

A plan that conflicts with a plan published at creation shows **Cannot be published while the other plans are live**.

To remove a plan from the list, click its delete icon.

### Review

The **Review & create** step lists the **Name**, **Version**, **Description**, **Listener**, **Binding mode**, **Binding**, and **Plans** of the Kafka Service. Each plan shows the status it gets at creation, **Published** or **Staging**.

1. Check the summary.
2. Optional: Select **Deploy now** to start the Kafka Service on the gateway right after creation. The checkbox is cleared by default. When the environment uses the API review workflow, the step shows **Ask for review** instead. Select it to submit the Kafka Service for review. See [Review a Kafka Service](publish-and-review-a-kafka-service.md).
3. Click **Create Kafka Service**.

The console creates the Kafka Service, creates its plans, then starts it or submits it for review when you selected the option. It confirms with **Kafka Service created** and opens the **Overview** page of the Kafka Service. See [Follow the setup checklist](follow-the-setup-checklist.md).

Without **Deploy now**, the Kafka Service is created stopped.

When the Kafka Service is created but a later step fails, for example a plan or the start, the console shows **Kafka Service created, but not fully set up**, followed by the reason, and opens the Kafka Service. Finish the step from its pages. If the creation itself fails, the wizard shows **Create failed** with the reason, and nothing is created.

## Import a Kafka Service

Instead of the wizard, you can create a Kafka Service from a Gravitee API definition, for example one exported from another environment.

1. On the **Kafka Services** list, click **Import**.
2. In the **Import API Definition** panel, choose the source of the definition:
    * **Local file**. Drop the JSON file on the drop zone, or click it to browse. The console accepts only a v4 definition of a Kafka Service, and shows why when the file doesn't fit.
    * **Remote URL**. Enter the http or https address of the definition in **Definition URL**. The Management API fetches the definition itself, so the address must be reachable from the Management API and allowed by its import allow list.
3. Click **Import**.

The console confirms with **Kafka Service imported** and opens the new Kafka Service. A definition fetched from a URL is checked only once the Management API has created the API. When it holds another type of API, the console warns that it imported that type, not a Kafka Service, and leaves you on the list.

## Verification

To verify that the Kafka Service is created, follow these steps:

1. Open the **Kafka Services** list, and check that the Kafka Service is listed with its listener host and its binding.
2. Open the Kafka Service, and check its **State** and its **Backend binding** on the **Overview** page.

## Next steps

* **Finish the plans**. Configure and publish the plans that you left in **Staging**. See [Manage plans](manage-plans.md).
* **Apply policies**. Add Kafka policies to the flows of the Kafka Service. See [Design flows in the Policy Studio](design-flows-in-the-policy-studio.md).
* **Federate several clusters**. Compose the connections of your registered clusters behind one Virtual Cluster. See [Establish a Virtual Cluster](../../kafka-infrastructure/virtual-clusters/establish-a-virtual-cluster.md).
