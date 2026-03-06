### Schedule Anchoring

Window-based triggers anchor their evaluation schedules to the trigger's `updatedAt` or `createdAt` timestamp. When a trigger restarts, the next evaluation is calculated relative to the anchor time, not the current time. This prevents schedule drift and ensures evaluations occur at consistent intervals.

#### Schedule Calculation

The engine calculates the next evaluation time using the following formula:

```
nextIntervalNumber = floor(timeSinceAnchor / duration) + 1
nextEvalAt = anchorTime + (nextIntervalNumber * duration)
initialDelay = nextEvalAt - now
```

Where:
- `timeSinceAnchor` is the elapsed time between the anchor timestamp and the current time
- `duration` is the trigger's configured window duration
- `anchorTime` is either `updatedAt` or `createdAt`
- `now` is the current system time

If the calculated `initialDelay` is negative, the trigger evaluates immediately.

#### Anchor Selection

The engine selects the anchor timestamp according to the following precedence:

| Condition | Behavior |
|:----------|:---------|
| `updatedAt` is present | Use `updatedAt` as schedule anchor |
| `updatedAt` is null, `createdAt` is present | Use `createdAt` as schedule anchor |
| Both timestamps are null | Fall back to scheduling from current time |
| Anchor timestamp is in the future | Fall back to scheduling from current time and log warning |

#### Timer Management

Each trigger with a window-based condition maintains an independent timer. When a trigger restarts, the engine disposes of the old timer and creates a new one. This prevents resource leaks and ensures only one active timer exists per trigger.

#### Validation

The trigger duration must be greater than 0. If validation fails, the engine throws an error:

#### Timestamp Updates

The `updatedAt` field is set whenever a trigger configuration changes. This timestamp becomes the new schedule anchor, resetting the evaluation cycle.
