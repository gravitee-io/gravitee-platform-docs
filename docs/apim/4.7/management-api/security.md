---
description: Tutorial on security.
---

# Security

## Brute-force attacks

A brute-force attack is the submission of a high volume of authentication requests consisting of password permutations. Even with OAuth 2.0 enabled, you can leave behind a login form for in-memory or local users. Some tools can help you to prevent malicious actions by banning IPs.

## Fail2Ban

This section explains how to secure the APIM UI components (Management and Portal) and APIM APIs against brute-force attacks using Fail2Ban. For instructions on installing Fail2Ban, see the [Fail2Ban website](https://www.fail2ban.org).

### **Configuration**

APIM API logs all authentication failures in the Gravitee log file. Follow the steps below to configure Fail2Ban to work with the Gravitee log file.

{% hint style="info" %}
Each time you modify Fail2Ban configuration resources, you need to restart the service.
{% endhint %}

1.  Configure a Fail2Ban filter to extract Gravitee authentication failure events:

    ```
    2019-05-03 16:03:03.304 [gravitee-listener-31] WARN  i.g.m.s.l.AuthenticationFailureListener - Authentication failed event for : admin - IP : 10.50.24.18
    ```
2.  Add a configuration file to declare filters: `/etc/fail2ban/filter.d/gravitee.conf`.

    ```
    [Definition]
    failregex = .*Authentication failed event for.*IP : <HOST>
    ignoreregex =
    ```
3.  Add Fail2Ban actions to `gravitee.conf`. Actions are `iptables` or `firewalld` commands.

    ```
    [INCLUDES]

    before = iptables-common.conf

    [Definition]

    # Option:  actionstart
    # Notes.:  command executed once at the start of Fail2Ban.
    # Values:  CMD
    #
    actionstart = <iptables> -N f2b-<name>
                  <iptables> -A f2b-<name> -j <returntype>
                  <iptables> -I <chain> -p <protocol> --dport <port> -j f2b-<name>

    # Option:  actionstop
    # Notes.:  command executed once at the end of Fail2Ban
    # Values:  CMD
    #
    actionstop = <iptables> -D <chain> -p <protocol> --dport <port> -j f2b-<name>
                 <iptables> -F f2b-<name>
                 <iptables> -X f2b-<name>

    # Option:  actioncheck
    # Notes.:  command executed once before each actionban command
    # Values:  CMD
    #
    actioncheck = <iptables> -n -L <chain> | grep -q 'f2b-<name>[ \t]'

    # Option:  actionban
    # Notes.:  command executed when banning an IP. Take care that the
    #          command is executed with Fail2Ban user rights.
    # Tags:    See jail.conf(5) man page
    # Values:  CMD
    #
    actionban = <iptables> -I f2b-<name> 1 -p tcp -m string --algo bm --string 'X-Forwarded-For: <ip>' -j DROP

    # Option:  actionunban
    # Notes.:  command executed when unbanning an IP. Take care that the
    #          command is executed with Fail2Ban user rights.
    # Tags:    See jail.conf(5) man page
    # Values:  CMD
    #
    actionunban = <iptables> -D f2b-<name> -p tcp -m string --algo bm --string 'X-Forwarded-For: <ip>' -j DROP

    [Init]
    ```
4.  Declare the new Gravitee Fail2Ban block in the main configuration file with the required parameters:

    ```
    [gravitee]
    banaction = gravitee
    logpath = /opt/gravitee-io-management-api/logs/management_api.log
    filter = gravitee
    enabled = true
    maxretry = 3
    ```
