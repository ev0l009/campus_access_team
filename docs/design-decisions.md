# Architecture & Design Decision Log (DDL)

## DDL-001: Functional Module Architecture

### Context
The system needs to separate user interface displays, status changes, and file I/O to maintain a clean, modular, and maintainable codebase.

### Decision
We divided the code into four modules within a `services/` directory, coordinated by a central runner (`main.py`).

- **`ui.py`** — Handles console inputs, outputs, and selection string mappings.
- **`requests.py`** — Handles core entry dictionary generation and search lookups.
- **`workflow.py`** — Enforces strict sequential lifecycle validation.
- **`storage.py`** — Manages file structures and persists dictionary state.

### Consequences
This architecture supports fast, independent unit testing. Console inputs, file operations, and data lookups can be targeted and mocked independently, improving testability and maintainability.

---

## DDL-002: In-Memory Primitive Dictionary State Tracking

### Context
Session state must persist and update across multiple menu operations without the overhead of a database engine.

### Decision
We chose a native Python dictionary, `data`, initialized in `main.py`. This structure is passed directly to service operations, where it can be accessed, modified, and returned as needed.

### Consequences
- State updates are immediate and accessible across service operations.
- Native Python data structures keep state management simple.
- The dictionary maps directly to standard-library JSON operations, avoiding unnecessary data conversions.

---

## DDL-003: Direct String Conditionals for the Lifecycle State Machine

### Context
Cards must transition through a strictly defined lifecycle:

`requested → approved → issued → returned`

Each transition must be validated to prevent invalid operations.

### Decision
Instead of introducing a state-machine framework, we enforce lifecycle rules using direct string comparisons in `workflow.py`.

For example:

```python
if request["status"] != "approved":
    # Reject the operation if the request is not approved.