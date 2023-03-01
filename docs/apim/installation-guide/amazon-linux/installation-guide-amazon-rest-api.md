---
title: APIM Installation Guide - Amazon Linux - APIM Component - Install REST API
tags:
  - APIM
  - Installation
  - Prerequisites
  - Amazon
  - REST API
---

# Install REST API

## Prerequisites

- Machine up and running
- Gravitee YUM repository added
- Java 11 jre installed
- MongoDB installed and running
- Elasticsearch installed and running

## Security group

- open port 8083

## Instructions

1. Install REST API:
  ```
  sudo yum install graviteeio-apim-rest-api-3x -y
  ```
2. Enable REST API on startup:
  ```
  sudo systemctl daemon-reload
  sudo systemctl enable graviteeio-apim-rest-api
  ```
3. Start REST API:
  ```
  sudo systemctl start graviteeio-apim-rest-api
  ```
4. Verify:
  ```
  sudo journalctl -f
  ```
    Follow along with the startup process. If any of the prerequisites is missing, this is were you’ll get error messages. You can also see the same in `/opt/graviteeio/apim/rest-api/logs/gravitee.log`.
5.  Verify some more:
  ```
  sudo ss -lntp '( sport = 8083 )'
  ```
    You should see that there’s a process listening on that port.
6.  Verify some more still:
  ```
  curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
  curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
  ```
    If the installation is successful both of these return a json
    document.

## Next steps

The next step is [installing the Gravitee APIM Management UI](installation-guide-amazon-management-ui.md).
