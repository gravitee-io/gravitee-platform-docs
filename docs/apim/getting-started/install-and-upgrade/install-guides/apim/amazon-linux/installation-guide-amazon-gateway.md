---
title: APIM Installation Guide - Amazon Linux - APIM Component - Install Gateway
tags:
  - APIM
  - Installation
  - APIM component
  - Amazon
  - Gateway
---

# APIM Component - Install Gateway

## Prerequisites

- Machine up and running
- Gravitee YUM repository added
- Java 11 jre installed
- MongoDB installed and running
- Elasticsearch installed and running

## Security group

- open port 8082

## Instructions

1. Install Gateway:
  ```
  sudo yum install graviteeio-apim-gateway-3x -y
  ```
2. Enable Gateway on startup:
  ```
  sudo systemctl daemon-reload
  sudo systemctl enable graviteeio-apim-gateway
  ```
3. Start Gateway:
  ```
  sudo systemctl start graviteeio-apim-gateway
  ```
4. Verify:
  ```
  sudo journalctl -f
  ```
    Follow along with the startup process. If any of the prerequisites
    is missing, this is were you’ll get error messages.
    You can also see the same in `/opt/graviteeio/apim/gateway/logs/gravitee.log`.
5.  Verify some more:
  ```
  sudo ss -lntp '( sport = 8082 )'
  ```
    You should see that there’s a process listening on that port.
6.  Verify some more still:
  ```
  curl -X GET http://localhost:8082/
  ```
    If the installation is successful this returns: **No context-path
    matches the request URI.**

## Next steps

The next step is [installing the Gravitee APIM REST API](installation-guide-amazon-rest-api.md).
