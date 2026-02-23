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
