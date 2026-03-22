# Implementing Context-Aware Logging in Gateway Plugins and Handlers

## Creating Context-Aware Loggers

Developers implementing Gateway policies or handlers create context-aware loggers by calling `ctx.withLogger(log)` where `ctx` is the `ExecutionContext` and `log` is a logger obtained from `NodeLoggerFactory`. The returned logger automatically populates MDC with request-scoped metadata (API ID, plan ID, user, application) before each log statement.

<!-- GAP: Example code block needed showing ctx.withLogger(log) usage -->

This produces a log entry with MDC keys `nodeId`, `apiId`, `planId`, etc., as configured in `node.logging.mdc.include`.

The `ExecutionContextLazyLogger.lazy(log, ctx, factory)` pattern defers logger initialization until a log level is enabled, avoiding overhead when logging is disabled. Use this in hot paths where context-aware logger creation is expensive.

Example:
