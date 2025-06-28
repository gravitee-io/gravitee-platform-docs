# Authentication Providers

## Overview

The following sections describe how to configure in-memory users, LDAP authentication, and APIM data source authentication.

## In-memory users

This example shows a basic in-memory implementation, providing a simple and convenient way to declare advanced users of APIM, such as administrator users. To do this, you could configure the `gravitee.yaml` file as follows:

<pre class="language-yaml"><code class="lang-yaml"># Authentication and identity sources
# Users can have following roles (authorities):
#  USER: Can access portal and be a member of an API
#  API_PUBLISHER: Can create and manage APIs
#  API_CONSUMER: Can create and manage Applications
#  ADMIN: Can manage global system
security:
  # When using an authentication providers, use trustAll mode for TLS connections
  # trustAll: false
  providers:  # authentication providers
    - type: <a data-footnote-ref href="#user-content-fn-1">memory</a>
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

</code></pre>

### Generate a new password

If you use [bcrypt](https://en.wikipedia.org/wiki/Bcrypt) to hash passwords, you can generate new passwords with the [htpasswd](https://httpd.apache.org/docs/current/en/programs/htpasswd.html) command line, as shown in the following example (where `new_password` is your new password):

```bash
htpasswd -bnBC 10 "" new_password | tr -d ':\n'
```

## LDAP authentication

There are many ways to configure users via LDAP. To illustrate the basic concepts, here is an example configuration using the `gravitee.yaml` file:

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

## APIM data source authentication

APIM allows users to connect using an APIM data source. This is required if you want to add and register users via self-registration.

To activate this provider, all you need to do is declare it in the `gravitee.yaml` file. All data source information is then retrieved from the Management Repository configuration.

```yaml
security:
  providers:
    - type: gravitee
```

[^1]: insert memory here.
