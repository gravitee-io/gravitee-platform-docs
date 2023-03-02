---
title: APIM Installation Guide - Amazon Linux - Fixing a known post-installation issue
tags:
  - APIM
  - Installation
  - Known issue
  - Fix
---

# Fixing a known post-installation issue

## Known issue description

There is currently a known issue in the Portal UI configuration. After installation, the `baseURL` in `/opt/graviteeio/apim/portal-ui/assets/config.json` is incorrect, as shown below:

![Incorrect baseURL in Portal UI configuration](/images/apim/3.x/installation/amazon-known-issues/portal-ui-known-issue.png)

!!! note

    Obviously your actual IP will differ from the one shown in this example.

## Fix

To fix this issue:

1. Remove the <http://localhost:8083> from the `baseURL`:
  ```
  sudo perl -pi -e 's/"baseURL": "http:\/\/localhost:8083/"baseURL": "/g' /opt/graviteeio/apim/portal-ui/assets/config.json
  ```
2. Restart Nginx:
  ```
  sudo systemctl restart nginx
  ```
