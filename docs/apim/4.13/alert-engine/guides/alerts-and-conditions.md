---
description: This article walks through the basics of alerts and how to set up conditions
---

# Alerts and Conditions

## Introduction

Gravitee Alert Engine sends alerts to defined systems per a set of given conditions. This article explains how alerts are structured and how to define conditions to control alerting.

## The anatomy of an alert

An alert is defined in `JSON` format and includes the following elements:

* Name
* Description
* Source (event source)
* Severity (info, warning, critical)
* List of conditions
* List of filters
* [Dampening](dampening.md)
* [Notifications](notifications.md)

### Example alert

```
{
  "name" : "Response time Threshold",
  "source" : "REQUEST",
  "enabled" : true,
  "conditions" : [ {
    "property" : "response.response_time",
    "operator" : "lt",
    "threshold" : 1500.0,
    "type" : "threshold"
  } ],
  "filters" : [ ],
  "dampening" : {
    "mode" : "strict_count",
    "trueEvaluations" : 2
  },
  "notifications" : [ {
    "type" : "slack-notifier",
    "configuration" : {
      "url" : "https://hooks.slack.com/services/T07XXXXX/BNXXXXXX/xxxxxxxxxxx",
      "useSystemProxy" : false,
      "message" : "${alert.name} has been evaluated to true"
    }
  }]
}
```

## Conditions

Conditions set the parameters for what triggers an alert, and therefore, notifications when using Gravitee AE. When defining a custom message, you can access the configuration of the conditions of your alert. For each condition, you will find a description of available fields.

The list of conditions you can define for an alert are described below.

### String

Used to compare a string property value to a given value.

Available operators are: `EQUALS`, `NOT_EQUALS`, `STARTS_WITH`, `ENDS_WITH`, `CONTAINS`, `MATCHES`

| Key                                          | Description                                                                                          |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `alert.conditions[`_`integer`_`].type`       | Type of the condition: `STRING`                                                                      |
| `alert.conditions[`_`integer`_`].property`   | Property of the condition                                                                            |
| `alert.conditions[`_`integer`_`].operator`   | Operator of the condition: `EQUALS`, `NOT_EQUALS`, `STARTS_WITH`, `ENDS_WITH`, `CONTAINS`, `MATCHES` |
| `alert.conditions[`_`integer`_`].pattern`    | Pattern used to compare the property value                                                           |
| `alert.conditions[`_`integer`_`].ignoreCase` | Boolean that indicates if the comparison should ignore the case of the property value                |

### Threshold

Used to compare a number property value to a given threshold (`property < X`).

Available operators are: `LT`, `LTE`, `GTE`, `GT`

| Key                                         | Description                                         |
| ------------------------------------------- | --------------------------------------------------- |
| `alert.conditions[`_`integer`_`].type`      | Type of the condition: `THRESHOLD`                  |
| `alert.conditions[`_`integer`_`].property`  | Property of the condition                           |
| `alert.conditions[`_`integer`_`].operator`  | Operator of the condition: `LT`, `LTE`, `GTE`, `GT` |
| `alert.conditions[`_`integer`_`].threshold` | Threshold value of the condition (double value)     |

### Threshold Range

Used to compare a number property value to a given threshold range (`X < property < Y`).

Available operators: `LT`, `LTE`, `GTE`, `GT`

| Key                                             | Description                                                            |
| ----------------------------------------------- | ---------------------------------------------------------------------- |
| `alert.conditions[`_`integer`_`].type`          | Type of the condition: `THRESHOLD_RANGE`                               |
| `alert.conditions[`_`integer`_`].property`      | Property of the condition                                              |
| `alert.conditions[`_`integer`_`].operatorLow`   | Operator for the low bound of the condition: `LT`, `LTE`, `GTE`, `GT`  |
| `alert.conditions[`_`integer`_`].thresholdLow`  | Threshold value for the low bound of the condition (double value)      |
| `alert.conditions[`_`integer`_`].operatorHigh`  | Operator for the high bound of the condition: `LT`, `LTE`, `GTE`, `GT` |
| `alert.conditions[`_`integer`_`].thresholdHigh` | Threshold value for the high bound of the condition (double value)     |

### Aggregation

Used to compare an aggregated property value to a threshold. Note that this kind of condition requires a time-frame window to aggregate property values.

Available operators are: `LT`, `LTE`, `GTE`, `GT`

Available functions: `COUNT`, `AVG`, `MIN`, `MAX`, `P50`, `P90`, `P95`, `P99`

| Key                                                       | Description                                                                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `alert.conditions[`_`integer`_`].type`                    | Type of the condition: `AGGREGATION`                                                                                |
| `alert.conditions[`_`integer`_`].function`                | Function used to compute the aggregation of the condition: `COUNT`, `AVG`, `MIN`, `MAX`, `P50`, `P90`, `P95`, `P99` |
| `alert.conditions[`_`integer`_`].property`                | Property of the condition                                                                                           |
| `alert.conditions[`_`integer`_`].operator`                | Operator of the condition: `LT`, `LTE`, `GTE`, `GT`                                                                 |
| `alert.conditions[`_`integer`_`].threshold`               | Threshold value of the condition (double value)                                                                     |
| `alert.conditions[`_`integer`_`].duration`                | Size of the time-frame window to aggregate values (long value)                                                      |
| `alert.conditions[`_`integer`_`].timeUnit`                | Unit of time of the duration.                                                                                       |
| `alert.conditions[`_`integer`_`].projections[0].property` | Property the aggregation will use to group results                                                                  |

### Rate

Used to calculate the rate for a property value in comparison to a given condition and compare it to a threshold. Note that this kind of condition requires a time-frame window to aggregate property values.

Available operators: `LT`, `LTE`, `GTE`, `GT`

| Key                                                       | Description                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `alert.conditions[`_`integer`_`].type`                    | Type of the condition: `RATE`                                                                                                                                                                                                                                                                                       |
| `alert.conditions[`_`integer`_`].operator`                | Operator of the condition: `LT`, `LTE`, `GTE`, `GT`                                                                                                                                                                                                                                                                 |
| `alert.conditions[`_`integer`_`].threshold`               | Threshold value of the condition (double value)                                                                                                                                                                                                                                                                     |
| `alert.conditions[`_`integer`_`].comparison`              | A single value condition. It can be: [string](alerts-and-conditions.md#string), [string comparison](alerts-and-conditions.md#string-comparison), [threshold](alerts-and-conditions.md#threshold), [threshold range](alerts-and-conditions.md#threshold-range), or [comparison](alerts-and-conditions.md#comparison) |
| `alert.conditions[`_`integer`_`].duration`                | Size of the time-frame window to aggregate values (long value)                                                                                                                                                                                                                                                      |
| `alert.conditions[`_`integer`_`].timeUnit`                | Unit of time of the duration                                                                                                                                                                                                                                                                                        |
| `alert.conditions[`_`integer`_`].projections[0].property` | Property the aggregation will use to group results                                                                                                                                                                                                                                                                  |

### Comparison

Used to compare a number property value to another number property value (`property1 < property2`).

Available operators: `LT`, `LTE`, `GTE`, `GT`

| Key                                          | Description                                         |
| -------------------------------------------- | --------------------------------------------------- |
| `alert.conditions[`_`integer`_`].type`       | Type of the condition: `COMPARE`                    |
| `alert.conditions[`_`integer`_`].property`   | Property of the condition                           |
| `alert.conditions[`_`integer`_`].operator`   | Operator of the condition: `LT`, `LTE`, `GTE`, `GT` |
| `alert.conditions[`_`integer`_`].multiplier` | Multiplier value of the condition (double value)    |
| `alert.conditions[`_`integer`_`].property2`  | Second property of the condition                    |

### String comparison

Used to compare a string property value to an other string property value (`property1 < property2`).

Available operators are: `EQUALS`, `NOT_EQUALS`, `STARTS_WITH`, `ENDS_WITH`, `CONTAINS`, `MATCHES`

| Key                                          | Description                                                                                          |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `alert.conditions[`_`integer`_`].type`       | Type of the condition: `STRING_COMPARE`                                                              |
| `alert.conditions[`_`integer`_`].property`   | Property of the condition                                                                            |
| `alert.conditions[`_`integer`_`].operator`   | Operator of the condition: `EQUALS`, `NOT_EQUALS`, `STARTS_WITH`, `ENDS_WITH`, `CONTAINS`, `MATCHES` |
| `alert.conditions[`_`integer`_`].property2`  | Second property of the condition                                                                     |
| `alert.conditions[`_`integer`_`].ignoreCase` | Boolean that indicates if the comparison should ignore the case of the properties value              |
