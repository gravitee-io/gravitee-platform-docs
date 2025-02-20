---
description: >-
  This article walks through how to configure the Gravitee API Management
  Console
---

# Management Console

## Introduction

The Gravitee APIM console is a graphical user interface to configure gateways, create APIs, design policies, and publish documentation. Every action in the APIM Management Console is tied to a REST API that can be accessed outside of the interface.

This article walks through how to configure the Gravitee APIM Console using:

* The `constants.json` file
* The values stored in the Management repository

You can use both together. The `constants.json` file overrides the repository configuration. For example, you can centralize all your configuration in the repository and override the `portal.entrypoint` with the `constants.json` file value to specify different values for different datacenters.

The only mandatory value in the `constants.json` file is:

```
{
  "baseURL": "gravitee_management_api_url"
}
```

This value describes where the APIM API Management endpoint is and must be set so that the APIM Console can send requests to the endpoint.

## Default configuration

The default configuration is available [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-console-webui/constants.json).

## Configuration endpoints

The following sections walk through the various Configuration endpoints.

### Organization settings

The following endpoint retrieves the organization configuration stored in the Management repository: `GET /management/organizations/{organizationId}/settings`

The following endpoint updates this configuration: `POST /management/organizations/{organizationId}/settings`

You must provide the complete JSON body shown below to update the configuration. Otherwise, default values are stored.

```
{
  "email" : {
    "enabled" : false,
    "host" : "smtp.my.domain",
    "port" : 587,
    "username" : "user@my.domain",
    "password" : "password",
    "protocol" : "smtp",
    "subject" : "[Gravitee.io] %s",
    "from" : "noreply@my.domain",
    "properties" : {
      "auth" : false,
      "startTlsEnable" : false,
      "sslTrust" : ""
    }
  },
  "alert" : {
    "enabled" : false
  },
  "authentication" : {
    "google" : {
      "clientId" : "googleplus_clientid"
    },
    "github" : {
      "clientId" : "github_clientId"
    },
    "oauth2" : {
      "clientId" : "oauth2_clientId"
    },
    "localLogin" : {
      "enabled" : true
    }
  },
  "cors" : {
    "allowOrigin" : [ "*" ],
    "allowHeaders" : [ "Cache-Control", "Pragma", "Origin", "Authorization", "Content-Type", "X-Requested-With", "If-Match", "X-Xsrf-Token", "X-Recaptcha-Token" ],
    "allowMethods" : [ "OPTIONS", "GET", "POST", "PUT", "DELETE", "PATCH" ],
    "exposedHeaders" : [ "ETag", "X-Xsrf-Token" ],
    "maxAge" : 1728000
  },
  "reCaptcha" : {
    "enabled" : false,
    "siteKey" : ""
  },
  "scheduler" : {
    "tasks" : 10,
    "notifications" : 10
  },
  "logging" : {
    "maxDurationMillis" : 0,
    "audit" : {
      "enabled" : false,
      "trail" : {
        "enabled" : false
      }
    },
    "user" : { }
  },
  "maintenance" : {
    "enabled" : false
  },
  "management" : {
    "support" : {
      "enabled" : true
    },
    "title" : "Gravitee.io Management",
    "url" : "",
    "userCreation" : {
      "enabled" : true
    },
    "automaticValidation" : {
      "enabled" : true
    }
  },
  "newsletter" : {
    "enabled" : true
  },
  "theme" : {
    "name" : "default",
    "logo" : "themes/assets/GRAVITEE_LOGO1-01.png",
    "loader" : "assets/gravitee_logo_anim.gif"
  }
}
```

### Environment settings

The following endpoint retrieves the organization configuration stored in the Management repository: `GET /management/organizations/{organizationId}/environments/{environmentId}/settings`

The following endpoint updates this configuration: `POST /management/organizations/{organizationId}/environments/{environmentId}/settings`

You must provide the complete JSON body shown below to update the configuration. Otherwise, default values are stored.

```
{
  "email" : {
    "enabled" : false,
    "host" : "smtp.my.domain",
    "port" : 587,
    "username" : "user@my.domain",
    "password" : "password",
    "protocol" : "smtp",
    "subject" : "[Gravitee.io] %s",
    "from" : "noreply@my.domain",
    "properties" : {
      "auth" : false,
      "startTlsEnable" : false,
      "sslTrust" : ""
    }
  },
  "analytics" : {
    "clientTimeout" : 30000
  },
  "api" : {
    "labelsDictionary" : [ ]
  },
  "apiQualityMetrics" : {
    "enabled" : false,
    "functionalDocumentationWeight" : 0,
    "technicalDocumentationWeight" : 0,
    "descriptionWeight" : 0,
    "descriptionMinLength" : 100,
    "logoWeight" : 0,
    "categoriesWeight" : 0,
    "labelsWeight" : 0,
    "healthcheckWeight" : 0
  },
  "apiReview" : {
    "enabled" : false
  },
  "application" : {
    "registration" : {
      "enabled" : true
    },
    "types" : {
      "simple" : {
        "enabled" : true
      },
      "browser" : {
        "enabled" : true
      },
      "web" : {
        "enabled" : true
      },
      "native" : {
        "enabled" : true
      },
      "backend_to_backend" : {
        "enabled" : true
      }
    }
  },
  "authentication" : {
    "google" : {
      "clientId" : "googleplus_clientid"
    },
    "github" : {
      "clientId" : "github_clientId"
    },
    "oauth2" : {
      "clientId" : "oauth2_clientId"
    },
    "forceLogin" : {
      "enabled" : false
    },
    "localLogin" : {
      "enabled" : true
    }
  },
  "company" : {
    "name" : "Gravitee.io"
  },
  "cors" : {
    "allowOrigin" : [ "*" ],
    "allowHeaders" : [ "Cache-Control", "Pragma", "Origin", "Authorization", "Content-Type", "X-Requested-With", "If-Match", "X-Xsrf-Token", "X-Recaptcha-Token" ],
    "allowMethods" : [ "OPTIONS", "GET", "POST", "PUT", "DELETE", "PATCH" ],
    "exposedHeaders" : [ "ETag", "X-Xsrf-Token" ],
    "maxAge" : 1728000
  },
  "dashboards" : {
    "apiStatus": {
      "enabled": true
    }
  },
  "documentation" : {
    "url" : "https://docs.gravitee.io"
  },
  "openAPIDocViewer" : {
    "openAPIDocType" : {
      "swagger" : {
        "enabled" : true
      },
      "redoc" : {
        "enabled" : true
      },
      "defaultType" : "Swagger"
    }
  },
  "plan" : {
    "security" : {
      "apikey" : {
        "enabled" : true
      },
      "customApiKey" : {
        "enabled" : false
      },
      "oauth2" : {
        "enabled" : true
      },
      "keyless" : {
        "enabled" : true
      },
      "jwt" : {
        "enabled" : true
      }
    }
  },
  "portal" : {
    "entrypoint" : "https://api.company.com",
    "apikeyHeader" : "X-Gravitee-Api-Key",
    "support" : {
      "enabled" : true
    },
    "url" : "",
    "apis" : {
      "tilesMode" : {
        "enabled" : true
      },
      "categoryMode" : {
        "enabled" : true
      },
      "apiHeaderShowTags" : {
        "enabled" : true
      },
      "apiHeaderShowCategories" : {
        "enabled" : true
      }
    },
    "analytics" : {
      "enabled" : false,
      "trackingId" : ""
    },
    "rating" : {
      "enabled" : true,
      "comment" : {
        "mandatory" : false
      }
    },
    "userCreation" : {
      "enabled" : true,
      "automaticValidation" : {
        "enabled" : true
      }
    },
    "uploadMedia" : {
      "enabled" : true,
      "maxSizeInOctet" : 1000000
    }
  },
  "reCaptcha" : {
    "enabled" : false,
    "siteKey" : ""
  },
  "scheduler" : {
    "tasks" : 10,
    "notifications" : 10
  }
}
```

### Dashboard

Gravitee comes with two Dashboards, each being configurable:

* Home
* API Status

#### Home

The Home dashboard is the default page users see when they first log in to APIM Console, or when they select the **Dashboard** menu option. You can configure the Home dashboard by modifying `home.json`.

This file is located in the `/dashboards` folder of the Management API distribution folder.

To customize the Home dashboard you can either modify this file or specify a new folder in the `gravitee.yml` file:

```
# Console dashboards
console:
  dashboards:
    path: ${gravitee.home}/dashboards
```

By default, this section is commented out and the path is `${gravitee.home}/dashboards`

Charts are generated with [Highcharts](https://api.highcharts.com/highcharts/). You can use the Highchart documentation to help you define the `chart` section of the JSON objects.

For example:

```
[
  {
    "row": 0,
    "col": 0,
    "sizeY": 1,
    "sizeX": 1,
    "title": "Number of APIs",
    "chart": {
      "type": "count",
      "data": [
        {
          "key": "count",
          "label": "total",
          "color": "#42a5f5"
        }
      ],
      "request": {
        "type": "count",
        "field": "api"
      }
    }
  },
  ...
]
```

#### API Status

The api status page is a panel in the dashboard that displays the status of all APIs.

The tab is enabled by default, but depending on the number of APIs, it may take a while to load. You can disable it in your Gateway settings. [Please refer to this documentation to learn more about dashboards.](../../managing-your-apis/api-measurement-tracking-and-analytics/create-a-dashboard.md)
