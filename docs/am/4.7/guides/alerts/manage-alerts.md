# Manage Alerts

## Overview

AM comes with some pre-defined alerts to notify you of suspicious end-user activity.

To manage alerts:

1. [Log in to AM Console](docs/am/4.7/getting-started/tutorial-getting-started-with-am/login-to-am-console.md).
2. Click **Settings > Alerts**.
3. Switch on **Enable Alerts**.
4. Enable the alerts you are interested in.

## Alert types

The following table lists the available alert types.

| Type                        | Key                            | Description                                                                       |
| --------------------------- | ------------------------------ | --------------------------------------------------------------------------------- |
| Too many login failures     | too\_many\_login\_failures     | Alert when the number of login failures is abnormally high.                       |
| Risk-based alerts           | risk\_assessment               | Alert when the user behaviour seems suspicious.                                   |
| Too many reset passwords    | too\_many\_reset\_password     | (not implemented) Alert when the number of reset passwords is abnormally high.    |
| Too many locked out users   | too\_many\_locked\_users       | (not implemented) Alert when then number of user lockouts is abnormally high.     |
| Slow user signin            | slow\_user\_signin             | (not implemented) Alert when the user sign-in phase is unusually slow.            |
| Too many user registrations | too\_many\_user\_registrations | (not implemented) Alert when the number of user registrations is abnormally high. |

{% hint style="info" %}
For each alert type, you can select the [notification channels](notification-channels.md) you want to use to send the events.
{% endhint %}

## Configure alerts

### Too many login failures

You can override the default configuration for each alert in the AM API `gravitee.yml` file.

```
vi GRAVITEE_AM_HOME/am-management-api/config/gravitee.yml

...
# Gravitee AM Alerts managed by the Alert Engine module
alerts:
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
...
```

## Installation and configuration

Beforehand you will need to deploy on your gateway:

* The [Risk Assessment Plugin](https://download.gravitee.io/#graviteeio-ee/plugins/services/risk-assessment/gravitee-risk-assessment-core/)
* Geo velocity requires the [Gravitee Geoip Plugin](https://download.gravitee.io/#graviteeio-am/plugins/repositories/gravitee-service-geoip/) to be installed also

### **Management API**

You can override the Management-API `gravitee.yml` configuration:

```yaml
alerts:
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
```

If you want to raise an alert for multiple assessments you CAN use comma-separated values for `alerts.risk_assessment.*.assessments`, e.g:

```yaml
alerts:
  risk_assessment:
  # You need the Risk Assessment Service plugin for these alerts
    geoVelocity:
      assessments: HIGH, MEDIUM, LOW # Will trigger an alert if either HIGH / MEDIUM / LOW is raised
    ipReputation:
      assessments: HIGH, LOW # Will trigger an alert if either HIGH / LOW is raised
    unknownDevices:
      assessments: LOW #  Will only trigger an alert if LOW is raised only
```

Possible values are `HIGH, MEDIUM, REGULAR, LOW, SAFE, NONE`

### Gateway

You can override the Gateway `gravitee.yml` configuration:

```yaml
alerts:
  risk_assessment:
    settings:
      enabled: true
      devices:
        enabled: true
        thresholds:
          HIGH: 1 # Arbitrary value
      ipReputation:
        enabled: true
        thresholds:
          LOW: 1 # in percentage
      geoVelocity:
        enabled: true
        thresholds:
          LOW: 0.2777778 # in m/s - 1km/h
```

If you want to raise more or change assessments, simply modify the settings:

```yaml
alerts:
  risk_assessment:
    settings:
      devices:
        thresholds:
          LOW: 1
      ipReputation:
        thresholds:
          HIGH: 70
          MEDIUM: 30
          LOW: 1
      geoVelocity:
        thresholds:
          LOW: 0.2777778 # in m/s - 1km/h
          MEDIUM: 6.9444445 # 25km/h
          HIGH: 69.444445 # 250km/h
```

Possible values are `HIGH, MEDIUM, REGULAR, LOW, SAFE, NONE`.
