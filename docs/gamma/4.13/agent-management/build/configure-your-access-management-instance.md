---
hidden: false
noIndex: false
description: Connect the Agent Management module to a Gravitee Access Management instance and select an AM domain so you can register agent identities.
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
| **SPIFFE**                            | The SPIFFE credential option for Workload Agents, so an agent can authenticate with a JWT-SVID.                                                        |
| **Service account + access token**    | An AM service account with rights to manage applications across the environments and domains you target. The module authenticates to AM with this token. |

{% hint style="info" %}
An administrator enables these on the AM domain in Gravitee Access Management.
{% endhint %}

## Configure the connection

To configure the connection, complete the following steps:

1. [Connect to Access Management](#connect-to-access-management)
2. [Select the scope](#select-the-scope)
3. [Save](#save)

### Connect to Access Management

This connection is configured in **Platform Management**. Open its **Access Management** settings and, in the **Gravitee Access Management connection** panel, provide the following:

| Field                                   | Description                                                               |
| --------------------------------------- | ------------------------------------------------------------------------- |
| **Gravitee Access Management base URL** | The base URL of your AM instance, **without** a `/management` suffix. The module appends `/management` itself. For example, if AM's management API is at `http://localhost:8093/management`, enter `http://localhost:8093`. |
| **Access Management organization**      | The organization this connection belongs to. Defaults to `DEFAULT`.       |
| **Service-account access token**        | The bearer token issued by AM for the service account. Encrypted at rest. Once saved, the field shows a masked placeholder—leave it blank to keep the stored token. |

Select **Verify & Load**. A successful check verifies the credentials and loads the environments and domains AM exposes, so you can choose a scope in the next step. If it fails, the status message shows the error returned by AM.

{% hint style="warning" %}
Enter the base URL without `/management`. Including it produces a request to `/management/management/…`, which AM answers with `HTTP 404 Not Found`. The status message reports only the 404, so this misconfiguration looks like a bad token or an unreachable host.

If the module runs in a container, the URL must be resolvable **from that container**, not from your browser. A `localhost` address that works in your address bar does not resolve inside the module's container.
{% endhint %}

### Select the scope

Once the connection is verified, choose where agents are created:

1. **Environment**—select the AM environment. If there's only one, it's selected automatically.
2. **Domain**—select the AM domain. The picker searches AM server-side, so you can find domains beyond the first page by typing.
3. **Gateway discovered**—a read-only field showing the gateway entrypoint the module found for the selected domain. If several are found, pick one; if none is found, the module falls back to the management URL.

{% hint style="warning" %}
If **Verify & Load** succeeds but the **Environment** list is empty, the service account authenticated but isn't authorized to enumerate environments and domains. Grant it a role with those rights in AM under **Organization** → **Administrative roles**, and then select **Verify & Load** again. The module reports this as a successful connection with no environments rather than as a permissions error.
{% endhint %}

### Save

Select **Save** to store the connection and scope. The module is now ready to register agents against the selected domain.

There's no capability check on this screen. To confirm which of the capabilities in [Prerequisites on the AM domain](#prerequisites-on-the-am-domain) are enabled, check the domain's settings in Gravitee Access Management. A capability that isn't enabled doesn't block you from saving the connection or from registering agents—it only makes the matching option unavailable in the agent wizard.

## Troubleshooting

* **`HTTP 404 Not Found` from Verify & Load.** Usually the base URL, not the token. The module appends `/management` to whatever you enter, so a URL that already ends in `/management` resolves to `/management/management/…`. Remove the suffix. If the module runs in a container, also confirm the host is resolvable from inside that container.
* **Verify & Load succeeds but the Environment list is empty.** The service account is authenticated but not authorized. Grant it a role that can enumerate environments and domains under **Organization** → **Administrative roles** in AM, and then select **Verify & Load** again.
* **"Gravitee Access Management is not configured" banner.** No connection has been saved yet, or AM is unreachable. The module returns `am_not_configured` when AM can't be reached. Save a working connection, and then retry.
* **AM upstream errors.** When AM returns a 4xx/5xx, the module surfaces the original status and message. Check that the service-account token is valid and has sufficient permissions.

## Next steps

* [Create an agent identity](create-an-agent-identity.md). Register your first agent against the connected domain.
