# Prerequisite - Install Elasticsearch

## Overview

Gravitee APIM uses Elasticsearch as a default reporting and analytics repository. Follow the instructions below to set up Elasticsearch.

For more information, see the [Elasticsearch installation documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#rpm-repo).

## Instructions

1. Create a file called `/etc/yum.repos.d/elasticsearch.repo`:

```
  sudo tee -a /etc/yum.repos.d/elasticsearch.repo <<EOF
  [elasticsearch]
  name=Elasticsearch repository for 7.x packages
  baseurl=https://artifacts.elastic.co/packages/7.x/yum
  gpgcheck=1
  gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
  enabled=0
  autorefresh=1
  type=rpm-md
  EOF
```

2. Install Elasticsearch:

```
  sudo yum install --enablerepo=elasticsearch elasticsearch -y
```

3. Enable Elasticsearch on startup:

```
  sudo systemctl daemon-reload
  sudo systemctl enable elasticsearch.service
```

4. Start Elasticsearch:

```
sudo systemctl start elasticsearch.service
```

5. Verify:

```
  sudo ss -lntp '( sport = 9200 )'
```

You should see that there is a process listening on that port.

## Next steps

The next step is [installing Nginx](installation-guide-amazon-prerequisite-nginx.md).
