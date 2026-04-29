---
description: An overview about authentication providers.
---

# Authentication Providers

## Overview

The following sections describe how to configure in-memory users, LDAP authentication, and APIM data source authentication.

## In-memory users

This example shows a basic in-memory implementation, providing a simple and convenient way to declare advanced users of APIM, such as administrator users. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
# Authentication and identity sources
# Users can have following roles (authorities):
#  USER: Can access portal and be a member of an API
#  API_PUBLISHER: Can create and manage APIs
#  API_CONSUMER: Can create and manage Applications
#  ADMIN: Can manage global system
security:
  # When using an authentication providers, use trustAll mode for TLS connections
  # trustAll: false
  providers:  # authentication providers
    - type: memory
      # allow search results to display the user email. Be careful, It may be contrary to the user privacy.
#      allow-email-in-search-results: true
      # password encoding/hashing algorithm. One of:
      # - bcrypt : passwords are hashed with bcrypt (supports only $2a$ algorithm)
      # - none : passwords are not hashed/encrypted
      # default value is bcrypt
      password-encoding-algo: bcrypt
      users:
        - user:
          username: user
          #firstname:
          #lastname:
          # Passwords are encoded using BCrypt
          # Password value: password
          password: $2a$10$9kjw/SH9gucCId3Lnt6EmuFreUAcXSZgpvAYuW2ISv7hSOhHRH1AO
          roles: ORGANIZATION:USER,ENVIRONMENT:USER
          # Useful to receive notifications
          #email:
        - user:
          username: admin
          #firstname:
          #lastname:
          # Password value: admin
          password: $2a$10$Ihk05VSds5rUSgMdsMVi9OKMIx2yUvMz7y9VP3rJmQeizZLrhLMyq
          roles: ORGANIZATION:ADMIN,ENVIRONMENT:ADMIN
          #email:
        - user:
          username: api1
          #firstname:
          #lastname:
          # Password value: api1
          password: $2a$10$iXdXO4wAYdhx2LOwijsp7.PsoAZQ05zEdHxbriIYCbtyo.y32LTji
          # You can declare multiple roles using comma separator
          roles: ORGANIZATION:USER,ENVIRONMENT:API_PUBLISHER
          #email:
        - user:
          username: application1
          #firstname:
          #lastname:
          # Password value: application1
          password: $2a$10$2gtKPYRB9zaVaPcn5RBx/.3T.7SeZoDGs9GKqbo9G64fKyXFR1He.
          roles: ORGANIZATION:USER,ENVIRONMENT:USER
          #email:
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
For Docker Compose, in-memory user lists are most reliably defined in `gravitee.yml` mounted into the Management API container. The provider type and password encoding can be set via environment variables in the `.env` file or the `environment:` block of the Management API service:

```bash
gravitee_security_providers_0_type=memory
gravitee_security_providers_0_password-encoding-algo=bcrypt
gravitee_security_providers_0_allow-email-in-search-results=false
```

For the user list, mount a `gravitee.yml` file containing the `security.providers[].users` block into `/opt/graviteeio-management-api/config/gravitee.yml`.
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the `inMemoryAuth` block, the admin account values, and `extraInMemoryUsers` in your `values.yaml` file. The APIM Helm chart renders these values into a `security.providers[]` entry of type `memory` in the Management API `gravitee.yml` at install time:

```yaml
inMemoryAuth:
  enabled: true
  allowEmailInSearchResults: false
  passwordEncodingAlgo: bcrypt

# Default admin account (set adminAccountEnable=false to disable)
adminAccountEnable: true
adminPasswordBcrypt: $2a$10$Ihk05VSds5rUSgMdsMVi9OKMIx2yUvMz7y9VP3rJmQeizZLrhLMyq
adminEmail:
adminFirstName:
adminLastName:

extraInMemoryUsers: |
  - user:
    username: user
    # Password value: password
    password: $2a$10$9kjw/SH9gucCId3Lnt6EmuFreUAcXSZgpvAYuW2ISv7hSOhHRH1AO
    roles: ORGANIZATION:USER, ENVIRONMENT:USER
  - user:
    username: api1
    # Password value: api1
    password: $2a$10$iXdXO4wAYdhx2LOwijsp7.PsoAZQ05zEdHxbriIYCbtyo.y32LTji
    roles: ORGANIZATION:USER, ENVIRONMENT:API_PUBLISHER
  - user:
    username: application1
    # Password value: application1
    password: $2a$10$2gtKPYRB9zaVaPcn5RBx/.3T.7SeZoDGs9GKqbo9G64fKyXFR1He.
    roles: ORGANIZATION:USER, ENVIRONMENT:USER
```
{% endtab %}
{% endtabs %}

### Generate a new password

If you use bcrypt to hash passwords, you can generate new passwords with the [htpasswd](https://httpd.apache.org/docs/current/en/programs/htpasswd.html) command line, as shown in the following example (where `new_password` is your new password):

```bash
htpasswd -bnBC 10 "" new_password | tr -d ':\n'
```

## LDAP authentication

There are many ways to configure users via LDAP. The following example illustrates the basic concepts. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
# ===================================================================
# LDAP SECURITY PROPERTIES
#
# This sample file declared one ldap authentication source
# ===================================================================
security:
  type: basic
  providers:
    - type: ldap
      context:
        username: "uid=admin,ou=system"
        password: "secret"
        url: "ldap://localhost:389/dc=gravitee,dc=io"
        base: "c=io,o=gravitee"
      authentication:
        user:
          base: "ou=people"
          filter: "uid={0}"
        group:
          base: "o=authorization groups"
          filter: "member={0}"
          role:
            attribute: "cn"
            mapper: {
              GRAVITEE-CONSUMERS: API_CONSUMER,
              GRAVITEE-PUBLISHERS: API_PUBLISHER,
              GRAVITEE-ADMINS: ADMIN,
              GRAVITEE-USERS: USER
            }
      lookup:
        user:
          base: "ou=people"
          filter: "(&(objectClass=myObjectClass)(|(cn=*{0}*)(uid={0})))"
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
For Docker Compose, LDAP user and group filters are most reliably defined in `gravitee.yml` mounted into the Management API container. The basic LDAP provider settings can be set via environment variables in the `.env` file or the `environment:` block of the Management API service:

```bash
gravitee_security_providers_0_type=ldap
gravitee_security_providers_0_context_username=uid=admin,ou=system
gravitee_security_providers_0_context_password=secret
gravitee_security_providers_0_context_url=ldap://localhost:389/dc=gravitee,dc=io
gravitee_security_providers_0_context_base=c=io,o=gravitee
```

For the full `authentication`, `lookup`, and `role.mapper` blocks, mount a `gravitee.yml` file containing the `security.providers[]` entry into `/opt/graviteeio-management-api/config/gravitee.yml`.
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the `ldap` block in your `values.yaml` file. The APIM Helm chart renders these values into a `security.providers[]` entry of type `ldap` in the Management API `gravitee.yml` at install time:

```yaml
ldap:
  enabled: true
  context:
    # User to bind the LDAP
    user: user@example.com
    # Password to bind the LDAP
    password: "secret"
    # URL to LDAP
    url: ldap://ldap.example.com
    # Bind base to be used in authentication and lookup sections
    base: dc=example,dc=com
  authentication:
    user:
      # Base to search users, must be relative to the context.base
      base: ou=users
      # Use sAMAccountName if you are in AD
      # Use uid if you are in a native LDAP
      # The {0} will be replaced by user typed to authenticate
      filter: sAMAccountName={0}
      # If you have an attribute with the user photo, you can set it here
      photo: "thumbnailPhoto"
    group:
      # Base to search groups, must be relative to the context.base
      # There an issue here, until fixed only oneleve search is supported
      base: ou=gravitee,ou=groups
      # The {0} will be replaced by DN of the user
      filter: member={0}
      role:
        # The attribute that define your group names on your AD/LDAP
        # You can use sAMAccountName if you're in AD or cn if you're in native LDAP
        attribute: sAMAccountName
        consumer: LDAP_GROUP_CONSUMER
        publisher: LDAP_GROUP_PUBLISHER
        admin: LDAP_GROUP_ADMIN
        user: LDAP_GROUP_USER
  lookup:
    allowEmailInSearchResults: false
    # Note that personal information can be exposed without user consentment
    user:
      # Base to lookup user, must be relative to context.base
      base: ou=users
      # The filter can be any type of complex LDAP query
      filter: (&(objectClass=person)(|(cn=*{0}*)(sAMAccountName={0})))
```
{% endtab %}
{% endtabs %}

## APIM data source authentication

APIM allows users to connect using an APIM data source. This is required if you want to add and register users via self-registration.

All data source information is retrieved from the Management Repository configuration. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
security:
  providers:
    - type: gravitee
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
Add the following variable to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Management API service:

```bash
gravitee_security_providers_0_type=gravitee
```
{% endtab %}

{% tab title="Helm values.yaml" %}
The APIM data source provider is enabled by default. Confirm or set `graviteeRepoAuth.enabled` in your `values.yaml` file:

```yaml
graviteeRepoAuth:
  enabled: true
```

The chart renders this as a `security.providers[]` entry of type `gravitee` in the Management API `gravitee.yml` at install time.
{% endtab %}
{% endtabs %}

[^1]: insert memory here.
