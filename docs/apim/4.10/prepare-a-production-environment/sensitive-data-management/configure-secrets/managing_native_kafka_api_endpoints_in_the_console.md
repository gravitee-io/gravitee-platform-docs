### Endpoint Table Display

The endpoint table adapts its columns based on API type:

| Column | Native Kafka Content | HTTP Proxy Content | Width |
|:-------|:---------------------|:-------------------|:------|
| Drag icon | Drag handle (hidden if read-only) | Drag handle | 48px |
| Name | Endpoint name + "Default" badge (first endpoint only) | Endpoint name | flexible |
| General | Bootstrap Servers | Target URL | flexible |
| Options | Security protocol badges (if configured) | Health check badges (if enabled) | flexible |
| Weight | (hidden for Native APIs) | Endpoint weight | 80px |
| Actions | Edit/Delete buttons | Edit/Delete buttons | 96px |

#### Options Column Badges

For Native Kafka APIs, the Options column displays security protocol badges when configured:

* Badge text displays the security protocol (e.g., `SASL_SSL`)
* Tooltip indicates whether the protocol is "inherited from group configuration" or "override by endpoint configuration"

For HTTP Proxy APIs, the Options column displays health check badges when enabled:

* Badge text displays `Health Check`
* Tooltip indicates whether health check is "enabled by endpoint configuration" or "enabled via inherited group configuration"

#### Default Endpoint Badge

The first endpoint in the first group of a Native Kafka API displays a "Default" badge. The tooltip for this badge reads "The default endpoint used by the API is the first one."

### Restrictions

* The load balancer type is optional for Native Kafka endpoint groups. The required validation constraint is removed for this API type.
* The Weight column is hidden for all Native API types.
* Drag-and-drop reordering is disabled when the API is in read-only mode or when a reorder operation is in progress.
* The load balancer badge is not displayed for `native-kafka` endpoint groups.
* Action buttons in the Actions column have been changed from icon-only to text buttons for improved accessibility.

