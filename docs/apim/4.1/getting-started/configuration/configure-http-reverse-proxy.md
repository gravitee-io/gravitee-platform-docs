# Configure HTTP Reverse Proxy

Here is a simple example of APIM components configuration with docker-compose.

## APIM configuration

For this example, we use a `docker-compose.yml` file to configure each APIM component

```yaml
version: '3.5'

networks:
  frontend:
    name: frontend
  storage:
    name: storage

volumes:
  data-elasticsearch:
  data-mongo:

services:

  mongodb:
    image: mongo:${MONGODB_VERSION:-6.0}
    container_name: gio_apim_mongodb
    restart: always
    volumes:
      - data-mongo:/data/db
      - ./.logs/apim-mongodb:/var/log/mongodb
    networks:
      - storage

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION:-8.9.0}
    container_name: gio_apim_elasticsearch
    restart: always
    volumes:
      - data-elasticsearch:/usr/share/elasticsearch/data
    environment:
      - http.host=0.0.0.0
      - transport.host=0.0.0.0
      - xpack.security.enabled=false
      - xpack.monitoring.enabled=false
      - cluster.name=elasticsearch
      - bootstrap.memory_lock=true
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile: 65536
    networks:
      - storage

  gateway:
    image: graviteeio/apim-gateway:${APIM_VERSION:-latest}
    container_name: gio_apim_gateway
    restart: always
    depends_on:
      - mongodb
      - elasticsearch
    volumes:
      - ./.logs/apim-gateway:/opt/graviteeio-gateway/logs
    environment:
      - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_ratelimit_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_reporters_elasticsearch_endpoints_0=http://elasticsearch:9200
    networks:
      - storage
      - frontend

  management_api:
    image: graviteeio/apim-management-api:${APIM_VERSION:-latest}
    container_name: gio_apim_management_api
    restart: always
    links:
      - mongodb
      - elasticsearch
    depends_on:
      - mongodb
      - elasticsearch
    volumes:
      - ./.logs/apim-management-api:/opt/graviteeio-management-api/logs
    environment:
      - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
      - console_ui_url=http://localhost/console
      - console_api_url=http://localhost/management
      - portal_ui_url=http://localhost/
    networks:
      - storage
      - frontend

  management_ui:
    image: graviteeio/apim-management-ui:${APIM_VERSION:-latest}
    container_name: gio_apim_management_ui
    restart: always
    depends_on:
      - management_api
    environment:
      - MGMT_API_URL=/management/organizations/DEFAULT/environments/DEFAULT/
    volumes:
      - ./.logs/apim-management-ui:/var/log/nginx
    networks:
      - frontend

  portal_ui:
    image: graviteeio/apim-portal-ui:${APIM_VERSION:-latest}
    container_name: gio_apim_portal_ui
    restart: always
    depends_on:
      - management_api
    environment:
      - PORTAL_API_URL=/portal/environments/DEFAULT
    volumes:
      - ./.logs/apim-portal-ui:/var/log/nginx
    networks:
      - frontend
```

## NGINX

Add the location for each gravitee components, define :

1. Management API under Console UI
2. Portal API under Portal UI

Don’t forget to add the `sub_filter` directives according to the locations.

```
http {
        include /etc/nginx/mime.types;

        resolver 127.0.0.1 ipv6=off;

        upstream apim-gateway {
            server gateway:8082;
        }

        upstream apim-management-api {
            server management_api:8083;
        }

        upstream apim-management-ui {
            server management_ui:8080;
        }

        upstream apim-portal-dev {
            server portal_ui:8080;
        }

        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
        proxy_set_header   X-Forwarded-Proto $scheme;

        server {
            listen 80;

            location /gateway/ {
                proxy_pass http://apim-gateway/;
            }

            location /management {
                proxy_pass http://apim-management-api/management/;
            }

            location /console/ {
                proxy_pass http://apim-management-ui/;
                sub_filter_once  on;
                sub_filter  '<base href="/' '<base href="/console/';
            }

            location /portal/ {
                proxy_pass http://apim-management-api/portal/;
                sub_filter_once  on;
                sub_filter  '<base href="/' '<base href="/portal/';
            }

            location / {
                proxy_pass http://apim-portal-dev/;
            }

            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root /usr/share/nginx/html;
            }
        }
}
```

### Nginx container

Add Nginx container to `docker-compose.yml`

```yaml
  nginx:
    image: nginx:latest
    container_name: nginx
    restart: unless-stopped
    depends_on:
      - management_ui
      - portal_ui
    ports:
      - "80:80"
    volumes:
      - ./conf/nginx.conf:/etc/nginx/nginx.conf
    networks:
      - frontend
```

After restart, you can access your components through nginx at the following addresses

| Component      | URL                          |
| -------------- | ---------------------------- |
| Gateway        | http://localhost/gateway/    |
| Management API | http://localhost/management/ |
| Portal API     | http://localhost/portal/     |
| Console UI     | http://localhost/console/    |
| Portal UI      | http://localhost/            |
