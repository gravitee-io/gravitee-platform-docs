---
description: Configuration guide for troubleshooting.
metaLinks:
  alternates:
    - troubleshooting.md
---

# Troubleshooting

<details>

<summary>Nginx cannot open on ports 8084 and 8085</summary>

Sometimes, an SELinux configuration issue can prevent Nginx from opening on ports 8084 and 8085. To correct this issue, complete the following steps:

1.  Validate that the port is not in the list of managed HTTP ports by running `semanage port -l`. You should get the following output:

    ```sh
    $ semanage port -l | grep http_port_t
    http_port_t                tcp      80, 81, 443, 488, 8008, 8009, 8443, 9000
    ```
2.  Add the port for Nginx to bind to, for example, 8084, using the following command:

    ```sh
    $ semanage port -a -t http_port_t  -p tcp 8084
    ```
3.  Validate that the port is listed using the following command:

    \{% code overflow="wrap" %\}

    ```sh
    $ semanage port -l | grep http_port_t
    http_port_t                tcp      8084, 80, 81, 443, 488, 8008, 8009, 8443, 9000

    ```

    \{% endcode %\}4) Restart Nginx.

</details>

<details>

<summary>Ports 8082 to 8085 do not open with a firewall enabled</summary>

If you have a firewall enabled on your Operating System (OS), you must open the APIM port through the firewall.

To open ports 8082 to 8085 through the firewall, use the following command:

```bash
 sudo firewall-cmd --add-port=8082-8085/tcp
```

</details>

<details>

<summary>Port conflict error when saving a Kafka plan</summary>

When configuring port-based routing for a native Kafka API plan, the console validates that the bootstrap port and broker port range do not conflict with other plans in the same environment. If you receive a port conflict error, verify that:

- The bootstrap port is not used by another plan's bootstrap port or broker range.
- The broker range does not overlap with another plan's broker range or bootstrap port.

Port allocations are unique per environment. Plans in different environments may reuse the same ports.

</details>

<details>

<summary>Kafka API deployment fails with port binding error</summary>

A Kafka plan may save successfully in the console but fail to deploy if the configured ports are already bound by another process on the gateway host. The console does not verify OS-level port availability at plan save time.

To resolve this issue:

1. Check which process is using the port by running `sudo lsof -i :<port>` or `sudo netstat -tulpn | grep <port>`.
2. Stop the conflicting process or assign different ports to the Kafka plan.
3. Redeploy the API.

</details>

<details>

<summary>Kafka clients disconnect after changing broker port range</summary>

Modifying the broker range start or broker range end on a deployed Kafka plan reassigns broker slots, which breaks active client connections. Clients automatically reconnect on their next metadata refresh cycle. No client-side configuration change is required.

If clients fail to reconnect:

- Verify that the new broker ports are open on the gateway host and accessible from the client network.
- Check client logs for connection errors or metadata refresh failures.
- Confirm that the gateway has been redeployed with the updated plan configuration.

</details>
