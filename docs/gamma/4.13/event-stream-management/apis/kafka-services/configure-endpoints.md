---
hidden: false
noIndex: false
description: Change how a Kafka Service in Event Stream Management reaches Kafka, with endpoint groups bound to bootstrap servers, a registered cluster, or a Virtual Cluster, and pin endpoints to gateway tenants. Follow the steps to change them.
---

# Configure endpoints

The endpoints of a Kafka Service decide how the Event Gateway reaches Kafka. Endpoints sit in endpoint groups. Each group has one binding mode, **Standalone**, **Managed Cluster**, or **Virtual Cluster**, and holds one or more endpoints of that mode. The wizard creates one group, `default-group`, with one endpoint, `default`.

## How the gateway picks an endpoint

The gateway connects through the first endpoint group only, the one marked **Default**. In that group, it uses the first endpoint that serves its tenant:

* An endpoint with no tenant serves every gateway.
* An endpoint with tenants serves only the gateways that run with one of those tenants.

The other groups stay in the definition without carrying traffic. To switch the Kafka Service to another group, for example to a disaster-recovery cluster, move that group to the top of the list and deploy the Kafka Service.

## Open the endpoints

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Design** group of the Kafka Service sidebar, click **Endpoints**.

The **Endpoints** card lists the endpoint groups. Each group shows its name, its binding mode, and its endpoints. Each endpoint shows its name, its connection, for example the bootstrap servers or the identifier of the cluster, and its **Tenants**, or **All gateways** when it has none.

Without permission to change the Kafka Service, the list is read-only.

Every change on this page is saved as soon as you confirm it, and the console confirms with **Kafka Service updated**. When a save fails, the console shows **The endpoints could not be saved.**, followed by the reason, or by **Try again.** when the Management API gives none. A change reaches the gateway at the next deployment, and until then the Kafka Service shows **Out of sync**. To deploy, click **Deploy** in the page header.

## Add an endpoint group

1. Click **Add endpoint group**.
2. In **Group name**, keep the proposed name or enter another one.
3. Select the binding mode of the group: **Standalone**, **Managed Cluster**, or **Virtual Cluster**. The mode of a group can't change later.
4. Configure the first endpoint of the group. See [Configure an endpoint](#configure-an-endpoint).
5. Click **Add group**.

The new group goes to the bottom of the list. **Back to list** leaves the form without saving.

## Manage the groups

* To rename a group, click its **Edit** button, change **Group name**, then click **Save group**.
* To reorder the groups, click the up and down arrows of a group. The group at the top is the **Default** group that the gateway uses.
* To delete a group, click its delete icon, then click **Delete** in the **Delete endpoint group?** dialog. A Kafka Service keeps at least one endpoint group, so the delete icon is disabled while only one remains.

## Manage the endpoints of a group

* To add an endpoint, click **Add endpoint** under the group, configure it, then click **Add endpoint**.
* To change an endpoint, click its edit icon, change the fields, then click **Save endpoint**.
* To reorder the endpoints, click the up and down arrows of an endpoint. The gateway uses the first endpoint that serves its tenant.
* To delete an endpoint, click its delete icon, then click **Delete** in the **Delete endpoint?** dialog. A group keeps at least one endpoint, so the delete icon is disabled while only one remains.

## Configure an endpoint

Each endpoint has an **Endpoint name**, the fields of the binding mode of its group, and its **Tenants**.

<table>
    <thead>
        <tr>
            <th width="170">Binding mode</th>
            <th>Fields</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Standalone</strong></td>
            <td><strong>Bootstrap servers</strong>: required, a comma-separated list of <code>host:port</code> Kafka brokers. A broker without a port uses <code>9092</code>. <strong>Security</strong>: the security protocol of the brokers, and the SASL or SSL settings that the protocol needs.</td>
        </tr>
        <tr>
            <td><strong>Managed Cluster</strong></td>
            <td><strong>Cluster</strong> and <strong>Connection</strong>: both required. Only deployed registered clusters with connections are listed. The endpoint uses the security settings of the cluster.</td>
        </tr>
        <tr>
            <td><strong>Virtual Cluster</strong></td>
            <td><strong>Virtual Cluster</strong>: required. Only Virtual Clusters in the <strong>Deployed</strong> state are listed, plus the Virtual Cluster that the endpoint already uses.</td>
        </tr>
    </tbody>
</table>

The names of the groups and of the endpoints are required, and each must be unique across all the groups and endpoints of the Kafka Service. A name that is already used shows **Names must be unique across groups and endpoints.**

**Tenants** is optional. Select the tenants of the gateways that use the endpoint, or leave it empty so that every gateway can use it.

### Security of a Standalone endpoint

The **Security** settings of a **Standalone** endpoint use the same form as a registered cluster:

* Select the security protocol, for example `PLAINTEXT`, `SASL_PLAINTEXT`, `SASL_SSL`, or `SSL`, then complete the SASL or SSL settings that appear.
* An SSL truststore or key store set to **None** means that the endpoint has no truststore or no key store.
* A truststore in PEM format, given by its path or its content, needs no password.

## Verification

To verify the endpoints, follow these steps:

1. Reload the **Endpoints** page, and check that the group you want the gateway to use is at the top, marked **Default**.
2. Check that each endpoint shows the connection and the tenants you expect.
3. Deploy the Kafka Service, and check that the header of the Kafka Service sidebar shows **Deployed**.
