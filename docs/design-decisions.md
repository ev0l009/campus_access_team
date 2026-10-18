## Design Decisions

- **State Machine:** Structured menu flow around clear state transitions.
- **Data Structures:** Used dictionaries to represent requests, with lists to manage collections of requests.
- **Error Handling:** Core functions handle their own validation and errors, keeping `main.py` slim and focused on menu flow.
- **Modular Design:** Separated request management, workflow, storage, and CLI responsibilities.
- **Persistence:** Used JSON for simple, file-based data storage.
- **Testing:** Used `unittest` to verify functionality, workflow rules, and edge cases.