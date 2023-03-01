# Setup

Before you can get into the actual installation, a couple of things need
to be set up

1.  **Docker**

    Is assumed to be installed.

2.  **Persistence**

    Containers are great, but you do want persistence in case they need
    to be restarted. You are going to persist the MongoDB data, the
    Elasticsearch data and provide locations for additional plugins
    (both for the Gateway and the REST API). It is assumed in this page
    that these will live under a filesystem mounted at `/gravitee` on
    the host system.

        mkdir /gravitee/mongodb
        mkdir /gravitee/mongodb/data
        mkdir /gravitee/elasticsearch
        mkdir /gravitee/elasticsearch/data
        mkdir /gravitee/apim-gateway
        mkdir /gravitee/apim-gateway/plugins
        mkdir /gravitee/apim-gateway/logs
        mkdir /gravitee/apim-management-api
        mkdir /gravitee/apim-management-api/plugins
        mkdir /gravitee/apim-management-api/logs
        mkdir /gravitee/apim-management-ui
        mkdir /gravitee/apim-management-ui/logs
        mkdir /gravitee/apim-portal-ui
        mkdir /gravitee/apim-portal-ui/logs

3.  **Network**

    To provide an easy way for the containers to **talk** in this setup,
    create two docker networks. One for **storage** communication, one
    for **frontend** communication. The combination of this network and
    giving names to the containers will allow you to specify connections
    easily.

        docker network create graviteestorage
        docker network create graviteefrontend

4.  **License**

    The Enterprise installation assumes you have a license. For more
    information on getting one, check <https://www.gravitee.io/pricing>.
    It is assumed below that you have a `/gravitee/license.key` file.

As was indicated before, your architecture may differ and thus require a
different setup.

# Install MongoDB

<table>
<caption>Assumptions</caption>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>container</p></td>
<td style="text-align: left;"><p><a
href="https://hub.docker.com/_/mongo">MongoDB^</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>network</p></td>
<td
style="text-align: left;"><p><strong>graviteestorage</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>persistence</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/mongodb/data</strong></p></td>
</tr>
</tbody>
</table>

Assumptions

**Instructions**

    docker pull mongo:3.6
    docker run --name gravitee-mongo \
      --net graviteestorage \
      --volume /gravitee/mongodb/data:/data/db \
      --detach mongo:3.6

# Install Elasticsearch

<table>
<caption>Assumptions</caption>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>container</p></td>
<td style="text-align: left;"><p><a
href="https://hub.docker.com/_/elasticsearch">Elasticsearch^</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>network</p></td>
<td
style="text-align: left;"><p><strong>graviteestorage</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>persistence</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/elasticsearch/data</strong></p></td>
</tr>
</tbody>
</table>

Assumptions

**Instructions**

    docker pull docker.elastic.co/elasticsearch/elasticsearch:7.7.0
    docker run --name gravitee-elasticsearch \
      --net graviteestorage \
      --env http.host=0.0.0.0 \
      --env transport.host=0.0.0.0 \
      --env xpack.security.enabled=false \
      --env xpack.monitoring.enabled=false \
      --env cluster.name=gravitee-elasticsearch \
      --env bootstrap.memory_lock=true \
      --env discovery.type=single-node \
      --env "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
      --volume /gravitee/elasticsearch/data:/usr/share/elasticsearch/data \
      --detach docker.elastic.co/elasticsearch/elasticsearch:7.7.0

# Install API Management Gateway

<table>
<caption>Assumptions</caption>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>container</p></td>
<td style="text-align: left;"><p><a
href="https://hub.docker.com/r/graviteeio/apim-gateway">Gateway^</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>network</p></td>
<td
style="text-align: left;"><p><strong>graviteestorage</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>network</p></td>
<td
style="text-align: left;"><p><strong>graviteefrontend</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>persistence</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/apim-gateway/plugins</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>persistence</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/apim-gateway/logs</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>license</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/license.key</strong></p></td>
</tr>
</tbody>
</table>

Assumptions

**Instructions**

    docker pull graviteeio/apim-gateway:{{ site.products.apim._3x.version }}-ee

    docker run --publish 8082:8082 \
      --volume /gravitee/apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext \
      --volume /gravitee/apim-gateway/logs:/opt/graviteeio-gateway/logs \
      --volume /gravitee/license.key:/opt/graviteeio-gateway/license/license.key \
      --env gravitee_management_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_ratelimit_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_reporters_elasticsearch_endpoints_0="http://gravitee-elasticsearch:9200" \
      --env gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins \
      --env gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext \
      --net graviteestorage \
      --name gravitee-apim-gateway \
      --detach graviteeio/apim-gateway:{{ site.products.apim._3x.version }}-ee

    docker network connect graviteefrontend gravitee-apim-gateway

# Install API Management REST API

<table>
<caption>Assumptions</caption>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>container</p></td>
<td style="text-align: left;"><p><a
href="https://hub.docker.com/r/graviteeio/apim-management-api">REST
API^</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>network</p></td>
<td
style="text-align: left;"><p><strong>graviteestorage</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>network</p></td>
<td
style="text-align: left;"><p><strong>graviteefrontend</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>persistence</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/apim-management-api/plugins</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>persistence</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/apim-management-api/logs</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>license</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/license.key</strong></p></td>
</tr>
</tbody>
</table>

Assumptions

**Instructions**

    docker pull graviteeio/apim-management-api:{{ site.products.apim._3x.version }}-ee

    docker run --publish 8083:8083 \
      --volume /gravitee/apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext \
      --volume /gravitee/apim-management-api/logs:/opt/graviteeio-management-api/logs \
      --volume /gravitee/license.key:/opt/graviteeio-management-api/license/license.key \
      --env gravitee_management_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_analytics_elasticsearch_endpoints_0="http://gravitee-elasticsearch:9200" \
      --env gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins \
      --env gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext \
      --net graviteestorage \
      --name gravitee-apim-management-api \
      --detach graviteeio/apim-management-api:{{ site.products.apim._3x.version }}-ee

    docker network connect graviteefrontend gravitee-apim-management-api

# Install API Management Management UI

<table>
<caption>Assumptions</caption>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>container</p></td>
<td style="text-align: left;"><p><a
href="https://hub.docker.com/r/graviteeio/apim-management-ui">Management
UI^</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>network</p></td>
<td
style="text-align: left;"><p><strong>graviteefrontend</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>persistence</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/apim-management-ui/logs</strong></p></td>
</tr>
</tbody>
</table>

Assumptions

**Instructions**

    docker pull graviteeio/apim-management-ui:latest
    docker run --publish 8084:8080 \
      --volume /gravitee/apim-management-ui/logs:/var/log/nginx \
      --net graviteefrontend \
      --name gravitee-apim-management-ui \
      --env MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT \
      --detach graviteeio/apim-management-ui:latest

# Install API Management Portal UI

<table>
<caption>Assumptions</caption>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>container</p></td>
<td style="text-align: left;"><p><a
href="https://hub.docker.com/r/graviteeio/apim-portal-ui">Portal
UI^</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>network</p></td>
<td
style="text-align: left;"><p><strong>graviteefrontend</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>persistence</p></td>
<td
style="text-align: left;"><p><strong>/gravitee/apim-portal-ui/logs</strong></p></td>
</tr>
</tbody>
</table>

Assumptions

**Instructions**

    docker pull graviteeio/apim-portal-ui:latest
    docker run --publish 8085:8080 \
      --volume /gravitee/apim-portal-ui/logs:/var/log/nginx \
      --net graviteefrontend \
      --name gravitee-apim-portal-ui \
      --env PORTAL_API_URL=http://localhost:8083/portal/environments/DEFAULT \
      --detach graviteeio/apim-portal-ui:latest
