# Enforcing logging rules with ArchUnit Maven plugin

## Overview

{% hint style="info" %}
This page is for plugin developers building custom Gravitee plugins. The ArchUnit rules require `gravitee-parent` version 24.0.0 or later.
{% endhint %}

The `gravitee-archrules-maven-plugin` enforces context-aware logging rules at build time. It runs during the Maven `verify` phase and provides two goals:

* **`global-logging-check`:** Verifies that all classes use `NodeLoggerFactory` instead of SLF4J's `LoggerFactory`.
* **`execution-context-logging-check`:** Verifies that methods with an `ExecutionContext` parameter use `ctx.withLogger(log)` instead of calling the logger directly.

## Configuration

<table>
    <thead>
        <tr>
            <th width="350">Property</th>
            <th width="100">Type</th>
            <th width="100">Default</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>gravitee.archrules.skip</code></td>
            <td>Boolean</td>
            <td><code>false</code></td>
            <td>Skip all ArchUnit rule checks</td>
        </tr>
        <tr>
            <td><code>global-logging-check.failOnError</code></td>
            <td>Boolean</td>
            <td><code>true</code></td>
            <td>Fail build on SLF4J <code>LoggerFactory</code> usage</td>
        </tr>
        <tr>
            <td><code>execution-context-logging-check.failOnError</code></td>
            <td>Boolean</td>
            <td><code>true</code></td>
            <td>Fail build on direct logger calls when <code>ExecutionContext</code> is available</td>
        </tr>
    </tbody>
</table>

## Skip checks

To skip ArchUnit checks during packaging or local development:

```bash
mvn clean package -Dgravitee.archrules.skip=true
```

For more information on the logging patterns these rules enforce, see [Context-aware logging in plugins](../../plugins/context-aware-logging.md).
