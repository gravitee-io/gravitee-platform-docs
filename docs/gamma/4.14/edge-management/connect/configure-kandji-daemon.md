---
hidden: false
noIndex: false
description: Deploy the Gamma Edge Daemon to your device fleet with Iru (formerly Kandji). Follow the steps to generate the download URL and create the Custom App.
---

# Configure Iru to deploy the Edge Daemon

Deploy the Edge Daemon to your device fleet with Iru (formerly Kandji). The **Daemon deployment** page of Edge Management generates the download link of the daemon and its install script for you, with the gateway addresses and the ID of the environment filled in.

For an overview of the Edge Daemon, see the [Edge Management overview](../get-started/edge-management-overview.md). To create the configuration of the environment first, see [Set up Edge Management](set-up-edge-management.md).

{% hint style="info" %}
**Compatibility.** This page covers macOS devices, on Apple Silicon and Intel. The Edge Daemon supports traffic interception for Claude Code through the Anthropic API.
{% endhint %}

## Prerequisites

Ensure the following are in place before continuing:

* Access to a running Gamma console with Edge Management enabled.
* An Edge Management configuration already created for the environment. See [Set up Edge Management](set-up-edge-management.md).
* An Iru account with admin access to your device fleet.
* Devices that run macOS.
* The gateway-side endpoints reachable from your devices. In particular, the Edge Reactor port, `18093` by default, must be exposed. See [Gateway-side requirements](../get-started/edge-management-overview.md#gateway-side-requirements).

To deploy the Edge Daemon with Iru, complete the following steps:

1. [Open the Daemon deployment page](#open-the-daemon-deployment-page)
2. [Download the daemon](#download-the-daemon)
3. [Create the Kandji Custom App](#create-the-kandji-custom-app)
4. [Verify your deployment](#verify-your-deployment)

## Open the Daemon deployment page

1. In the Gamma console, open **Edge Management**.
2. Click **Daemon deployment**.

<figure><img src="../.gitbook/assets/edge-deploy-kandji.png" alt="The Daemon deployment page with the architecture selector, the download URL, the Kandji Custom App postinstall script with the gateway addresses and the environment ID, and the Diagnostic commands section"><figcaption><p>The Daemon deployment page generates the download URL and the Kandji post-install script.</p></figcaption></figure>

## Download the daemon

1. Click the **macOS** tab.
2. In the menu next to **Download**, select the architecture that matches your devices: **Apple Silicon (arm64)** or **Intel (amd64)**.
3. Click **Download** to fetch the daemon package, or click the link button next to the menu to copy its URL. The version of the daemon shows under the button.

Here is an example of the link for Apple Silicon:

```text
https://download.gravitee.io/graviteeio-ai/gravitee-gamma-edge-daemon/gravitee-gamma-edge-daemon-2.0.0-darwin-arm64.zip
```

## Create the Kandji Custom App

Under **Install script**, the page generates the install command with the Gateway URL, the Reactor URL, and the ID of the environment filled in. With the ID, each daemon gets the configuration of this environment, even from a gateway that serves several environments. Once mTLS is on, on the **Daemon authentication** page, the command also passes the certificate of your fleet and its private key, as files next to `install.sh`. The command runs from the folder where the daemon package is extracted, and looks like the following example:

```bash
sudo ./install.sh \
  --gateway-url 'https://gateway.example.com' \
  --reactor-url 'https://edge-reactor.example.com:18093' \
  --environment-id 'DEFAULT' \
  --client-cert './client.crt' \
  --client-key './client.key' \
  # --reactor-ca './reactor-ca.crt'   # only if the reactor certificate is signed by a private CA
```

For an environment whose ID holds a character other than letters, digits, hyphens, and underscores, the page shows **This environment cannot be installed from a script** instead of the command. It says that the installer accepts only those characters.

To deploy the command, complete the following steps:

1. In the Iru admin console, create a new **Custom App**.
2. Configure the app to extract the daemon package to `/tmp`. The package holds `install.sh` at its root.
3. If mTLS is on, add the certificate of your fleet and its private key to the Custom App zip, next to `install.sh`, as `client.crt` and `client.key`. If your daemons need `--reactor-ca`, add that certificate as `reactor-ca.crt` too, and uncomment the last line of the command. See [Configure daemon authentication](configure-daemon-authentication.md#turn-on-mtls).
4. As the post-install script, enter `cd /tmp` followed by the generated command, unchanged. Iru runs the script as root. For example:

   ```bash
   #!/bin/bash
   set -euo pipefail

   cd /tmp
   sudo ./install.sh \
     --gateway-url 'https://gateway.example.com' \
     --reactor-url 'https://edge-reactor.example.com:18093' \
     --environment-id 'DEFAULT' \
     --client-cert './client.crt' \
     --client-key './client.key' \
     # --reactor-ca './reactor-ca.crt'   # only if the reactor certificate is signed by a private CA

   rm -f /tmp/client.crt /tmp/client.key /tmp/reactor-ca.crt
   ```

   The last line removes the fleet certificate and its private key from `/tmp` once the installer has copied them.
5. Assign the Custom App to the appropriate device blueprints. Iru then distributes and installs the Edge Daemon on all assigned devices.

{% hint style="warning" %}
**Tell your users to open a new terminal.** The installer sets `NODE_EXTRA_CA_CERTS` so that Claude Code trusts the certificate authority of the daemon, and needs no restart for it. Terminals and Claude Code sessions already open when the daemon installs don't get the variable. Ask your users to open a new terminal before they use Claude Code. In a terminal opened before the install, Claude Code reports that it "couldn't reach Anthropic to load your organization's settings".

If the shell profile of a user already exports another `NODE_EXTRA_CA_CERTS`, for example the certificate bundle of a security proxy, a new terminal keeps that value, and Claude Code started from it doesn't trust the daemon either.
{% endhint %}

{% hint style="info" %}
The page also carries collapsible **Diagnostic commands** and **Uninstall** sections, with the commands to check that the daemon runs, to follow its logs, to stop and start it, and to remove it from a device.
{% endhint %}

## Verify your deployment

As your devices receive and start the daemon, they send heartbeats to the Edge Reactor and appear in Edge Management. To verify your deployment, complete the following step:

* Click **Devices** and confirm that your devices report as **Active**. See [Monitor your devices](../observe/monitor-devices.md).

## Next steps

* **Connect AI tools.** Check what, if anything, you have to do on a device. See [Connect Claude Code to the Edge Daemon](../connect-claude-code-to-daemon.md).
* **Watch the traffic.** See [Monitor proxied traffic](../observe/monitor-proxied-traffic.md).
