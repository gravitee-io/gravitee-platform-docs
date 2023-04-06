# Prerequisite - Install MongoDB

## Overview

Gravitee APIM uses MongoDB as its default repository to store global configurations. Follow the instructions below to set up MongoDB.

For more information, see the [MongoDB Installation documentation](https://docs.mongodb.com/v3.6/tutorial/install-mongodb-on-amazon).

## Instructions

1. Create a file called `/etc/yum.repos.d/mongodb-org-3.6.repo`:

```
  sudo tee -a /etc/yum.repos.d/graviteeio.repo <<EOF
  [mongodb-org-3.6]
  name=MongoDB Repository
  baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.6/x86_64/
  gpgcheck=1
  enabled=1
  gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc
  EOF
```

2. Install MongoDB:

```
  sudo yum install mongodb-org -y
```

3. Enable MongoDB on startup:

```
  sudo systemctl daemon-reload
  sudo systemctl enable mongod
```

4. Start MongoDB:

```
  sudo systemctl start mongod
```

5. Verify:

```
sudo ss -lntp '( sport = 27017 )'
```

You should see that there is a process listening on that port.

## Next steps

The next step is [installing Elasticsearch](installation-guide-amazon-prerequisite-elasticsearch.md).
