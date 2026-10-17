```markdown
# AI Learning Log

## Topic 1: Architecture Patterns — Functions / State Machine vs. Conditionals

### What I Explored
The design choice of building a lightweight state machine using a standard `while` loop combined with explicit `if/elif/else` branching in `main.py`, rather than introducing an abstract, class-based, or external state machine framework.

### Key AI Insights

- **Simple Conditionals Are Often Enough:** Using explicit conditionals with string literals such as `"dashboard"` and `"create_request"` provides a readable and practical way to manage navigation in a straightforward terminal application.

- **Primitive State and Functional Boundaries:** Passing an in-memory dictionary (`data`) through clearly defined function boundaries keeps the architecture lightweight and makes individual operations easier to test.

- **Separation of Responsibilities:** Isolating functions makes it easier to identify where specific responsibilities belong:
  - `workflow.py` — Handles lifecycle rules and status transitions.
  - `requests.py` — Handles request data structure generation and lookup operations.
  - `main.py` — Coordinates application execution and menu navigation.

### Key Takeaway
**Choose the simplest architecture that adequately solves the problem.** A dedicated state machine framework becomes more valuable when transitions, states, and associated behaviors grow complex enough to justify the additional abstraction.

---

## Topic 2: Mastering Automated Testing & Mocking Structures

### What I Explored
Using Python's native `unittest` and `unittest.mock` frameworks to isolate application logic, simulate console interactions, and troubleshoot test execution errors.

### Key AI Insights

#### 1. Python Paths and Test Execution

Running test scripts from nested directories can cause Python to fail to resolve project modules because the project root may not be available on the module search path.

A standard approach is to execute test discovery from the project root:

```bash
python -m unittest discover -s tests
```

This provides a consistent testing workflow and helps Python resolve project modules from the root directory.

#### 2. Mock Argument Stacking Order

When stacking multiple `@patch` decorators on a test function, `unittest.mock` passes the generated mock objects into the test function in **bottom-to-top decorator order**.

For example:

```python
from unittest.mock import patch

@patch("sys.stdout")
@patch("builtins.open")
@patch("pathlib.Path.mkdir")
def test_storage(mock_mkdir, mock_open, mock_stdout):
    ...
```

The mock corresponding to the bottom decorator, `pathlib.Path.mkdir`, becomes the first injected argument.

Failing to account for every applied decorator or declaring the arguments in the wrong order can cause confusing test failures, including `TypeError` argument-count mismatches.

#### 3. Intercepting Terminal I/O

Using `patch("sys.stdout", new_callable=StringIO)` allows tests to capture output produced by `print()` without displaying it in the active terminal.

Example:

```python
from io import StringIO
from unittest.mock import patch

def test_error_message(self):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        print("Invalid request.")

    self.assertEqual(
        mock_stdout.getvalue(),
        "Invalid request.\n"
    )
```

This makes it possible to verify terminal messages and test how the application responds to simulated failures.

### Key Takeaway
**Effective testing requires understanding both the code being tested and the environment in which the tests execute.** Knowing how imports, mocks, and standard output behave makes it easier to isolate problems and build reliable automated tests.

---

## Overall Reflection

This learning phase strengthened my understanding of two important areas of software engineering:

1. **Architectural judgment:** Knowing when straightforward functions and conditionals are preferable to more complex abstractions.
2. **Testing discipline:** Using test discovery, mocks, and output capture to verify application behavior without depending on real files or interactive terminal input.

The broader lesson is that maintainable software does not necessarily require complicated architecture. It requires clear responsibilities, predictable behavior, and tests that verify the system's important rules.