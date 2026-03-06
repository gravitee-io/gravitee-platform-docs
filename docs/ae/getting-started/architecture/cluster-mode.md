### Cluster Node Roles

The Alert Engine cluster uses automatic leader election to designate one node as PRIMARY. The PRIMARY node processes all incoming events. If the primary node fails, another node is automatically elected to take over.

The oldest member in the Hazelcast cluster member list is always elected as the PRIMARY node. All other nodes remain on standby as REPLICA nodes.

### Failover Behavior

When the PRIMARY node fails or leaves the cluster, Hazelcast automatically elects a new PRIMARY node from the remaining cluster members. The new PRIMARY node resumes event processing without manual intervention.
