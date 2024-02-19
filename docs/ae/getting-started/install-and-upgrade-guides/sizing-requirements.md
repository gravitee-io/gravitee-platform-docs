---
description: This article walks through sizing requirements for Alert Engine
---

# Sizing requirements

## Introduction

The following sections provide installation advice, particularly regarding resource planning and system optimization.

## Size requirements

| Number of triggers | Compute  | Memory | Events/second |
| ------------------ | -------- | ------ | ------------- |
| 10                 | 1 (v)CPU | 256m   | 7000          |
| 100                | 1 (v)CPU | 256m   | 4000          |
| 100                | 2 (v)CPU | 256m   | 8000          |
| 500                | 1 (v)CPU | 256m   | 2500          |
| 500                | 2 (v)CPU | 256m   | 5000          |
| 500                | 2 (v)CPU | 512m   | 6000          |
| 1000               | 2 (v)CPU | 512m   | 4000          |

## Best practices

### Moderate your notifications

Ingesting and processing events requires computational resources, so you should make sure that all this processing power is not overcome by firing too many notifications. The following best practices can help with this.

### **Dampenings**

Dampenings are a good way to reduce the frequency of your notifications. See the [Dampening](../../guides/dampening.md) page for more information about various dampening strategies you can use.

### **Time-based conditions**

[Aggregation](../../guides/alerts-and-conditions.md#aggregation) and [Rate](../../guides/alerts-and-conditions.md#rate) conditions rely on `duration` and `timeUnit`, so they can be evaluated in a given period of time.

### Redundancy

Alert Engine allows you to deploy a cluster of several gateways in order to ingest events and triggers but also to avoid having a single point of failure in case one of the nodes goes down.

## Tune your JVM

We performed our tests by enforcing **Garbage-First Collector**. While this garbage collector has been the default one since Java 9, under certain conditions (such as very low resource allocation) the JVM enforces the **Serial Garbage Collector** (SerialGC) as the default one.

To enforce it, make sure that `JAVA_OPTS="$JAVA_OPTS -XX:+UseG1GC"` is included in your JVM arguments.

## Make your events small

Your events should only contain the necessary data, which means that you should:

* Remove extra unnecessary data.
* Keep the name/values of your JSON objects as small as possible.

This provides for better performance for data serialization.

## More compute, more power

If you need more processing power to ingest events or to execute rules, increase the number of (v)CPUs. Increasing the memory size can be useful if you are dealing with large data or as a buffer when the computational power is under load.\\
