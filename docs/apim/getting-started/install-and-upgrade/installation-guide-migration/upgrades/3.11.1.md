# Repository

## Mongodb

Before running any script, please create a dump of your existing
database.

[/apim/3.x/mongodb/3.11.1/1-event-debug-migration.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.11.1/1-event-debug-migration.js)  
This script removes the `API_ID` property for events of type `DEBUG`.
