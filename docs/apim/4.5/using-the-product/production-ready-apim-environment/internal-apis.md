# Configuring Internal APIs

## Overview

APIM API and APIM Gateway include internal APIs that are enabled by default. These internal APIs permit the retrieval of monitoring and technical information pertaining to Gravitee components (more information [here](/apim/getting-started/configuration/configure-apim-management-api/internal-api-1)).

## Disabling internal APIs

APIM API and APIM Gateway include internal APIs which are enabled by default. If you do not intend to use them, **we recommend you disable them**.

Perform the following steps on both the APIM API component and the APIM Gateway component:

1. Open your `gravitee.yml` file.
2.  In the `services:` section, set the `http:` `enabled` value to `false`:

    ```yaml
    services:
      core:
        http:
          enabled: false
          port: 18083
          host: localhost
          authentication:
            # authentication type to be used for the core services
            # - none: to disable authentication
            # - basic: to use basic authentication
            # default is "basic"
            type: basic
            users:
              admin: adminadmin
    ```

### Enforcing security

If you plan to keep the internal API enabled, please consider enforcing the security by following the next steps.

1.  Ensure basic authentication:

    ```yaml
    services:
      core:
        http:
          ...
          authentication:
            type: basic
            users:
              admin: adminadmin
    ```
2. Remove the default admin user and password.
3. Replace these with a username/password of your choosing, as shown in the example below. A good practice is to:
   1. Create a random username that is less obvious than a simple "admin" user.
   2.  Define a strong password that follows security best practices. Ideally, you should use a password generator.

       ```yaml
       services:
         core:
           http:
             ...
             authentication:
               type: basic
               users:
                 kJCe9nxhNV: "k5/ya\S6*9dm2kT`dbnhr{jzyD)<u.<9"
       ```
4.  It is highly recommended that you bind the internal API to make it accessible from localhost only:

    ```yaml
    services:
      core:
        http:
          enabled: true
          port: 18083
          host: localhost
    ```
