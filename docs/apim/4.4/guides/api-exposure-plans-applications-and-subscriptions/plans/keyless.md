---
description: This page describes the Keyless authentication type
---

# Keyless

## Introduction

A Keyless (public) plan does not require authentication and allows public access to an API. By default, keyless plans offer no security and are most useful for quickly and easily exposing your API to external users.

## Configuration

A Keyless plan does not require configuration other than general plan settings and restrictions.

Due to not requiring a subscription and the lack of a consumer identifier token, Keyless consumers are set as `unknown application` in the API analytics section.

You can configure basic authentication for Keyless plans by associating a [Basic Authentication policy](../../../reference/policy-reference/basic-authentication.md) that uses either an LDAP or inline resource.
