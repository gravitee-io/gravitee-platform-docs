---
description: Overview of Alerts.
---

# Alerts

## Overview

You can put in place a system of alerting to warn of any unusual and potentially dangerous events on the Gravitee Access Management (AM) authorization server that may be of interest to administrators or monitoring services.

AM integrates with the Alert Engine product, a notification system to deliver messages using channels such as SMTP, Webhooks or [Slack](https://slack.com/).

Out of the box, some pre-defined alerts and notification systems (known as notifiers) are available to help you get started.

### Alert Engine

AM’s system of alerts and notifications is based on the Gravitee Alert Engine product.

{% hint style="info" %}
Alert Engine is a standalone module that needs to be configured and deployed before use. For more information, see the AE installation documentation.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/ae/howitworks/overview.png" alt=""><figcaption><p>Alert Engine diagram</p></figcaption></figure>
