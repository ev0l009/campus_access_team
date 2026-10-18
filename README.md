# Campus Access

Campus Access is a Python CLI application for managing campus access-card requests. It supports request creation, approval, card issuance, returns, and JSON-based data persistence.

## Features

- Create, view, and list access-card requests.
- Support visitor, student, and staff cards.
- Enforce the request workflow: `requested → approved → issued → returned`.
- Validate inputs and prevent invalid status transitions.
- Generate sequential request IDs.
- Save and load requests using JSON.
- Validate saved data and handle malformed files safely.
- Automated tests using Python's `unittest`.

## Requirements

- Python 3.12+
- Python standard library only.

## Getting Started

Clone the repository and navigate to the project directory.

Run the application:

```bash
python3 main.py
```

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Project Structure

- `main.py` — CLI and menu interface.
- `campus_access/requests.py` — Request creation, lookup, and validation.
- `campus_access/workflow.py` — Approval, issuance, and return operations.
- `campus_access/storage.py` — JSON persistence and data validation.
- `tests/` — Automated tests.
- `data/` — Saved request data.

## Contributors

### Engineer A — Request Management and Data Safety
- Implemented request creation, validation, unique ID generation, and lookup.
- Implemented JSON persistence and saved-data validation.
- Wrote tests for request management and storage.

### Engineer B — Workflow and CLI
- Implemented request approval, card issuance, and card returns.
- Built the command-line interface and user interaction.
- Wrote tests for workflow transitions and invalid operations.