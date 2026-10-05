---
hidden: false
noIndex: false
description: Change the listener host prefix that Kafka clients connect to on a Kafka Service in Event Stream Management, and find its bootstrap server. Follow the steps to edit the entrypoint.
---

# Configure the entrypoint

The entrypoint of a Kafka Service is its Kafka listener, the address that Kafka clients connect to. The Event Gateway routes each client connection by its SNI host name, so the only setting of the listener is its **Host prefix**. The gateway builds the full bootstrap host name by appending its configured domain, and clients connect on the gateway's SNI port.

## Open the entrypoint

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Design** group of the Kafka Service sidebar, click **Entrypoint**.

The **Entrypoint** card shows the **Host prefix** and the **Bootstrap servers** of the Kafka Service. **Bootstrap servers** lists the addresses that the gateway resolved for the listener, each with a copy button. Until the gateway can resolve them, it reads **Available once the Kafka Service is deployed**.

Without permission to change the Kafka Service, the card shows the host prefix and the bootstrap servers read-only.

## Change the host prefix

1. In **Host prefix**, enter the new prefix. Enter only the prefix, for example `orders`.
2. At the bottom of the page, click **Save changes**.

The host prefix follows these rules:

* It uses lowercase letters, digits, hyphens, and underscores, with dots to separate labels. Each label starts and ends with a letter or a digit, and has at most 63 characters.
* Its first label has at most 49 characters.
* The whole prefix has at most 241 characters.
* No other API in the environment uses it. Once you stop typing, the console checks the host and shows **Checking host availability…**, then **This host is already in use.** when another API holds it.

When the prefix breaks a rule, or the check is still running, **Save changes** shows **Fix the errors to save** with the reason, for example **Host is not valid** or **Still checking host availability.**, and moves to the field.

The console saves the listener and confirms with **Kafka Service updated**. When the save fails, the bar shows **Couldn't save** with the reason, and **Save changes** becomes **Try again**.

The new host reaches the gateway at the next deployment, and until then the Kafka Service shows **Out of sync**. Once it's deployed, Kafka clients connect with the bootstrap server built from the new prefix. To deploy, click **Deploy** in the page header.

To drop your change instead, click **Discard**. If you leave the page with an unsaved change, the console asks **Leave without saving?**.

## Verification

To verify the entrypoint, follow these steps:

1. Reload the **Entrypoint** page, and check that **Host prefix** shows the prefix you saved.
2. Deploy the Kafka Service, then check that **Bootstrap servers** shows an address built from the new prefix.
