### Schedule Anchoring

Window-based alerts anchor their evaluation schedules to the trigger's `updatedAt` or `createdAt` timestamp. When a scheduled alert is updated, the next evaluation cycle starts from the update time, not the current time. If no timestamp is available or the anchor is in the future, the engine falls back to scheduling from the current time. Negative initial delays result in immediate scheduling.

The engine applies the following logic to determine the schedule anchor:

| Condition | Behavior |
|:----------|:---------|
| `updatedAt` is present | Use `updatedAt` as schedule anchor |
| `updatedAt` is null, `createdAt` is present | Use `createdAt` as schedule anchor |
| Both timestamps are null | Fall back to scheduling from current time with simple duration |
| Anchor timestamp is in the future | Fall back to scheduling from current time with duration (log warning) |
| Calculated initial delay is negative | Schedule immediately (delay = 0) |

The engine logs the following messages during schedule calculation:

* `"Using updatedAt timestamp {} as schedule anchor for trigger {}"`
* `"Using createdAt timestamp {} as schedule anchor for trigger {}"`
* `"No timestamp (updatedAt or createdAt) available for trigger {}. Falling back to scheduling from now."`
* `"Anchor timestamp {} is in the future for trigger {}. Falling back to scheduling from now with duration {} ms."`
* `"Calculated negative initial delay {} ms for trigger {}. Scheduling immediately"`

{% hint style="info" %}
Schedule anchoring requires Alert Engine version 3.0.0 or later.
{% endhint %}

### Helm Chart Parameters

The following table describes the Helm chart parameters for configuring Alert Engine default filters:

| Property | Description | Default |
|:---------|:------------|:--------|
| `alerts.api.ws.defaultFilters.enabled` | Enable or disable Alert Engine default filters through the APIM REST API | `true` |

{% hint style="info" %}
This parameter controls whether Alert Engine default filters can be managed via the APIM REST API.
{% endhint %}

### Default Filters

The WebSocket connector applies default filters to alert events. For example, the connector enforces installation ID constraints to ensure alerts are routed only within the same installation.

Administrators can disable these default filters via configuration. This allows:
- Cross-installation alert routing
- Custom filtering logic

{% hint style="warning" %}
Disabling default filters may require additional configuration to prevent unintended alert delivery across installations.
{% endhint %}

