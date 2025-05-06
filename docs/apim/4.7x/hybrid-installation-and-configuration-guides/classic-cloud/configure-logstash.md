# Configure Logstash

## Compatibility with Elasticsearch

Support versions: Please refer to the [compatibility matrix with Elasticsearch](https://www.elastic.co/support/matrix#matrix_compatibility).

## Kubernetes

1. Install Logstash. To install Logstash, go to either of the following websites:

* [Official Helm charts](https://artifacthub.io/packages/helm/elastic/logstash#how-to-install-oss-version-of-logstash)
* [Bitnami Helm charts](https://bitnami.com/stack/logstash/helm)

2. Configure Logstash by coping the following file:

{% code title="values.yaml" lineNumbers="true" %}
```yaml
gateway:
  reporters:
    elasticsearch:
      enabled: false
    tcp:
      enabled: true
      host: logstash-host
      port: 8379
      output: elasticsearch
```
{% endcode %}

## Docker

1. Install Logstash. To install Logstash, copy the following file:&#x20;

{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

services:
  logstash:
    # https://www.docker.elastic.co/r/logstash/logstash-oss 
    image: docker.elastic.co/logstash/logstash-oss:${LOGSTASH_VERSION:-8.10.2}
    container_name: gio_apim_hybrid_logstash
    hostname: logstash
    ports:
      - "8379:8379"
    healthcheck:
      test: curl -f -I http://localhost:9600/_node/pipelines/main || exit 1
      start_period: 20s
      interval: 3s
      timeout: 5s
      retries: 30
    volumes:
      - ./config/logstash:/usr/share/logstash/pipeline:ro
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
```
{% endcode %}

2. Configure Logstash by copying the following file:

{% code title="docker-compose.yaml" overflow="wrap" lineNumbers="true" %}
```yaml
version: '3'

services:
  gateway:
    image: graviteeio/apim-gateway:<VERSION-ALIGNED-WITH-CONTROL-PLANE>
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
    environment:
      # --- LOGSTASH ---
      - gravitee_reporters_elasticsearch_enabled=false
      - gravitee_reporters_tcp_enabled=true
      - gravitee_reporters_tcp_host=logstash-host
      - gravitee_reporters_tcp_port=8379
      - gravitee_reporters_tcp_output=elasticsearch
```
{% endcode %}

## .ZIP

1. Install Logstash. To install Logstash, go to [Download Logstash - OSS only](https://www.elastic.co/downloads/logstash-oss).
2. Configure Logstash by copying the following file:

{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
reporters:
  elasticsearch:
    enabled: false
  tcp:
    enabled: true
    host: logstash-host
    port: 8379
    output: elasticsearch
```
{% endcode %}

{% hint style="info" %}
For more information about configuring Logstash, see [Configuring Logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html).
{% endhint %}

To configure Logstash for you environment, copy the following example:

{% code title="logstash.conf" lineNumbers="true" %}
```
input {
  tcp {
      port => 8379
      codec => "json_lines"
  }
}

filter {
    if [type] != "request" or [type] != "v4-metrics" {
        mutate { remove_field => ["path", "host"] }
    }
}

output {
  s3 {
    access_key_id => "${S3_ACEESS_KEY_ID}"
    secret_access_key => "${S3_SECRET_ACCESS_KEY}"
    region => "${S3_REGION}"
    bucket => "${S3_BUCKET_NAME}"
    rotation_strategy => time
    time_file => 1
    codec => "json_lines"
  }
}
```
{% endcode %}
