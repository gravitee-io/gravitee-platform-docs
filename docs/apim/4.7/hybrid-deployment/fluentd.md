# Fluentd

## Kubernetes

1. Install Fluentd. To install Fluentd,  go to either of the following sites:

* [Official Helm charts](https://artifacthub.io/packages/helm/fluent/fluentd)

## Docker

1. Install Fluentd. To install Fluentd, build a Docker image by copying the following files:

{% code title="Dockerfile" lineNumbers="true" %}
```
FROM fluent/fluentd:v1.16.2-1.0
USER root
RUN ["gem", "install", "fluent-plugin-s3"]
USER fluent
```
{% endcode %}

{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

services:
  fluentd:
    image: fluentd:s3
    container_name: gio_apim_fluentd
    hostname: fluentd
    restart: always
    ports:
      - "9000:9000"
    volumes:
      - ./fluentd_conf:/fluentd/etc
```
{% endcode %}

## .ZIP

1. Install Fluentd. To install Fluentd, go to [Download Fluentd](https://www.fluentd.org/download).

## Configure Fluentd

{% code title="fluentd.conf" lineNumbers="true" %}
```editorconfig
<source>
  @type tcp
  tag tcp
  <parse>
    @type json
  </parse>
  port 9000
</source>

<match *.**>
  @type s3
  aws_key_id "xxxxxxxxxxxxxxx"
  aws_sec_key "xxxxxxxxxxxxxxx"
  s3_bucket "my-s3-bucket"
  s3_region "my-s3-region"
  
  path /
  time_slice_format %Y%m%d%H
  time_slice_wait 10m
  time_format %Y%m%d%H%M

  buffer_type file
  buffer_path /fluentd/log
  buffer_chunk_limit 256m
  buffer_queue_limit 512
  flush_interval 10s
  flush_at_shutdown true
  
  <format>
    @type json
  </format>
</match>
```
{% endcode %}
