# Console UI and Database Schema Changes for Kafka Virtual Clusters

## Related Changes

The Console UI introduces three navigation labels under the **Kafka** category:

* **Standalone** (route: `./clusters/kafka-standalone`)
* **Clusters** (route: `./clusters/kafka-clusters`)
* **Virtual Clusters** (route: `./clusters/kafka-virtual-clusters`)

Tab visibility depends on cluster type:

* **KAFKA_CLUSTER_STANDALONE**: **General**, **Explorer**, **Configuration**, and **User Permissions** tabs are shown.
* **KAFKA_CLUSTER** and **KAFKA_VIRTUAL_CLUSTER**: **General**, **Configuration**, and **User Permissions** tabs are shown. The **Explorer** tab is not available.

Status badges display lifecycle states:

* **DEPLOYED** (success color)
* **PENDING** (warning color)
* **UNDEPLOYED** (neutral color)

The API creation wizard for `NATIVE` APIs includes an "Endpoint Type" step (Step 3.1) where users select between three endpoint connector types:

* `native-kafka` (standalone broker configuration)
* `native-kafka-cluster` (reference to a Kafka Cluster entity)
* `native-kafka-virtual-cluster` (reference to a Kafka Virtual Cluster entity)

Database migration adds the following columns to the `clusters` table:

* `type` (default value: `KAFKA_CLUSTER_STANDALONE`)
* `lifecycleState`
* `deployedAt`
* `version`

Migration scripts:

* `src/main/resources/liquibase/changelogs/v4_12_0/schema.yml`
* `src/main/resources/liquibase/changelogs/v4_12_0/data.yml`

Conditional display logic for SASL mechanism fields in the cluster configuration form was updated to use relative path references (`../protocol`) instead of absolute path references (`value.security.protocol`).

A new Management API endpoint was added:

* **GET** `/environments/{envId}/clusters/deployed` — retrieves deployed clusters with their connections.

UI component dependencies were updated to version 17.8.0:

* `@gravitee/ui-analytics`
* `@gravitee/ui-particles-angular`
* `@gravitee/ui-policy-studio-angular`
* `@gravitee/ui-schematics`
