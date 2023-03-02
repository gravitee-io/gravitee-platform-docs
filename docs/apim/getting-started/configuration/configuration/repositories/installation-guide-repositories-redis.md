# Overview

This repository plugin is for connecting to Redis databases for Rate
Limit feature.

# Install the Rate Limit repository plugin

Repeat these steps on each component (APIM Gateway and APIM API) where
the SQL database is used.

1.  Download the plugin corresponding to your APIM version (take the
    latest maintenance release).

2.  Place the zip file in the plugin directory for each component
    (`$GRAVITEE_HOME/plugins`).

3.  Configure your `gravitee.yml` files, as described in the next
    section.

# Configure the Rate Limit repository plugin

    # ===================================================================
    # MINIMUM REDIS REPOSITORY PROPERTIES
    #
    # This is a minimal sample file declared connection to Redis
    # ===================================================================
    ratelimit:
      type: redis               # repository type
      redis:                    # redis repository
        host:                   # redis host (default localhost)
        port:                   # redis port (default 6379)
        password:               # redis password (default null)
        timeout:                # redis timeout (default -1)

        # Following properties are REQUIRED ONLY when running Redis in sentinel mode
        sentinel:
          master:               # redis sentinel master host
          password:             # redis sentinel master password
          nodes: [              # redis sentinel node(s) list
            {
              host : localhost, # redis sentinel node host
              port : 26379      # redis sentinel node port
            },
            {
              host : localhost,
              port : 26380
            },
            {
              host : localhost,
              port : 26381
            }
          ]

# Point of interest

If Redis Rate Limit repository is not accessible, the call to API will
pass successfully. Do not forget to monitor your probe healthcheck to
verify if Redis repository is healthy. You can find health endpoints
here: link:{{
*/apim/3.x/apim\_installguide\_rest\_apis\_technical\_api.html#endpoints*
| relative\_url }}\[Installation Guide\]
