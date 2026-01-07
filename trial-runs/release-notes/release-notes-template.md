# Release Notes Template

## Release Date: Month Day, Year

## Highlights

* Highlight 1
* Highlight 2

## Breaking Changes

#### **Breaking Change 1**

* Prior to APIM version 4.9.0, users had to override the `runAsGroup` securityContext to set the GID to 1000. With APIM 4.9.0, users must set the `runAsGroup` securityContext to `null` to let OpenShift select the root group.

#### Breaking Change 2

* If the `integration-controller` ingress uses the same host as the `management` ingress, it no longer inherits the annotation of the `management` ingress. With APIM 4.9.0, you must configure the `integration-controller` ingress with the following values:\
  \
  <br>

```yaml
api:
  federation:
    ingress:
      enabled: true
      path: /integration-controller(/.*)?
      pathType: Prefix
      hosts:
        - apim.example.com
      annotations:
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-read-timeout: 3600   
```

```yaml
api:
  federation:
    ingress:
      enabled: true
      path: /integration-controller(/.*)?
      pathType: Prefix
      hosts:
        - apim.example.com
      annotations:
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-read-timeout: 3600   
```

* **Elasticsearch template updates required**\
  When you upgrade to 4.9.0, you must update Elasticsearch templates to support execution transparency analytics with error and warning component tracking. If you manage your own Elasticsearch installation, update index templates before you upgrade. Elasticsearch auto-generates templates if you do not manually update them, but this results in suboptimal field mappings. Gravitee-managed Elasticsearch or SaaS deployments update automatically.

## New Features

#### cr\_title 1

* json object 1 for cr\_title 1
* json object 2 for cr\_title 1
* ...
* json object n for cr\_title 1

#### cr\_title 2

* json object 1 for cr\_title 2
* json object 2 for cr\_title 2
* ...
* json object n for cr\_title 2

#### cr\_title n

* json object 1 for cr\_title n
* json object 2 for cr\_title n
* ...
* json object n for cr\_title n

## Updated Features

#### cr\_title 1st update

* json object 1 for cr\_title 1
* json object 2 for cr\_title 1
* ...
* json object n for cr\_title 1

#### cr\_title 2nd update

* json object 1 for cr\_title 2
* json object 2 for cr\_title 2
* ...
* json object n for cr\_title 2

#### cr\_title 3rd update

* json object 1 for cr\_title n
* json object 2 for cr\_title n
* ...
* json object n for cr\_title n
