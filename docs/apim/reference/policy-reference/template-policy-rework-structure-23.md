---
description: This page provides the technical details of the Keyless policy
---

# Keyless

## Overview

This security policy does not block any requests as it considers them as valid by default.

It sets multiple attributes during policy execution, as follows:

* `application`: Anonymous application value, which is equal to `1`.
* `user-id`: Internet Protocol (IP) address of the client or last proxy that sent the request.

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Keyless policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="176.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Errors

This policy cannot fail as it does not carry out any validation.

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-keyless/blob/master/CHANGELOG.md" %}
