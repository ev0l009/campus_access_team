# Campus Access

Campus Access is a Python CLI application for managing campus access-card requests. It tracks requests through a strict lifecycle using JSON data persistence.

## Features

- **Workflow Enforcement:** Restricts status transitions (`requested` → `approved` → `issued` → `returned`).
- **Flexible Profiles:** Supports Visitor, Student, and Staff card configurations.
- **ID Generation:** Automatically builds unique sequential IDs (e.g., `A001`).
- **Fault-Tolerant Persistence:** Gracefully handles missing or corrupted JSON database files.
- **Robust Verification:** Complete test coverage using the native `unittest` package.

## Project Structure

```text
.
├── main.py              # Application entry point and CLI loop
├── services/
│   ├── requests.py      # Request CRUD, input validation, and ID parsing
│   ├── workflow.py      # State transition logic (approval, issuance, returns)
│   ├── storage.py       # JSON loading, saving, and folder generation
│   └── ui.py            # User menu displays and option mapping
├── tests/               # Automated test suites matching service layers
└── data/                # Local database location (requests.json)
```

## Getting Started

### Prerequisites
- Python 3.12+ (Uses standard library utilities only)

### Execution
Run the terminal interface:
```bash
python3 main.py
```

### Testing
Execute the entire automated test suite:
```bash
python3 -m unittest discover -s tests -v
```

## Contributors

### Engineer A — Request Management & Data Safety
- Developed creation mechanics, input schemas, and automatic key parsing in `services/requests.py`.
- Wrote storage boundaries, validation handlers, and directories setups in `services/storage.py`.
- Built testing suites across `tests/test_requests.py` and `tests/test_storage.py`.

### Engineer B — Workflow & CLI Interface
- Programmed business state rules and transition guards in `services/workflow.py`.
- Configured user terminal selection mappings and CLI layouts in `services/ui.py` and `main.py`.
- Built lifecycle state checking assertions in `tests/test_workflow.py`.