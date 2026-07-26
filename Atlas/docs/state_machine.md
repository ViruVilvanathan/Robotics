# Atlas State Machine

## Purpose

The state machine controls the operational mode of Atlas and ensures
only valid transitions occur.

## States

- OFF
- IDLE
- MANUAL
- AUTONOMOUS
- FAULT
- EMERGENCY_STOP

```mermaid
stateDiagram
    OFF --> IDLE
    IDLE --> MANUAL
    IDLE --> AUTONOMOUS
    MANUAL --> IDLE
    AUTONOMOUS --> IDLE
    MANUAL --> EMERGENCY_STOP
    AUTONOMOUS --> EMERGENCY_STOP
    EMERGENCY_STOP --> IDLE
```