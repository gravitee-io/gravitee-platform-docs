---
description: An overview about keyless.
---

# Keyless

## Overview

A Keyless (public) plan does not require authentication and allows public access to an API. By default, keyless plans offer no security and are most useful for quickly and easily exposing your API to external users.

## Configuration

A Keyless plan does not require configuration other than general plan settings and restrictions.

Due to not requiring a subscription and the lack of a consumer identifier token, Keyless consumers are set as `unknown application` in the API analytics section.

You can configure basic authentication for Keyless plans by associating a Basic Authentication policy (see the [policy reference](../../create-and-configure-apis/apply-policies/policy-reference/)) that uses either an LDAP or inline resource.
