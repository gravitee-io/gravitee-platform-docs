# Overview

This page describes how to configure APIM to allow users to connect
using an APIM data source. This is required when you want to allow user
registration.

You define new users in APIM Console.

Passwords are encoded using the BCrypt strong hashing function.

To activate this provider, all you need to do is declare it. All data
source information is then retrieved from the Management Repository
configuration.

    security:
      providers:
        - type: gravitee
