### Deploying a Cluster

To deploy Alert Engine in cluster mode, configure Hazelcast for production by editing the `hazelcast.xml` file:

1. Disable multicast discovery by setting `<multicast enabled="false"/>`.
2. Enable TCP-IP discovery by setting `<tcp-ip enabled="true">`.
3. Add `<member>` entries for each node's IP address or hostname.
4. Set the `LICENCE_KEY_PATH` environment variable to the absolute path of your license file.
5. Start the Alert Engine nodes with the cluster configuration.

Each node logs its role (PRIMARY or REPLICA) and cluster size at startup. Monitor logs for `MembershipEvent` messages to confirm nodes join successfully.

**Example log messages:**

```
INFO  c.g.a.c.hz.HazelcastClusterManager - Local node [[172.25.0.2]:5701] role is PRIMARY (cluster size: 1)
INFO  c.g.a.c.hz.HazelcastClusterManager - A node has joined the cluster: MembershipEvent {...}
INFO  c.g.a.c.hz.HazelcastClusterManager - Local node [[172.25.0.2]:5701] role is PRIMARY (cluster size: 2)
INFO  c.g.a.c.hz.HazelcastClusterManager - Local node [[172.25.0.3]:5701] role is REPLICA (cluster size: 2)
```

These messages appear at node startup and when nodes join or leave the cluster.

### Configuring Hazelcast Discovery

For production clusters, replace multicast discovery with TCP-IP by editing the Hazelcast configuration file. Set the cluster name to `graviteeio-ae` and list all node IP addresses or hostnames in `<tcp-ip>` member entries.

**Example TCP-IP configuration:**

```xml
<network>
    <join>
        <multicast enabled="false"/>
        <tcp-ip enabled="true">
            <member>192.168.1.10</member>
            <member>192.168.1.11</member>
            <member>192.168.1.12</member>
        </tcp-ip>
    </join>
</network>
```

The default configuration uses multicast, which works for nodes on the same network but is not recommended for production.

### Node Health Check

Alert Engine nodes expose a health check endpoint at `http://admin:adminadmin@localhost:18072/_node`. The health check runs with the following parameters:

* **Interval:** 20s
* **Timeout:** 10s
* **Retries:** 3
