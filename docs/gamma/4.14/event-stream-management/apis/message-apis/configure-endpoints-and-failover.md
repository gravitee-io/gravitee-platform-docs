---
hidden: false
noIndex: false
description: Configure the endpoint groups and endpoints that a Message API produces to and consumes from in Event Stream Management, their load balancing and tenants, and failover for failed calls. Follow the steps to change them.
---

# Configure endpoints and failover

The endpoints of a Message API are the backends that it produces to and consumes from, such as a Kafka cluster or an MQTT broker. Endpoints sit in endpoint groups: a group holds the connector, the load balancing algorithm, and the connection settings that its endpoints share, and each endpoint holds its own settings. Failover retries a failed call to the backend and stops calling a backend that keeps failing.

## Open the endpoints

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Design** group of the Message API sidebar, click **Endpoints**.

<figure><img src="../../.gitbook/assets/gamma-esm-message-api-endpoints.png" alt="The Endpoints page of a Message API, with its default Kafka group, its connector, load balancing, and Default badges, and the table of its endpoints"><figcaption><p>The Endpoints page of a Message API</p></figcaption></figure>

The **Endpoints** card lists the endpoint groups. Each group shows its name, its connector, its load balancing algorithm, and a table of its endpoints with their **Name**, **Weight**, and, when set, **Tenants**. The endpoints of a Kafka group also show their **Bootstrap servers**.

The first group carries the **Default** badge: the Message API uses it to produce and consume. The other groups serve, for example, as the dead letter queue of an entrypoint. See [Configure entrypoints](configure-entrypoints.md#send-failed-messages-to-a-dead-letter-queue).

Without permission to change the Message API's definition, or when the Gravitee Kubernetes Operator manages the Message API, the page is read-only. Each group then offers **View**, and each endpoint a view icon, which open the forms with every field disabled. See [Manage general settings](manage-general-settings.md#kubernetes-managed-message-apis).

Every change on this page is saved as soon as you confirm it, and the console confirms with **API updated**. When a save fails, the card shows **Save failed** with the reason, and the form keeps your input. A change reaches the gateway at the next deployment, and until then the Message API shows **Out of sync**. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

## Add an endpoint group

1. Click **Add endpoint group**.
2. Under **Endpoint group type**, select a connector, for example **Kafka**, **MQTT 5.x**, **Solace**, **RabbitMQ**, or **Mock**. The cards cover only the connectors that support the quality of service of every entrypoint of the Message API.
3. In **Group name**, keep the proposed name, `Default <connector> group`, or enter another one.
4. In **Load balancing algorithm**, select **Round robin**, **Random**, **Weighted round robin**, or **Weighted random**. The default is **Round robin**.
5. Complete the `<connector> connection` form, which the endpoints of the group inherit, and the **Endpoint configuration** form of the first endpoint. A **Mock** group has neither form, and shows **Configuration is disabled for Mock endpoint groups.**
6. Click **Create endpoint group**. The button stays disabled while a required field is empty or invalid.

The new group goes to the bottom of the list, with one endpoint named `Default <connector>`. **Back to list** leaves the form without saving.

A group name and an endpoint name are required, can't contain `:`, and must be unique across the groups and the endpoints of the Message API: **Names must be unique across groups and endpoints.** When the proposed name is taken, the console adds a number to it, for example `Default Kafka group-2`.

For **Kafka**, the connection form shows only the producer settings, the consumer settings, or both, depending on what the entrypoints of the Message API need. An entrypoint that receives messages from clients, such as **HTTP POST**, needs a producer. An entrypoint that delivers messages to clients, such as **HTTP GET**, **Server-Sent Events**, or **Webhook**, needs a consumer.

When the security protocol of a Kafka connection is **Protocol SSL** or **Protocol SASL_SSL**, **SSL configuration** includes **Verify Host**. It makes the gateway check that the broker hostname matches its certificate, and it's enabled by default. Disable it only if you trust the network.

## Connect a Kafka group to a registered cluster

A Kafka endpoint group takes its connection from one of two places: **Direct**, the default, uses the bootstrap servers and the security that you enter in the group. **Registered cluster** uses the connections of a Cluster registered in Event Stream Management, which hold the bootstrap servers and the security. See [Register your Kafka clusters](../../kafka-infrastructure/clusters/register-your-kafka-clusters.md).

1. Click **Add endpoint group**.
2. Under **Endpoint group type**, select **Kafka**.
3. Select **Registered cluster**.
4. In **Cluster**, select a Cluster.
5. In **Default connection**, select one of its connections.
6. Complete the other settings of the connection form. With **Registered cluster**, the form has no security settings: they come from the connection.
7. Click **Create endpoint group**.

<figure><img src="../../.gitbook/assets/gamma-esm-message-api-registered-cluster-group.png" alt="The form of a Kafka endpoint group with Registered cluster selected instead of Direct, the Orders Kafka Cluster, the orders-producer Default connection, and the Kafka connection form below them"><figcaption><p>A Kafka endpoint group in Registered cluster mode</p></figcaption></figure>

The first endpoint of the new group uses the default connection. To connect an existing Kafka group, click its **Edit** button, follow steps 3 to 6, then click **Save group**.

The **Cluster** list offers the deployed Clusters that you're a member of, directly or through a group that has access to the Cluster, and every deployed Cluster to an organization administrator. When it has none to offer, the form shows **No deployed Clusters. Deploy a Kafka cluster first, then bind to it here.** or **You are not a member of any deployed Cluster. Ask an owner of a Cluster to add you as a member, then bind to it here.** See [Manage cluster permissions](../../kafka-infrastructure/clusters/manage-cluster-permissions.md).

The connections offered are those of the Cluster as it was last deployed. After you add a connection to a Cluster, deploy the Cluster to offer it here.

A connection that Message APIs can't use shows **(not supported)** after its name, and can't be selected. Its tooltip gives the reason, for example:

* The security protocol is `SASL_PLAINTEXT` or `SASL_SSL`, without a SASL mechanism or with `NONE`.
* The SASL mechanism is `DELEGATE_TO_BROKER`. A Message API has no client credentials to pass on to the brokers.
* The SSL settings trust every certificate instead of using a truststore.
* The PEM key store is given by a path instead of the content of the key and the certificate.

### Choose the connection of each endpoint

Each endpoint of the group uses one connection of the Cluster. A new endpoint gets the default connection of its group. To give an endpoint another connection, follow these steps:

1. Click the edit icon of the endpoint.
2. In **Connection**, select a connection.
3. Click **Save endpoint**.

An endpoint can also use another Cluster, or **Direct**. On the **Group shared configuration** tab of the endpoint, clear **Inherit configuration from the endpoint group**, then choose **Direct** or **Registered cluster**, the **Cluster**, and the **Default connection** of its **Connection override**.

When you switch a group between **Direct** and **Registered cluster**, or change its **Cluster** or its **Default connection**, the endpoints that inherit its configuration follow it, and the form names them with the connection that they'll use. When you switch the group to **Direct**, the form asks for the endpoint configuration that they'll use instead, with its bootstrap servers. An endpoint with its own connection override keeps it.

In the list of endpoints, the **Bootstrap servers** column of the group becomes **Connection**, and shows the name of the Cluster and the name of the connection of each endpoint that uses one. When the endpoints of a group use different connections, the group warns that the same traffic can then reach different brokers and authenticate as different Kafka principals.

<figure><img src="../../.gitbook/assets/gamma-esm-message-api-cluster-endpoints.png" alt="The Endpoints page of a Message API whose Kafka group uses a registered Cluster, with the warning that its endpoints use different cluster connections and the Connection column showing Orders Kafka and the connection of each endpoint"><figcaption><p>The endpoints of a group connected to a registered cluster</p></figcaption></figure>

The form checks each Cluster and connection that you pick against the Cluster as it was last deployed. A connection that the deployed Cluster no longer has, or that Message APIs can't use, shows the reason under the field, and the form doesn't save until you pick another one.

When the Message API already uses a Cluster that you're not a member of, the form keeps that Cluster, shows **You are not a member of the Cluster \<name\>**, and offers only the connections that the Message API already uses. To use another connection of that Cluster, ask an owner of the Cluster to add you as a member.

### Start and update a Message API that uses a Cluster

A Message API that uses a Cluster follows the changes that you deploy on the Cluster, such as new credentials, without a new deployment of the Message API. New requests use the changes right away. When the deployment changes the connection that an endpoint uses, the connections opened before it keep working for a short time, then close.

The Message API doesn't start, and its deployment is refused, while its Cluster isn't deployed, the deployed Cluster doesn't have the connection of an endpoint, or Message APIs can't use that connection. The console shows the reason in a notification. The Message API stays editable. See [Manage clusters](../../kafka-infrastructure/clusters/manage-a-cluster.md).

## Manage the groups

* To change a group, click its **Edit** button. Change **Group name**, **Load balancing algorithm**, or the `<connector> connection` form, then click **Save group**.
* To reorder the groups, click the up and down arrows of a group. The group at the top becomes the **Default** group.
* To delete a group, click its delete icon, then click **Delete** in the **Delete endpoint group?** dialog. A Message API keeps at least one endpoint group, so the delete icon is disabled while only one remains, and shows **A Message API needs at least one endpoint group.**

When **Enable failover** is selected on the **Failover** page, each Kafka group shows **Failover is enabled but it is not supported for Kafka endpoints. Use the native Kafka failover by providing multiple bootstrap servers.**

### Groups used as a dead letter queue

An entrypoint can send the messages that it fails to push to a group or to an endpoint of this page. The page keeps the entrypoints in step:

* Renaming a group or an endpoint that serves as a dead letter queue updates the entrypoints that use it. The form says so under the name.
* Deleting it disables the dead letter queue of those entrypoints. The delete dialog names them.
* The default group isn't meant to serve as a dead letter queue. When it does, for example after a reorder, the card says so and names the entrypoints concerned. Move another group to the top, or pick another dead letter queue on the **Entrypoints** page.

## Manage the endpoints of a group

* To add an endpoint, click **Add endpoint** under the group, configure it, then click **Add endpoint**.
* To change an endpoint, click its edit icon, change the fields, then click **Save endpoint**.
* To reorder the endpoints, click the up and down arrows of an endpoint.
* To delete an endpoint, click its delete icon, then click **Delete** in the **Delete endpoint?** dialog. While the Message API has a single group, its last endpoint can't be deleted, and the delete icon shows **At least one endpoint is required.**

### Configure an endpoint

An endpoint has the following fields:

<table>
    <thead>
        <tr>
            <th width="220">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Endpoint name</strong></td>
            <td>Required. A new endpoint is named <code>&lt;group name&gt; endpoint</code>.</td>
        </tr>
        <tr>
            <td><strong>Endpoint configuration</strong></td>
            <td>The settings of the endpoint itself, built from the connector. A <strong>Mock</strong> endpoint doesn't have it.</td>
        </tr>
        <tr>
            <td><strong>Weight</strong></td>
            <td>Required. A whole number of 1 or more, used by the <strong>Weighted round robin</strong> and <strong>Weighted random</strong> algorithms. The default is 1.</td>
        </tr>
        <tr>
            <td><strong>Tenants</strong></td>
            <td>Optional. A gateway that runs with one of the selected tenants uses this endpoint. Leave it empty to make the endpoint available to every gateway.</td>
        </tr>
        <tr>
            <td><strong>Inherit configuration from the endpoint group</strong></td>
            <td>Selected for a new endpoint: the endpoint uses the connection settings of its group. Clear it to show the <strong>Connection override</strong> form, prefilled with the connection settings of the group, and change them for this endpoint only. The checkbox appears for the connectors that have group connection settings.</td>
        </tr>
    </tbody>
</table>

## Configure failover

<figure><img src="../../.gitbook/assets/gamma-esm-message-api-failover.png" alt="The Failover page of a Message API with a Kafka endpoint, with Enable failover cleared, the note that failover is not supported for Kafka endpoints, and the Max retries, Force next endpoint on failure, and Failure condition fields"><figcaption><p>The failover settings of a Message API</p></figcaption></figure>

1. In the **Design** group of the Message API sidebar, click **Failover**.
2. Select **Enable failover**. The other fields become editable.
3. Complete the following fields. A field that the Message API doesn't set shows its default value.

<table>
    <thead>
        <tr>
            <th width="220">Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Force next endpoint on failure</strong></td>
            <td>Retries a failed call on the next endpoint of the group, instead of the endpoint that the load balancer picks. The first attempt always uses the load balancer. Cleared by default.</td>
        </tr>
        <tr>
            <td><strong>Max retries</strong></td>
            <td>How many times the gateway retries a failed call to the backend before it fails the request. 0 or more. The default is 2.</td>
        </tr>
        <tr>
            <td><strong>Failure condition</strong></td>
            <td>Optional. An expression, for example <code>{#response.status >= 500}</code>. A response that matches it counts as a failure.</td>
        </tr>
        <tr>
            <td><strong>Slow call duration (ms)</strong></td>
            <td>How long each attempt to reach the backend can run before the gateway abandons it and retries. A call that takes longer than this in total, retries included, counts as slow. 50 or more. The default is 2000. Configure the endpoints with timeouts greater than this duration.</td>
        </tr>
        <tr>
            <td><strong>Open state duration (ms)</strong></td>
            <td>How long the circuit breaker stays open before the gateway tries the backend again with a single call. 500 or more. The default is 10000.</td>
        </tr>
        <tr>
            <td><strong>Max failures</strong></td>
            <td>How many recent calls the circuit breaker weighs. When that many calls have all failed, or have all run slow, the circuit breaker opens, and the gateway stops calling the backend. 1 or more. The default is 5.</td>
        </tr>
        <tr>
            <td><strong>Per subscription</strong></td>
            <td>Keeps a separate circuit breaker for each subscription instead of one for the whole Message API. Selected by default.</td>
        </tr>
    </tbody>
</table>

4. In the save bar at the bottom of the page, click **Save changes**.
5. If **Per subscription** is cleared, the **Use a global circuit breaker?** dialog warns that one circuit breaker is shared by every consumer. Click **Yes, update it**.

While the circuit breaker is open, the gateway answers `502`. A number field that is empty, not a whole number, or under its minimum shows **A whole number is required.** or **Must be <minimum> or more.**, and **Save changes** doesn't save until you fix it.

When the Message API has a Kafka endpoint group, the page shows **Failover is not supported for Kafka endpoints. Use the native Kafka failover by providing multiple bootstrap servers.**

The console confirms with **API updated**. Like the endpoints, failover reaches the gateway at the next deployment.

Clearing **Enable failover** keeps the other values, so they're back the next time you select it.

Without permission to change the Message API's definition, or when the Gravitee Kubernetes Operator manages the Message API, the **Failover** page is read-only.

## Verification

To verify that the endpoints and failover are saved, follow these steps:

1. Reload the **Endpoints** page, and check that each endpoint group lists the endpoints you expect, with their weight and tenants.
2. Click **Edit** on a group, and check that the connection form shows the settings you entered.
3. For a group connected to a registered cluster, check that the **Connection** column shows the Cluster and the connection of each endpoint.
4. Open **Failover**, and check that **Enable failover** and the values you entered are still set.
5. Check that the header of the Message API sidebar shows **Out of sync** until you deploy.
