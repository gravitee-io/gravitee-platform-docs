---
noIndex: true
---

# Upgrade or Migrate to a Newer Version

## Upgrading Ambassador Edge Stack

{% hint style="warning" %}
Read the instructions below before making any changes to your cluster!
{% endhint %}

There are currently multiple paths for upgrading Ambassador Edge Stack, depending on what version you're currently running, what you want to be running, and whether you installed Ambassador Edge Stack using [Helm or YAML](../).

(To check out if you installed Ambassador Edge Stack using Helm, run `helm list --all-namespaces` and see if Ambassador Edge Stack is listed. If so, you installed using Helm.)

{% hint style="warning" %}
Read the instructions below before making any changes to your cluster!
{% endhint %}

### If you are currently running Emissary-ingress

See the instructions on updating Emissary-ingress.

### If you installed Ambassador Edge Stack using Helm

| If you're running.                    | You can upgrade to           |
| ------------------------------------- | ---------------------------- |
| Ambassador Edge Stack 3.11.X          | Ambassador Edge Stack 3.12.8 |
| Ambassador Edge Stack 2.5.1           | Ambassador Edge Stack 3.12.8 |
| Ambassador Edge Stack 2.4.X           | Ambassador Edge Stack 2.5.1  |
| Ambassador Edge Stack 2.0.X           | Ambassador Edge Stack 2.5.1  |
| Ambassador Edge Stack 1.14.4          | Ambassador Edge Stack 2.5.1  |
| Ambassador Edge Stack prior to 1.14.4 | Ambassador Edge Stack 1.14.4 |
| Emissary-ingress 3.9.1                | Ambassador Edge Stack 3.12.6 |

### If you installed Ambassador Edge Stack manually by applying YAML

| If you're running.                    | You can upgrade to           |
| ------------------------------------- | ---------------------------- |
| Ambassador Edge Stack 3.11.X          | Ambassador Edge Stack 3.12.8 |
| Ambassador Edge Stack 2.5.1           | Ambassador Edge Stack 3.12.8 |
| Ambassador Edge Stack 2.4.X           | Ambassador Edge Stack 2.5.1  |
| Ambassador Edge Stack 2.0.X           | Ambassador Edge Stack 2.5.1  |
| Ambassador Edge Stack 1.14.4          | Ambassador Edge Stack 2.5.1  |
| Ambassador Edge Stack prior to 1.14.4 | Ambassador Edge Stack 1.14.4 |
| Emissary-ingress 3.9.1                | Ambassador Edge Stack 3.12.6 |
