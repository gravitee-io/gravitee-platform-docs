# Full stack installation

## Prerequisites

* Machine up and running

## Security group

* open port 8082
* open port 8083
* open port 8084
* open port 8085

## Instructions

1. Install all the prerequisites and Gravitee APIM components:

```
curl -L https://bit.ly/install-apim-3x | sudo bash
```

2. Fix a known post-installation issue. There is a known issue with the Portal UI configuration. You can find a fix [here](installation-guide-amazon-issue.md).
3. Verify:

```
sudo ss -lntp '( sport = 9200 )'
sudo ss -lntp '( sport = 27017 )'
sudo ss -lntp '( sport = 8082 )'
sudo ss -lntp '( sport = 8083 )'
sudo ss -lntp '( sport = 8084 )'
sudo ss -lntp '( sport = 8085 )'
```

```
You should see that there are processes listening on those ports.
```

4\. Verify some more:

```
curl -X GET http://localhost:8082/
curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

```
If the installation is successful the first one returns: **No context-path matches the request URI.** The others return a json structure.
```

**Congratulations**, you have a fully functional Gravitee APIM!
