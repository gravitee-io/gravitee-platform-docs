---
hidden: false
noIndex: false
description: Connect the Agent Management module to a Gravitee Access Management instance, select an AM domain, and check readiness so you can register agent identities.
---

# Configure your Access Management instance

The Agent Management module uses Gravitee Access Management (AM) as its identity backend: every agent identity you register is an OAuth client created in an AM domain. Before you can register agents, you connect the module to an AM instance and point it at a domain.

You configure this connection **once per organization**. The connection—including the service-account token, which is encrypted at rest—is stored by the module and reused for every agent.

## Prerequisites on the AM domain

The connection targets a single AM domain. Anything not enabled makes the matching option unavailable in the agent wizard. For example, if CIMD isn't enabled, the **CIMD** client-identifier option is grayed out. For the full set of agent-identity features, that domain needs the following capabilities enabled:

| Capability                            | What it unlocks                                                                                                                                          |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dynamic Client Registration (DCR)** | Lets the module register agents as OAuth clients at all. Required.                                                                                       |
| **Client template application**       | A template application whose settings AM clones onto each registered client. Required for CIMD.                                                          |
| **CIMD**                              | The CIMD client-identifier option in the agent wizard, so an agent can be identified by a metadata-document URL.                                         |
| **SPIFFE**                            | The SPIFFE credential option for Autonomous agents, so an agent can authenticate with a JWT-SVID.                                                        |
| **Service account + access token**    | An AM service account with rights to manage applications across the environments and domains you target. The module authenticates to AM with this token. |

{% hint style="info" %}
An administrator enables these on the AM domain in Gravitee Access Management. The readiness check tells you which capabilities are present on the domain you've selected.
{% endhint %}

## Configure the connection

To configure the connection, complete the following steps:

1. [Connect to Access Management](#connect-to-access-management)
2. [Select the scope](#select-the-scope)
3. [Check readiness](#check-readiness)
4. [Save](#save)

### Connect to Access Management

This connection is configured in **Platform Management**. Open its **Access Management** settings and, in the **Gravitee Access Management connection** panel, provide the following:

| Field                                   | Description                                                               |
| --------------------------------------- | ------------------------------------------------------------------------- |
| **Gravitee Access Management base URL** | The AM management API base URL, for example `http://localhost:8093`.      |
| **Access Management organization**      | The organization this connection belongs to. Defaults to `DEFAULT`.       |
| **Service-account access token**        | The bearer token issued by AM for the service account. Encrypted at rest. |

Select **Verify & Load**. A successful check verifies the credentials and loads the environments and domains AM exposes, so you can choose a scope in the next step. If it fails, the status message shows the error returned by AM.

### Select the scope

Once the connection is verified, choose where agents are created:

1. **Environment**—select the AM environment. If there's only one, it's selected automatically.
2. **Domain**—select the AM domain. The picker searches AM server-side, so you can find domains beyond the first page by typing.
3. **Gateway entrypoint**—the module discovers the gateway entrypoints for the selected domain. If exactly one is found, it's used automatically; if several are found, pick one. If none is found, the module falls back to the management URL.

### Check readiness

Select **Check readiness** to confirm the selected domain has the capabilities the module relies on. Each of the following probes reports **ok**, **fail**, or **skipped**:

| Probe                           | Checks                                                   |
| ------------------------------- | -------------------------------------------------------- |
| **Connection**                  | The module can reach AM with the configured credentials. |
| **Domain**                      | The selected domain is reachable.                        |
| **Dynamic Client Registration** | DCR is enabled on the domain.                            |
| **CIMD**                        | CIMD is enabled on the domain.                           |
| **CIBA**                        | CIBA is enabled on the domain.                           |
| **SPIFFE**                      | SPIFFE workload identity is enabled on the domain.       |

When a probe fails, its row includes an **Open in Gravitee Access Management** link that deep-links to the relevant AM settings so you can enable the missing capability.

{% hint style="info" %}
The readiness check reports on **CIBA** for completeness, but it isn't required by the agent identity flows in this guide. A failed CIBA probe doesn't stop you from registering agents.
{% endhint %}

{% hint style="info" %}
A failed CIMD or SPIFFE probe doesn't block you from registering agents. It only means those specific identifier or credential options aren't available in the wizard until you enable them on the domain.
{% endhint %}

### Save

Select **Save** to store the connection and scope. The module is now ready to register agents against the selected domain.

## Troubleshooting

* **"Gravitee Access Management is not configured" banner.** No connection has been saved yet, or AM is unreachable. The module returns `am_not_configured` when AM can't be reached. Save a working connection, and then retry.
* **AM upstream errors.** When AM returns a 4xx/5xx, the module surfaces the original status and message. Check that the service-account token is valid and has sufficient permissions.

## Next steps

* [Create an agent identity](create-an-agent-identity.md). Register your first agent against the connected domain.
