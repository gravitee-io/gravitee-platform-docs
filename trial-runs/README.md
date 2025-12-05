# Configure authentication with Login and password

## Overview

## Prerequisites&#x20;

* Install Self-Hosted Installation of Gravitee APIM or a Hybrid Installation of Gravitee APIM. For more information about installing Gravitee APIM, see [Broken link](/broken/pages/l3VTaBMjUvFd4jXfkLQh "mention") or [Broken link](/broken/pages/KmYIfcneJBExnYks77zr "mention").&#x20;
* Ensure that your installation of Gravitee APIM  is version 4.10 or later. For more information about upgrading Gravitee APIM, see [Broken link](/broken/pages/7anra8jO4R0or1MnFTlp "mention").
* Complete the steps in [Broken link](/broken/pages/5RELNfUmXNFFWCOkXm6g "mention").

## Authentication using login and password

You can configure login and password authentication using any of the following methods:<br>

* [#in-memory-users](./#in-memory-users "mention")
* [#ldap-authentication](./#ldap-authentication "mention")
* [#apim-data-source-authentication](./#apim-data-source-authentication "mention")

### In-memory users

To configure in-memory users, complete the steps relevant to your installation type:

{% tabs %}
{% tab title="Docker" %}
1. In your `gravitee.yaml` file, navigate to the `security` section, and then add the following configuration:&#x20;

```yaml
Overview
The following sections describe how to configure in-memory users, LDAP authentication, and APIM data source authentication.
In-memory users
This example shows a basic in-memory implementation, providing a simple and convenient way to declare advanced users of APIM, such as administrator users. To do this, you could configure the gravitee.yaml file as follows:
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
    - type: 
memory
insert memory here.

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

2. Deploy your installation with your new configuration using the following command:

```bash
docker compose up -d
```
{% endtab %}

{% tab title="Helm" %}
1.  In your `values.yaml` file, navigate to the `graviteeRepoAuth` section, and then add the following configuration:<br>

    ```yaml
    inMemoryAuth:
      enabled: true
      allowEmailInSearchResults: false
      passwordEncodingAlgo: bcrypt

    # Define extra inMemory users here or disable the default ones here
    # By default, admin user will be added. If you want to remove the default admin turn the followong boolean to false.
    adminAccountEnable: true
    # Default password "admin", use bcrypt ($2a$ version) to generate a new one
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
        # Useful to receive notifications
        #email:
        #firstName:
        #lastName:
      - user:
        username: api1
        # Password value: api1
        password: $2a$10$iXdXO4wAYdhx2LOwijsp7.PsoAZQ05zEdHxbriIYCbtyo.y32LTji
        # You can declare multiple roles using comma separator
        roles: ORGANIZATION:USER, ENVIRONMENT:API_PUBLISHER
        #email:
        #firstName:
        #lastName:
      - user:
        username: application1
        # Password value: application1
        password: $2a$10$2gtKPYRB9zaVaPcn5RBx/.3T.7SeZoDGs9GKqbo9G64fKyXFR1He.
        roles: ORGANIZATION:USER, ENVIRONMENT:USER
        #email:
        #firstName:
        #lastName:

    ```
2.  Deploy your installation with your new configuration using the following command:<br>

    ```bash
    helm upgrade gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml \
      --set 'portal.ingress.annotations.nginx\.ingress\.kubernetes\.io/rewrite-target=null' \
      --wait \
      --timeout 5m
    ```
{% endtab %}
{% endtabs %}

#### Generate a new password

*   Generate a new password for your hash password using the following command:<br>

    ```bash
    htpasswd -bnBC 10 "" <new_password> | tr -d ':\n'
    ```

    * Replace `<new_password>` with the new password.&#x20;

#### Verification&#x20;

### LDAP authentication&#x20;

{% tabs %}
{% tab title="Docker" %}
1.  Navigate to the `security` section, and then add the following configuration: <br>

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
2.  Deploy your installation with your new configuration using the following command: <br>

    ```yaml
    docker compose up -d
    ```
{% endtab %}

{% tab title="Helm" %}
1.  In your `values.yaml` file, navigate to the `ldap` section, and then add the following configuration: <br>

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
2.  Deploy your installation with your new configuration using the following command:<br>

    ```bash
    helm upgrade gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml \
      --set 'portal.ingress.annotations.nginx\.ingress\.kubernetes\.io/rewrite-target=null' \
      --wait \
      --timeout 5m
    ```
{% endtab %}
{% endtabs %}

#### Verification

### APIM data source authentication&#x20;

You can connect users to the New Developer Portal using an APIM data source. If you want to add users with self-registration, you must add an APIM data source.&#x20;

To connect users to your the New Developer Portal using an APIM data source, follow the steps relevant to your installation:

{% tabs %}
{% tab title="Docker" %}
1. Navigate to the `security` section, and then add the following configuration:

```yaml
security:
  providers:
    - type: gravitee
```

2. Deploy your installation with your new configuration using the following command:

```
docker compose down 
docker compose up 
```
{% endtab %}

{% tab title="Helm" %}

{% endtab %}
{% endtabs %}

#### Verification&#x20;

## Next steps&#x20;

* [Broken link](/broken/pages/dEbr8DOikUsbYrvRS8Ec "mention")
