# All

## Prerequisites

* Machine up and running
* Gravitee YUM repository added
* Java 11 jre installed
* MongoDB installed and running
* Elasticsearch installed and running
* Nginx installed

## Security group

* open port 8082
* open port 8083
* open port 8084
* open port 8085

## Instructions

1. Install all Gravitee APIM components:

```
sudo yum install graviteeio-apim-3x -y
```

2. Enable Gateway and REST API on startup:

```
sudo systemctl daemon-reload
sudo systemctl enable graviteeio-apim-gateway
sudo systemctl enable graviteeio-apim-rest-api
```

3. Start Gateway and REST API:

```
sudo systemctl start graviteeio-apim-gateway
sudo systemctl start graviteeio-apim-rest-api
```

4. Restart Nginx:

```
sudo systemctl restart nginx
```

5. Fix an issue. There is a known issue with the Portal UI configuration. You can find a fix [here](https://docs.gravitee.io/apim/3.x/apim\_installation\_guide\_amazon\_issue.html).
6. Verify:

```
sudo journalctl -f
```

Follow along with the startup process. If any of the prerequisites is missing, this is were you’ll get error messages.

**NOTE:** You can also see the same in `/opt/graviteeio/apim/gateway/logs/gravitee.log` and `/opt/graviteeio/apim/rest-api/logs/gravitee.log`

7. Verify some more:

```
sudo ss -lntp '( sport = 8082 )'
sudo ss -lntp '( sport = 8083 )'
sudo ss -lntp '( sport = 8084 )'
sudo ss -lntp '( sport = 8085 )'
```

You should see that there are processes listening on those ports.

8. Verify some more still:

```
curl -X GET http://localhost:8082/
curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

If the installation is successful the first one returns: **No context-path matches the request URI.** The others return a JSON structure.
