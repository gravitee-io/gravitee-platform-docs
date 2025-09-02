# VPN Configurations

To enhance security, Kubernetes API server endpoints are often configured to be accessible only through a VPN. In these setups, you must first connect to your VPN before using Blackbird cluster (powered by Telepresence) to access your cluster. However, because Blackbird relies on similar underlying technologies, conflicts can occur.

Typically, there are two types of routes to your machine:

* **Public VPN route**: Overrides your default route, meaning it makes sure that packets you send out to the public internet go through a private tunnel instead of your ethernet or Wi-Fi adapter.
* **Private VPN route**: Allows your local machine to access hosts inside the VPN that aren't accessible to the public internet. This is the more limited route that will connect your machine only to reachable hosts on the private network, such as your Kubernetes API server.

A Kubernetes cluster assigns IP addresses to pods and services. This is a key element of Kubernetes networking, because it allows applications on the cluster to reach each other. When Blackbird connects you to the cluster, it tries to connect you to the IP addresses that your cluster assigns to services and pods. When creating a cluster, administrators can configure Classless Inter-Domain Routing (CIDR) ranges where the Kubernetes cluster will place resources.

Use this guide to identify and resolve potential VPN-related issues.

## Conflicts

When you run `blackbird cluster connect` to connect to a cluster, Blackbird talks to the API server to determine which pod and service CIDRs it needs to map in your local machine. If it detects that these CIDR ranges are already mapped by a VPN's `private route`, it will produce an error and inform you of the conflicting subnets:

```console
$ blackbird cluster connect
blackbird cluster connect: error: connector.Connect: failed to connect to root daemon: rpc error: code = Unknown desc = subnet 10.43.0.0/16 overlaps with existing route "10.0.0.0/8 via 10.0.0.0 dev utun4, gw 10.0.0.1"
```

Blackbird offers three ways to resolve this issue:

* [Allow the conflict](vpn-configurations.md#allowing-the-conflict) in a controlled manner.
* [Avoid the conflict](vpn-configurations.md#avoiding-the-conflict) using the `--proxy-via` connect flag.
* [Use Docker](vpn-configurations.md#using-docker) to make Blackbird run in a container with its own network config.

### Allowing the conflict

Evaluate your network layout, and then configure Blackbird to override conflicting subnets. By default, Blackbird avoids mapping these subnets to prevent making certain VPN-hosted resources unreachable. However, you (or your network administrator) have the best understanding of how hosts are distributed within your VPN.

Even if your private route covers the entire 10.0.0.0/8 range, hosts may only exist within a specific subset of that space. For example, if all VPN hosts reside within 10.0.0.0/9 and new hosts will only be assigned IPs from this range, you can safely override the unused portion (10.128.0.0/9) where services and pods exist.

To enable this, configure the `client.routing.allowConflicingSubnets` flag in the Telepresence Helm chart. You can do this using the following command.

```console
$ blackbird cluster helm upgrade --set client.routing.allowConflictingSubnets="{10.128.0.0/9}"
```

You can also be more specific and only allow the CIDRs that you know are used by the cluster.

```console
$ blackbird cluster helm upgrade --set client.routing.allowConflictingSubnets="{10.130.0.0/16,10.132.0.0/16}"
```

### Avoiding the conflict

If you don't want to allow the conflict, remap the cluster's CIDRs to virtual CIDRs on your workstation by passing a `--proxy-via` flag to `blackbird cluster connect`.

The `blackbird cluster connect` flag `--proxy-via` allows the local DNS server to translate cluster subnets to virtual subnets on your workstation, and the virtual network interface (VIF) to provide the reverse translation. The following is the syntax for the flag, which can be repeated:

```console
$ blackbird cluster connect --proxy-via CIDR=WORKLOAD
```

Cluster DNS responses matching CIDR to virtual IPs are routed (with reverse translation) using WORKLOAD. The CIDR can also be a symbolic name that identifies a subnet or list of subnets.

| Symbol    | Meaning                                |
| --------- | -------------------------------------- |
| `also`    | All subnets added with `--also-proxy`. |
| `service` | The cluster's service subnet.          |
| `pods`    | The cluster's pod subnets.             |
| `all`     | All of the above.                      |

The WORKLOAD is the deployment, replicaset, statefulset, or argo-rollout in the cluster whose agent will be used for targeting the routed subnets.

This is particularly useful in two scenarios:

1. The cluster's subnets overlap with those available on the workstation, which is a common issue when using a VPN. This is especially true if the VPN has a board subnet range due to a small subnet mask. To resolve this conflict, you can use the `--proxy-via` flag. Instead of allowing the conflict to occur, this flag gives Blackbird precedence, effectively hiding the conflicting subnets. By rerouting the cluster's subnet, `--proxy-via` prevents the overlap and ensures smooth connectivity.
2. The cluster's DNS is configured with domains that resolve to loopback addresses (e.g., when the cluster uses a mesh configured to listen to a loopback address and then reroutes from there). A loopback address isn't useful on the client, but the `--proxy-via` flag can reroute the loopback address to a virtual IP that the client can use.

Subnet proxying is done by the client's DNS resolver, which translates the IPs returned by the cluster's DNS resolver to a virtual IP (VIP) to use on the client. Blackbird's VIF will detect when the VIP is used and translate it back to the loopback address on the pod.

#### Proxy-via and using IP-addresses directly

If the service is using IP addresses instead of domain names when connecting to other cluster resources, then these connections will fail when running locally. The `--proxy-via` flag relies on the local DNS server to translate the cluster's DNS responses, so the IP of an `A` or `AAAA` response is replaced with a virtual IP from the configured subnet. If connections are made using an IP instead of a domain-name, then the lookup is made. Blackbird has no way of detecting the direct use of IP addresses.

#### Virtual IP configuration

Blackbird will use a special subnet when it generates the virtual IPs that are used locally. On a Linux or macOS workstation, this subnet will be a class E subnet (not normally used for any other purposes). On Windows, the class E subnet isn't routed, and Blackbird will instead default to `211.55.48.0/20`. The default can be changed using the following configuration: `cluster.virtualIPSubnet`.

#### Example

For example, there's a conflict between the cluster's subnets, where all subnets are covered by the CIDR `10.124.0.0/9` and a VPN using `10.0.0.0/9`. You can avoid the conflict using:

```console
$ blackbird cluster connect --proxy-via all=echo
```

The cluster's subnets are now hidden behind a virtual subnet.

### Using docker

You can use `blackbird cluster connect --docker` to make the Blackbird daemon containerized, which means that it has its own network configuration and therefore no conflict with a VPN.
