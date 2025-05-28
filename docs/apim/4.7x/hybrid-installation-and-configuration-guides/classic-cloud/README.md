# Classic Cloud

## Deployment methods

Gravitee APIM can be installed using the following technology stacks and deployment methods.

{% hint style="warning" %}
Deployment methods that are not linked to documentation are still fully supported. For more information, contact us.
{% endhint %}

### Docker

* Docker Compose
* Docker CLI

### Kubernetes

* Vanilla Kubernetes
* AWS EKS
* Azure AKS
* GCP GKE
* OpenShift

### Linux

* RPM
* .ZIP

### Windows

* .ZIP

## Gateway and Bridge compatibility versions

The Bridge and APIM Gateway versions used for your hybrid deployment must be compatible per the tables below.

The following table lists the Gateway versions supported by each Bridge version.

| Bridge version | Supported Gateway versions |
| -------------- | -------------------------- |
| 4.3.x          | 4.3.x                      |
| 4.4.x          | 4.3.x to 4.4.x             |
| 4.5.x          | 4.3.x to 4.5.x             |
| 4.6.x          | 4.3.x to 4.6.x             |

The following table lists the Bridge versions supported by each Gateway version.

| Gateway version | Supported Bridge versions |
| --------------- | ------------------------- |
| 4.3.x           | 4.3.x to 4.6.x            |
| 4.4.x           | 4.4.x to 4.6.x            |
| 4.5.x           | 4.5.x to 4.6.x            |
| 4.6.x           | 4.6.x                     |

## Architecture

<img src="../../.gitbook/assets/file.excalidraw (18).svg" alt="Hybrid deployment architecture" class="gitbook-drawing">

<figure><img src="../../.gitbook/assets/image (172).png" alt="Diagram showing the hybrid architecture"><figcaption><p>Hybrid architecture connections</p></figcaption></figure>
