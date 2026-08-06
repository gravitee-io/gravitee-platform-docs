---
description: >-
  This page shows the supported geographies and providers available for Gravitee
  Cloud.
---

# Geography and Provider Support

Gravitee Cloud allows you to choose where your API Management control plane is hosted, as well as where your Gravitee-hosted API Gateways run.

This is important to ensure compliance with data privacy requirements, and also to minimize latency, as it guarantees your Gravitee-hosted API Gateway runs close to your end users and upstream services.

Gravitee Cloud currently offers the following geography and provider support. If you’re interested in another geography or provider, Gravitee can introduce that for you.

### API Management Control Plane

<table>
    <thead>
        <tr>
            <th width="140">Provider</th>
            <th width="280">Geography</th>
            <th>Region</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Azure</td>
            <td>US (United States)</td>
            <td>Washington (<code>westus2</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>EU (Europe)</td>
            <td>Netherlands (<code>westeurope</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>AU (Australia)</td>
            <td>Australia (<code>australiaeast</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>CH (Switzerland)</td>
            <td>Switzerland (<code>switzerlandnorth</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>UAE (United Arab Emirates)</td>
            <td>United Arab Emirates (<code>uaenorth</code>)</td>
        </tr>
    </tbody>
</table>

Each Control Plane geography has its own Cloud Gate, which is the endpoint a hybrid Gateway connects to. For the Cloud Gate URLs, see [Next-Gen Cloud](https://documentation.gravitee.io/apim/hybrid-installation-and-configuration-guides/next-gen-cloud#architecture).

### Gravitee hosted API Gateways

<table>
    <thead>
        <tr>
            <th width="140">Provider</th>
            <th width="280">Geography</th>
            <th>Region</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Azure</td>
            <td>US (United States)</td>
            <td>Washington (<code>westus2</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>US (United States)</td>
            <td>Virginia (<code>eastus2</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>EU (Europe)</td>
            <td>Netherlands (<code>westeurope</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>AU (Australia)</td>
            <td>Australia (<code>australiaeast</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>CH (Switzerland)</td>
            <td>Switzerland (<code>switzerlandnorth</code>)</td>
        </tr>
        <tr>
            <td>Azure</td>
            <td>UAE (United Arab Emirates)</td>
            <td>United Arab Emirates (<code>uaenorth</code>)</td>
        </tr>
        <tr>
            <td>AWS</td>
            <td>US (United States)</td>
            <td>N. Virginia (<code>us-east-1</code>)</td>
        </tr>
        <tr>
            <td>AWS</td>
            <td>APAC (Asia-Pacific)</td>
            <td>Sydney (<code>ap-southeast-2</code>)</td>
        </tr>
        <tr>
            <td>AWS</td>
            <td>EU (Europe)</td>
            <td>Dublin (<code>eu-west-1</code>)</td>
        </tr>
        <tr>
            <td>GCP</td>
            <td>US (United States)</td>
            <td>Iowa (<code>us-central1</code>)</td>
        </tr>
        <tr>
            <td>GCP</td>
            <td>EU (Europe)</td>
            <td>Frankfurt (<code>europe-west3</code>)</td>
        </tr>
        <tr>
            <td>GCP</td>
            <td>APAC (Asia-Pacific)</td>
            <td>Singapore (<code>asia-southeast1</code>)</td>
        </tr>
    </tbody>
</table>

For more information about Azure regions, go to [Microsoft Datacenters](https://datacenters.microsoft.com/globe/explore/).

For more information about AWS regions, go to [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/).\
\
For more information about GCP regions, go to [Google Cloud Locations](https://cloud.google.com/about/locations).
