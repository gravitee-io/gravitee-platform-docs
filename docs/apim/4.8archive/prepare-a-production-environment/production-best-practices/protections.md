# Protections

## Brute-force protection

A brute-force attack is the submission of a high volume of authentication requests consisting of password permutations. Even with OAuth 2.0 enabled, you can leave behind a login form for in-memory or local users. Some tools can help you to prevent malicious actions by banning IPs. This section explains how to secure the APIM UI components (Management and Portal) and APIM APIs against brute-force attacks.&#x20;

### ReCaptcha

Ensure that ReCaptcha is configured to protect forms against bots and brute-force attempts:

```yaml
# Allows to enable or disable recaptcha (see https://developers.google.com/recaptcha/docs/v3). Currently, it only affect the user registration route.
reCaptcha:
  enabled: true
  siteKey: <your_site_key>
  secretKey: <your_secret_key>
  minScore: 0.5
  serviceUrl: https://www.google.com/recaptcha/api/siteverify
```

Gravitee relies on [ReCaptcha V3](https://developers.google.com/recaptcha/docs/v3?hl=en), which is non-intrusive for the end user. You can obtain your site key and secret key directly from your Google developer account ([https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)).

### Fail2Ban

If your platform is particularly exposed to the outside world, we recommend adding additional protection against pure brute-force attacks by setting up Fail2Ban. For instructions on installing Fail2Ban, see the [Fail2Ban website](https://www.fail2ban.org).

Fail2Ban scans log files and automatically bans IPs that show malicious signs, e.g., too many password failures, seeking an opportunity for exploitation, etc.&#x20;

#### **Configuration**

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

## Browser protection

### Enable CSRF protection

Cross-site request forgery (CSRF) is a web security vulnerability that allows an attacker to induce users to perform actions that they do not intend to perform. You can protect your end users by checking that the CSRF protection is enabled (enabled by default):

```yaml
http: 
  csrf:
    # Allows to enable or disable the CSRF protection. Enabled by default.
    enabled: true
```

We strongly recommend **NEVER** disabling CSRF protection unless you are absolutely sure of what you are doing and that your users may be exposed to [Cross Site Request Forgery attacks](https://fr.wikipedia.org/wiki/Cross-site_request_forgery).

### Configure CORS

CORS is one of the most important things to set up to protect your users and your system against malicious attackers. It allows the user's browser to enable native protection preventing unauthorized websites to perform a JavaScript HTTP call to the Console or REST API. Basically, when well-configured, you only allow your own Console website (e.g., `https://gio-console.mycompany.com`) and Dev Portal website (e.g., `https://gio-portal.mycompany.com`) to make calls from a browser to their respective APIs.

Make sure CORS is well-configured for both the Console AND the Portal APIs:

```yaml
http:
  api:
    management:
      cors:
        allow-origin: 'https://gio-console.mycompany.com'
    portal:
      cors:
        allow-origin: 'https://gio-portal.mycompany.com'
```

`allow-origin: '*'` should be considered a security risk because it permits all cross-origin requests. **We highly recommend fine-tuning the allow-origin setting. Refer to** the [Gravitee documentation](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/internal-api#cors-configuration) for other useful information related to CORS.
