---
description: >-
  This article walks through how to configure your Alert Engine and Access
  Management integration
---

# Configuration

## Introduction

Gravitee Access Management (AM) comes with an intuitive and easy to use Alert Engine integration.

AM provides a pre-defined and pre-configured list of alerts that only have to be enabled or disabled. This can be done via the Management API and Gateway config settings.

* Management API:

```
alerts:
  alert-engine:
    enabled: true
    ws:
      discovery: true
      endpoints:
        - http://localhost:8072/
      security:
        username: admin
        password: adminadmin
  risk_assessment:
  # You need the Risk Assessment Service plugin for these alerts
    geoVelocity:
      name: Geo velocity alert
      description: A geo velocity risk-based alert has been triggered
      assessments: LOW # Default is LOW
      severity: WARNING
    ipReputation:
      name: IP reputation alert
      description: An IP reputation risk-based alert has been triggered
      assessments: LOW # Default is LOW
      severity: WARNING
    unknownDevices:
      name: Unknown Device alert
      description: An unknown device risk-based alert has been triggered
      assessments: HIGH # Default is HIGH
      severity: WARNING
   too_many_login_failures:
    name: "Too many login failures detected"
    description: "More than {threshold}% of logins are in failure over the last {window} second(s)"
    # the threshold rate in % to reach before notify. Default 10% of login failures.
    threshold: 10
    # the minimum sample size. Default 1000 login attempts.
    sampleSize: 1000
    # window time in seconds. Default 600s (10 minutes).
    window: 600
    # severity of the alert (INFO, WARNING, CRITICAL). Default WARNING.
    severity: WARNING
```

* Gateway

```
alerts:
  alert-engine:
    enabled: true
    ws:
      discovery: true
      endpoints:
        - http://localhost:8072/
      security:
        username: admin
        password: adminadmin
  risk_assessment:
    settings:
      enabled: true # default is false
      devices:
        enabled: true # default is true
        thresholds:
          HIGH: 1 # Arbitrary value
      ipReputation:
        enabled: true # default is true
        thresholds:
          #Default is only LOW, but you can add more thresholds
          #percentage
          LOW: 1
          MEDIUM: 30
          HIGH: 70
      geoVelocity:
        enabled: true # default is true
        thresholds:
          # meters per second, default is 0.2777778 (1km/h)
          LOW: 0.2777778
          MEDIUM: 6.9444445 # (25km/h)
          HIGH: 69.444445 # (250km/h)
```

These snippets give you a glimpse of how you can finely configure your alerts. You can find more information in the [Access Management "Manage alerts" documentation](/am/guides/alerts/manage-alerts).

{% hint style="info" %}
**Using the `.yaml` file**

If you want to change some advanced settings, you can still update the relevant section of the `gravitee.yml` file.
{% endhint %}
