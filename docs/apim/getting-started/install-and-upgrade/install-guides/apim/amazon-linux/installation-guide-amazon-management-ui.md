# Install Management UI

## Prerequisites

* Machine up and running
* Gravitee YUM repository added
* Gravitee APIM REST API installed and running
* Nginx installed

## Security group

* open port 8084

## Instructions

1. Install Management UI:

```
sudo yum install graviteeio-apim-management-ui-3x -y
```

2. Restart Nginx:

```
sudo systemctl restart nginx
```

3. Verify:

```
sudo ss -lntp '( sport = 8084 )'
```

```
You should see that there’s a process listening on that port.
```

!!! note

```
The Management UI package does not provide its own service. It provides:

- A javascript application that can be found at `/opt/graviteeio/apim/management-ui`.
- An Nginx configuration that can be found at `/etc/nginx/conf.d/graviteeio-apim-management-ui.conf`.
```

## Next steps

The next step is [installing the Gravitee APIM Portal UI](installation-guide-amazon-portal-ui.md).
