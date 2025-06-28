---
hidden: true
---

# Vanilla Kubernetes

## Configure Redis

Redis can be used by Gravitee for both caching and rate-limiting.

1. To install Redis, use packages available from [Bitnami Helm charts](https://artifacthub.io/packages/helm/bitnami/redis).  The following example uses a standalone configuration.
2.  Configure your Gravitee Gateway to use Redis by using the following example `values.yaml` configuration:\


    {% code title="values.yaml" lineNumbers="true" %}
    ```yaml
    gateway:
      ...
      ratelimit:
        type: redis
      redis:
        host: ${redis_hostname}
        port: ${redis_port_number}
        password: ${redis_password}
        #password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
        download: true
    ```
    {% endcode %}

## Configure Logstash

You can configure Logstash to send data to ElasticSearch.

{% hint style="info" %}
* For support versions, refer to the [compatibility matrix with Elasticsearch](https://www.elastic.co/support/matrix#matrix_compatibility).
* For more information about configuring Logstash, see [Creating a Logstash Pipeline](https://www.elastic.co/docs/reference/logstash/creating-logstash-pipeline) in the Elastic documentation.
{% endhint %}

1. Install Logstash. To install Logstash, go to [Official Helm charts](https://artifacthub.io/packages/helm/elastic/logstash#how-to-install-oss-version-of-logstash).
2.  Configure the Logstash helm chart with the following values:\


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

    &#x20;
3.  In your Gateway `values.yaml` file, configure the TCP reporter to push the analytics to Logstash using the following example:\


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

## Configure Fluentd

* Install Fluentd. To install Fluentd,  go to either of the following sites:
  * [Official Helm charts](https://artifacthub.io/packages/helm/fluent/fluentd)
  * [Bitnami Helm charts](https://bitnami.com/stack/fluentd/helm)

## Configure Alert Engine

```yaml
alerts:
  enabled: true
  endpoints:
    - https://alert-engine-url:alert-engine-port
  security:
    enabled: true
    username: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
    password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
```

