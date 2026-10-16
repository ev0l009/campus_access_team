# 🏫 CAMPUS ACCESS — THE ENGINEERING CHALLENGE

**Guided Python Recovery Project | Fellow Edition**

You are two junior engineers asked to build a reliable campus access-card request manager. Your goal is to understand, build, test, explain, review and improve software—not to paste an AI-generated solution. This is a learning opportunity; mistakes you can investigate and correct are part of the work.

---

# 🎯 1. Your mission

A campus issues visitor, student and staff access cards. A request must be created, approved by an authorized staff identifier, issued and eventually returned. The software must stop invalid actions and preserve correct data even after restart.

Build a Python command-line application, not a web application. Use only Python standard library and GitHub.

## 📦 What you must deliver

A working CLI with:

- Create request
- View request
- Approve request
- Issue card
- Return card
- List requests
- Save to JSON
- Reload from JSON
- Quit safely

Each request stores:

`id`, `fellow_id`, `card_type`, `status`, `approved_by`.

Allowed `card_type`: `visitor`, `student`, `staff`.

New status: `requested`.

## 🔄 The workflow contract

`requested → approved → issued → returned`

- Only a request with nonempty `approved_by` may move from approved to issued.
- No skipping states.
- Returned is final.
- Unknown IDs, blank fellow IDs, invalid card types, malformed IDs, empty approver and unsupported transitions must be rejected.
- When an operation fails, the record must stay exactly unchanged.

IDs are `A001`, `A002`, `A003`... and must stay unique across restarts.

On loading JSON, validate the data and reject malformed files clearly; never silently replace an invalid file with empty data.

For ID checks, accept ASCII digits `0–9`, not arbitrary Unicode numerals.

---

# 📚 2. Learn before you build

## 📖 Concept A — dictionaries, functions and validation

Study Python dictionaries and how to access/update values. Study function parameters, return values and `ValueError`.

Try an unrelated mini exercise: validate a book record with title and page count.

**Reflection:** Why should input be validated BEFORE writing to your dictionary?

## 🔀 Concept B — state machines and invariants

A state machine defines which actions can follow which states.

On paper, draw four boxes: requested, approved, issued, returned. Draw only legal arrows. Try to find three illegal shortcuts.

**Reflection:** If an invalid transition raises an error, how can you prove that the stored record was not modified?

## 💾 Concept C — JSON and persistence

Study `json.dump`, `json.load`, `FileNotFoundError` and `JSONDecodeError`.

Make a tiny unrelated example that saves two books to a temporary JSON file, reloads them and checks their content.

**Reflection:** What happens if a file is corrupt, contains duplicate IDs, or has missing keys?

## 🧪 Concept D — unittest and GitHub collaboration

Study `unittest.TestCase`, `assertEqual`, `assertRaises`, `setUp` and temporary files.

Learn:

- `git status`
- `switch -c`
- `add`
- `commit`
- `push`
- Pull request
- Review
- Merge

**Reflection:** Why is a passing test on your feature branch not enough after both branches merge?

## 🤖 How to use AI professionally

Use AI to explain a concept, ask you a question, critique your design, suggest edge cases, or interpret a test failure.

Before applying advice, predict what should happen, test it yourself and record whether the advice worked.

**Do not ask AI to write the whole Campus Access project.**

Each engineer records at least **TWO learning cycles**:

1. Question
2. AI explanation
3. Your own experiment
4. Verification
5. Final decision

---

# 🧩 3. Design together before writing code

Discuss and write answers in `docs/design-decisions.md`:

1. What does one request dictionary look like?
2. What should `create_request` return?
3. How will functions report invalid inputs?
4. Where is the next ID generated?
5. How will Engineer B call Engineer A's storage functions?
6. What happens if a saved JSON file is invalid?
7. Which data must never change on a rejected operation?

---

# 👨‍💻 4. Engineer A — Registration and data safety

You own request creation, validation, unique ID generation, read-only lookup, save and load.

**Suggested interfaces:**

- `create_request(fellow_id, card_type)`
- `get_request(request_id)`
- `save_requests(path)`
- `load_requests(path)`

Agree on signatures and storage ownership with B; names are suggestions, not provided solutions.

## ✅ Build checkpoints for A

- **A1.** Create A001 with a nonempty fellow ID and valid card type; inspect all five fields.
- **A2.** Reject blank fellow ID, invalid card type, wrong input type and malformed ID.
- **A3.** Save requests, restart and reload; new request must become A002, not A001.
- **A4.** Reject corrupted JSON, missing keys, duplicate IDs and invalid states without silently wiping existing records.

## ❓ Questions Engineer A must answer

- Why is a dictionary appropriate here?
- What happens if the file is empty?
- How do you avoid duplicate IDs after restart?
- Why can data loaded from a local JSON file still be unsafe?
- What is the difference between validation and sanitization?
- How would you test that a failed save does not overwrite a valid file?

---

# 👨‍💻 5. Engineer B — Approval and safe workflow

You own approve, issue, return and CLI interaction.

**Suggested interfaces:**

- `approve_request(request_id, approved_by)`
- `issue_card(request_id)`
- `return_card(request_id)`
- `run_menu()`

Coordinate with A so B does not bypass validation or modify records directly without agreed contracts.

## ✅ Build checkpoints for B

- **B1.** Show a newly created request with status `requested`.
- **B2.** Reject `requested → issued` and prove status stays `requested`.
- **B3.** Reject approval with blank approver and preserve previous data.
- **B4.** Approve with M01, then issue and return.
- **B5.** Reject a second return and an attempt to issue a returned card.
- **B6.** Invalid menu options must display helpful feedback and let the user retry.

## ❓ Questions Engineer B must answer

- What is an illegal transition?
- Why validate before mutation?
- How do you keep the CLI from crashing on a typo?
- What should happen if an unknown ID is used?
- How do you test that an error leaves the original record unchanged?
- Why is a status check more reliable than merely hiding a menu option?

---

# 🧩 6. Your challenge board — demonstrate, don't guess

### 🧪 CASE 1: Create visitor request for F001

**Expected:** A001, `requested`, `approved_by` null.

### 🧪 CASE 2: Issue A001 before approval

**Expected:** Rejected; no field changes.

### 🧪 CASE 3: Approve A001 with blank approver

**Expected:** Rejected; still `requested`.

### 🧪 CASE 4: Approve A001 with M01; issue; return

**Expected:** `requested → approved → issued → returned`.

### 🧪 CASE 5: Return A001 again, or issue it again

**Expected:** Rejected; remains `returned`.

### 🧪 CASE 6: Save, exit, reopen and create another request

**Expected:** A002, no duplicate.

### 🧪 CASE 7: Load malformed JSON

**Expected:** Clear failure; never silently destroy prior valid data.

### 🧪 CASE 8: Enter a wrong menu option or unexpected text

**Expected:** Helpful message and another chance to enter valid input.

## 🐛 The bug-hunter challenge

Swap roles.

- Engineer A invents two edge cases for B's workflow.
- Engineer B invents two for A's validation/persistence.

Predict the result first. Run the tests and record expected vs actual output.

**Ask:** Can I make this system enter a state the business rules forbid?

---

# 🧪 7. Tests are part of the product

Create at least eight meaningful `unittest` tests, with at least two written by each engineer.

**Recommended tests:**

- Valid creation
- Invalid card type
- Blank fellow ID
- Unique IDs after reload
- Corrupted JSON
- Illegal issue before approval
- Blank approver
- Correct full workflow
- Double return
- CLI retry

Use isolated temporary test files.

**Run:**

```bash
python -m unittest discover -s tests -v
```

⚠️ Do not claim tests passed unless you actually ran them.

---

# 🐙 8. GitHub — work as two professional engineers

Create a repository with:

- `README.md`
- `.gitignore`
- `main.py`
- Project modules
- `tests/`
- `docs/ai-learning-log.md`
- `docs/design-decisions.md`

Create GitHub issues with clear acceptance criteria.

**Engineer A** works on:

`feat/1-request-validation`

**Engineer B** works on:

`feat/2-access-workflow`

Use commits such as:

- `feat: validate card requests`
- `test: reject invalid transitions`
- `docs: explain project setup`

## 🔀 Pull requests and code reviews

Each engineer must open a PR containing substantive code and tests.

The **OTHER engineer** must review it, run relevant tests, leave at least two meaningful observations and request changes when necessary.

The author addresses feedback; the partner approves before merge.

No direct feature pushes to `main`.

If branch protection is unavailable, show the mentor the actual review timeline.

## 🔍 Questions to ask in a pull request review

- Which requirement does this function satisfy?
- Can a failed action partially modify a record?
- Where is the test for this condition?
- Does the new module work with the other engineer's module?
- Could loading a corrupted file destroy valid data?
- Is the README still accurate?

---

# 🏆 9. Evidence and final demonstration

Both engineers must show:

- Their authored code
- Two or more tests they wrote
- Their PR
- The review they gave their partner
- An AI-assisted learning cycle
- One problem they solved

Then demonstrate all eight challenge-board cases together.

Finally, rerun tests from integrated `main` and record:

```bash
git rev-parse HEAD
```

## 📝 Individual reflection

### 👨‍💻 Engineer A

- Which validation bug surprised you?
- What did your partner notice during review?
- What can you now explain without AI?

### 👨‍💻 Engineer B

- Which transition was easiest to get wrong?
- What test helped you fix it?
- How did your partner's feedback improve the workflow?

### 🤝 Both

- What did AI teach you that you did not know before?
- What AI advice did you verify, adjust or reject?
- What would you improve if you had another day?

---

# 📊 10. How your work will be assessed

| Assessment area | Marks |
|---|---:|
| Correct functionality | 35 |
| Meaningful automated tests | 20 |
| Git branches, commits, PRs and reciprocal reviews | 20 |
| Independent AI-assisted learning and verification | 15 |
| Documentation, teamwork and individual explanation | 10 |
| **Total** | **100** |

A working demo alone does not earn full credit.

## 📋 Submission checklist

Submit:

- The repository link
- Engineer A and B names
- Final `main` commit SHA
- Both PR URLs
- Passing `unittest` evidence
- AI learning log
- README

Be prepared to explain a function and change a small requirement live.

---

# 🎯 Final message

Build something you can explain.

A good engineer is not someone who never encounters errors; a good engineer can identify a problem, ask better questions, test a hypothesis, work with another engineer, and prove the final result is reliable.