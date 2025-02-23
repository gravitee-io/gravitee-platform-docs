# Connect with Keycloak

### Overview

This page explains how to configure APIM to allow users to connect using [Keycloak](https://www.keycloak.org/).

### Create a Keycloak client

Before you can connect to the Gravitee portal using Keycloak, you need to create a new client.

#### Create a new client

1.  In Keycloak, create a new client.

    ![Create a new client](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_create\_client.png)
2.  Enter the client details.

    ![Fill the form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_configure\_client.png)

|   | The `Valid Redirect URIs` value must exactly match the domain which is hosting APIM Portal. |
| - | ------------------------------------------------------------------------------------------- |

#### Retrieve client credentials

After you create the client, you can retrieve its details for authentication configuration.

![Get Client credentials](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_client\_credentials.png)

### Configure APIM

#### SSL support

When using custom a Public Key Infrastructure (PKI) for your OAuth2 authentication provider, you may have to specify the certificate authority chain of your provider in APIM.

```
export JAVA_OPTS="
  -Djavax.net.ssl.trustStore=/opt/graviteeio-management-api/security/truststore.jks
  -Djavax.net.ssl.trustStorePassword=<MYPWD>"
```

Docker environment

```
 local_managementapi:
    extends:
      file: common.yml
      service: managementapi
    ports:
      - "8005:8083"
    volumes:
      - ./conf/ssl/truststore.jks:/opt/graviteeio-management-api/security/truststore.jks:ro
      - ./logs/management-api:/home/gravitee/logs
    links:
      - "local_mongodb:demo-mongodb"
      - "local_elasticsearch:demo-elasticsearch"
    environment:
      - JAVA_OPTS=-Djavax.net.ssl.trustStore=/opt/graviteeio-management-api/security/truststore.jks -Djavax.net.ssl.trustStorePassword=<MYPWD>
      - gravitee_management_mongodb_uri=mongodb://demo-mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_analytics_elasticsearch_endpoints_0=http://demo-elasticsearch:9200
```

#### Configure with `gravitee.yml` or APIM Console

You can configure this provider both in APIM Console and in the `gravitee.yml` configuration file. Whichever you choose, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you click the **Save** button (if configuring in APIM Console) or restart APIM API (if configuring in the configuration file).

|   | If you configure the provider in the configuration file and then change the values in APIM Console, all changes are overwritten by the values in the configuration file next time you restart APIM API. |
| - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

**APIM Console configuration**

1. Click **Organization Settings > Authentication**.
2. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) and select the **OpenID Connect** icon.
3. If you want to use this provider to log in to APIM Portal, ensure that **Allow portal authentication to use this identity provider** is checked. To use it only for APIM Console, uncheck this option.
4.  Enter the details of the provider, including the credentials created in the AM client.

    ![Gravitee.io - New OIDC IDP](https://docs.gravitee.io/images/apim/3.x/management-api-configuration-idp/new-oidc.png)
5. Click **CREATE**.
6. Activate the provider for Portal or Console login.

**`gravitee.yml` file configuration**

Update the following section of the file with the Keycloak client credentials.

```
security:
  providers:
    - type: oidc
      id: keycloak # not required if not present, the type is used
      clientId: gravitee
      clientSecret: 3aea136c-f056-49a8-80f4-a6ea521b0c94
      tokenIntrospectionEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/token/introspect
      tokenEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/token
      authorizeEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/auth
      userInfoEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/userinfo
      userLogoutEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/logout
      color: "#0076b4"
      syncMappings: false
      scopes:
        - openid
        - profile
      userMapping:
        id: sub
        email: email
        lastname: family_name
        firstname: given_name
        picture: picture
      groupMapping:
        - condition: "{#jsonPath(#profile, '$.identity_provider_id') == 'PARTNERS' && #jsonPath(#profile, '$.job_id') != 'API_MANAGER'}"
          groups:
            - Group 1
            - Group 2
      roleMapping:
        - condition: "{#jsonPath(#profile, '$.job_id') != 'API_MANAGER'}"
          roles:
            - "ORGANIZATION:USER"
            - "ENVIRONMENT:API_CONSUMER"                  #applied to the DEFAULT environment
            - "ENVIRONMENT:DEFAULT:API_CONSUMER"          #applied to the DEFAULT environment
            - "ENVIRONMENT:<ENVIRONMENT_ID>:API_CONSUMER" #applied to environment whose id is <ENVIRONMENT_ID>
```

### Test the connection

#### Create a new user in Keycloak

1.  Create your new user.

    ![Create a user](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_users.png)
2.  Enter the user details.

    ![Fill the user form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_create\_user.png)
3.  Define the user credentials.

    ![Define user credentials](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_create\_user\_credentials.png)

#### Log in to APIM Portal

1.  Click **Sign in with Keycloak**.

    ![Login Form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_login\_form.png)
2.  Enter the Keycloak credentials and click **Log In**.

    ![Keycloak Login Form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_login\_form2.png)

    You have successfully logged in:

    ![Here we are !](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_login\_success.png)

### Managing roles with keycloak

Configure Keycloak and Gravitee to map your own organization with available built-in or your custom registered roles.

#### Gravitee roles console

1.  Consider built-in or create custom Gravitee roles.

    ![Gravitee console - roles page](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-00-gravitee-default\_roles.png)

#### Create and configure Keycloak Client scope

1. In your realm, go to the `Client scopes` page.
2.  Set a special gravitee-client-groups [Scope](https://oauth.net/2/scope/) that will contain users' roles.

    ![Keycloak console - Create scope](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-01-client\_scopes-roles\_add\_client\_scope.png)
3.  In the new client scope, set a mapper with Claim name "groups".

    ![Keycloak console - Add mapper to scope](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-02-client\_scopes-mapper.png)
4. In your realm, go to the `Client` page, and select your Client.
5.  Add the new configured scope in the `Client Scopes` tab.

    ![Keycloak console - Add scope to client](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-03-client-add\_scope.png)

#### Create Keycloak Client roles

1.  In your client, create roles as needed by organization.

    ![Keycloak console - Create client roles](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-04-client-add\_roles.png)

#### Configure Keycloak users with appropriate roles

![Keycloak console - Add roles to user](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-roles-05-users-add\_user\_client\_roles.png)

#### Configure Gravitee role mappings

Gravitee role mapping uses Spring Expression Language ([SpEL](https://docs.spring.io/spring-framework/docs/3.0.x/reference/expressions.html)) for writing conditions. The only available object in context is #profile set from [userInfoEndpoint](https://www.oauth.com/oauth2-servers/signing-in-with-google/verifying-the-user-info/).

```
security:
  providers:
    - type: oidc
      ...
      roleMapping:
        - condition: "{(#jsonPath(#profile, '$.groups') matches 'gravitee-admin' )}"
          roles:
            - "ORGANIZATION:ADMIN"
            - "ENVIRONMENT:ADMIN"
```
