---
title: APIM Installation Guide - Amazon Linux - Prerequisites - Install Nginx
tags:
  - APIM
  - Installation
  - Prerequisites
  - Amazon
  - Nginx
---

# Prerequisite - Install Nginx

## Overview

Both Gravitee APIM user interfaces (console and developer portal) use Nginx as their webserver. Follow the instructions below to set up Nginx.

For more information, see the [Nginx Installation documentation](https://nginx.org/en/linux_packages.html#Amazon-Linux).

## Instructions

1. Create a file called `/etc/yum.repos.d/nginx.repo`:

```
  sudo tee -a /etc/yum.repos.d/nginx.repo <<EOF
  [nginx-stable]
  name=nginx stable repo
  baseurl=http://nginx.org/packages/amzn2/\$releasever/\$basearch/
  gpgcheck=1
  enabled=1
  gpgkey=https://nginx.org/keys/nginx_signing.key
  module_hotfixes=true
  EOF
```

2. Install Nginx:

```
  sudo yum install nginx -y
```

3. Enable Nginx on startup:

```
  sudo systemctl daemon-reload
  sudo systemctl enable nginx
```

4. Start Nginx:

```
  sudo systemctl start nginx
```

5. Verify:

```
  sudo ss -lntp '( sport = 80 )'
```

You should see that there is a process listening on that port.

## Next steps

You are done with the prerequisites!

The next steps are [installing the Gravitee APIM Gateway](installation-guide-amazon-gateway.md) and [installing all the Gravitee APIM components](installation-guide-amazon-all.md).
