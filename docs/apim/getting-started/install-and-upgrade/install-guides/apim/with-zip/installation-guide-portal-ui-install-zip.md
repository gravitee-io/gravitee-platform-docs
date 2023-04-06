# installation-guide-portal-ui-install-zip

## Prerequisites

Your environment must meet the requirements listed below before you install APIM Portal.

Before you begin, ensure APIM API is installed and running.

### Browsers

APIM Portal is supported with the two most recent versions of all modern internet browsers.

## Download and extract the `.zip` archive

The binaries are available from [Downloads page](https://gravitee.io/downloads/api-management) or via [https://download.gravitee.io/graviteeio-apim/distributions/graviteeio-full](https://download.gravitee.io/graviteeio-apim/distributions/graviteeio-full)-\{{ site.products.apim.\_3x.version \}}.zip\[Download].

```
$ curl -L https://download.gravitee.io/graviteeio-apim/distributions/graviteeio-full-{{ site.products.apim._3x.version }}.zip -o gravitee-standalone-distribution-{{ site.products.apim._3x.version }}.zip
```

Once file has been downloaded, you just have to unpack it in the right place

```
$ unzip gravitee-standalone-distribution-{{ site.products.apim._3x.version }}.zip
```

### Deploy

The portal is a client-side only Angular application and can be deployed on any HTTP server like [Apache](https://httpd.apache.org/) or [Nginx](http://nginx.org/).

### Run with Node.js

```
$ npm install angular-http-server -g
$ cd graviteeio-apim-portal-ui-{{ site.products.apim._3x.version }}
$ angular-http-server
$ Listening on 8080
```
