# Logstash

## Overview

You can configure Logstash to send data to ElasticSearch. To configure Logstash, follow the steps for one of the following deployment types:

* [#kubernetes](logstash.md#kubernetes "mention")
* [#docker](logstash.md#docker "mention")
* [#zip](logstash.md#zip "mention")

### Compatibility with Elasticsearch

Support versions: Please refer to the [compatibility matrix with Elasticsearch](https://www.elastic.co/support/matrix#matrix_compatibility).

## Kubernetes

1. Install Logstash. To install Logstash, go to [Official Helm charts](https://artifacthub.io/packages/helm/elastic/logstash#how-to-install-oss-version-of-logstash).
2. Configure the Logstash helm chart with the following values:

```json
image: "docker.elastic.co/logstash/logstash"  
imageTag: "8.5.3"                                                                                                              
extraPorts:                                                                                                                    
  - name: tcp-input                    
    containerPort: 8379                                                                                                                                     
service:                                 
  type: ClusterIP                       
  ports:                                      
    - name: tcp-input                                                                                                          
      port: 8379                                                                                                               
      protocol: TCP                                      
      targetPort: 8379                 
replicas: 1                                              
resources:                                                                                                                     
  requests:                                  
    cpu: "300m"                          
    memory: "2048Mi"                                   
  limits:                                                                                                                      
    cpu: "400m"                     
    memory: "2048Mi"
    
logstashConfig:                                 
  logstash.yml: |                                  
    http.host: 0.0.0.0                 
    xpack.monitoring.enabled: false                                                                                                                                                                                                                            
    pipeline.ecs_compatibility: disabled
    path.config: /usr/share/logstash/pipeline
    queue.type: persisted
    queue.max_bytes: 512mb
  
logstashPipeline:
  logstash.conf: |
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
        access_key_id => "${S3_ACCESS_KEY_ID}"
        secret_access_key => "${S3_SECRET_ACCESS_KEY}"
        region => "${S3_REGION}"
        bucket => "${S3_BUCKET_NAME}"
        rotation_strategy => time
        time_file => 1
        codec => "json_lines"
      }
    }
```

3. In your gateway `values.yaml` file, configure the TCP reporter to push the analytics to Logstash using the following example:

{% code title="values.yaml" lineNumbers="true" %}
```yaml
gateway:
  reporters:
    elasticsearch:
      enabled: false
    tcp:
      enabled: true
      host: logstash-logstash
      port: 8379
      output: elasticsearch
```
{% endcode %}

## Docker

1. Create a `logstash.conf` file and a `logstash.yml` file in your local **config** directory. Here are examples of a `logstash.conf` file and a `logstash.yml` file.

```json
# logstash.conf

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
    access_key_id => "${S3_ACCESS_KEY_ID}"
    secret_access_key => "${S3_SECRET_ACCESS_KEY}"
    region => "${S3_REGION}"
    bucket => "${S3_BUCKET_NAME}"
    rotation_strategy => time
    time_file => 1
    codec => "json_lines"
  }
}
```

```yaml
# pipeline.yml
    
http.host: 0.0.0.0                                                                                                                                                                                                                                            
pipeline.ecs_compatibility: disabled
path.config: /usr/share/logstash/pipeline
queue.type: persisted
queue.max_bytes: 512mb
```

2. To install Logstash, copy the following file or append it to your current docker-compose manifest:&#x20;

{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

services:
  logstash:
    # https://www.docker.elastic.co/r/logstash/logstash-oss 
    image: docker.elastic.co/logstash/logstash-oss:${LOGSTASH_VERSION:-8.10.2}
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
      - ./config/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
      - ./config/pipeline.yml:/usr/share/logstash/config/logstash.yml
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
```
{% endcode %}

3. In your `docker-compose.yaml` file, configure the TCP reporter to push the analytics to Logstash using the following example:

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
      - gravitee_reporters_tcp_host=logstash
      - gravitee_reporters_tcp_port=8379
      - gravitee_reporters_tcp_output=elasticsearch
```
{% endcode %}

## .ZIP

1. Install Logstash. To install Logstash, go to [Download Logstash - OSS only](https://www.elastic.co/downloads/logstash-oss).
2. Configure Logstash using the following logstash.conf file:

{% code title="logstash.conf" lineNumbers="true" %}
```json
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
    access_key_id => "${S3_ACCESS_KEY_ID}"
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

3. In your `gravitee.yaml` file, configure the TCP reporter to push the analytics to Logstash using the following example:

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
For more information about configuring logstash, see [Configuring Logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html).
{% endhint %}
