# ASD-STE100 Grammar & Writing Rules Reference

ASD-STE100 (Simplified Technical English) establishes 9 primary categories of writing rules. This reference details each rule category with specific guidelines and examples.

---

## 1. Controlled Vocabulary & Part of Speech (POS)

- **One Word, One Meaning, One Part of Speech**: Each approved word in STE has a single defined meaning and must be used as its assigned part of speech.
- **Do Not Convert Parts of Speech**: Do not turn nouns into verbs or adjectives into nouns (e.g., do not use "access" as a verb; use "read", "get", or "open").
- **Unapproved Synonyms**: Do not use different words to describe the same item or action. Stick consistently to the approved term across all documentation.

| Non-STE | Approved STE Equivalent | Reason / Rule |
| :--- | :--- | :--- |
| "Impact the performance" | "Affect the performance" | *Impact* is approved only as a noun, not a verb. |
| "Access the file" | "Open the file" / "Read the file" | *Access* is approved only as a noun. |
| "Utilize the tool" | "Use the tool" | *Utilize* is unapproved; use *use*. |

---

## 2. Extensible Technical Vocabulary (Technical Names & Technical Verbs)

Because general STE dictionaries cannot list all domain-specific nouns and processes, ASD-STE100 allows controlled extensions under strict criteria:

### Technical Names (TN)
Approved domain-specific nouns and noun phrases. Categories include:
- **Names of Parts / Hardware**: `O-ring`, `resistor`, `actuator`, `chassis`.
- **Names of Software / Data Elements**: `kernel`, `database`, `array`, `payload`, `repository`.
- **Names of UI Controls & Interfaces**: `button`, `checkbox`, `dialog box`, `command line`.
- **Names of Tools, Equipment & Materials**: `torque wrench`, `sealant`, `oscilloscope`.
- **Names of Systems & Processes**: `authentication`, `garbage collection`, `pull request`.

### Technical Verbs (TV)
Approved action verbs for explicit manufacturing, software, or technical processes not present in core STE.
- Must describe a specific, unambiguous physical or technical action.
- Examples: `compile`, `reboot`, `serialize`, `refactor`, `solder`, `calibrate`.
- *Rule*: Do not create a Technical Verb if an existing core STE verb (e.g., `make`, `change`, `turn`, `put`, `remove`) accurately describes the action.

---

## 3. Sentence Length Limits

Length limits ensure high readability and low cognitive load:

- **Procedural / Instructional Sentences**: Maximum **20 words**.
- **Descriptive / Informational Sentences**: Maximum **25 words**.

*Counting Rules*:
- Every word separated by whitespace counts as one word.
- Hyphenated words count as a single word if listed as such in the dictionary.

---

## 4. One Idea Per Sentence

- Each sentence must express only one complete thought, instruction, or condition.
- Avoid multi-clause compound sentences connected by multiple conjunctions (`and`, `which`, `because`, `although`).

**Non-STE**:
> "Before you turn on the pump, check that the inlet valve is open and verify the pressure gauge reads below 5 PSI, which ensures proper fluid circulation." *(26 words, 3 ideas)*

**STE Rewritten**:
> 1. Make sure the inlet valve is open.
> 2. Verify that the pressure gauge shows less than 5 PSI.
> 3. Turn on the pump.

---

## 5. Active Voice & Imperative Mood

- **Instructions**: Must use the **imperative mood** starting with an action verb.
- **Descriptive Text**: Must use the **active voice** (Subject + Verb + Object) wherever possible.
- **Passive Voice Exemption**: Passive voice is permitted *only* in descriptive text when the actor is unknown or irrelevant (e.g., "The log file is saved automatically every hour"). Passive voice is **never** permitted in procedural instructions.

**Non-STE Instruction**:
> "The power switch must be turned to the ON position by the operator."

**STE Instruction**:
> "Turn the power switch to ON."

---

## 6. Permitted Verb Tenses & Aspects

To eliminate temporal ambiguity:

- **Approved Tenses**:
  - **Simple Present**: `The server responds quickly.`
  - **Simple Past**: `The installation finished successfully.`
  - **Simple Future**: `The system will reboot.`
  - **Imperative**: `Click Next.`
- **Forbidden Forms**:
  - **Continuous / Progressive (`-ing`)**: Do not use `-ing` verbs as active verbs (e.g., avoid "The process is running").
  - **Perfect Tenses (`have/had + participle`)**: Avoid "The build has completed". Use "The build completed".
  - **Complex Modals**: Avoid `should`, `would`, `could`, `might`, `may`.
  - **Approved Modals**: Use `can` for ability and `must` for mandatory requirements.

---

## 7. Noun Clusters (Maximum 3 Nouns)

- A sequence of consecutive nouns modifying another noun (a noun cluster or stack) must not exceed **3 nouns**.
- Break up longer noun chains using prepositions (`of`, `for`, `in`, `on`).

**Non-STE (5 nouns)**:
> "Flight control system computer reset switch"

**STE Rewritten**:
> "Reset switch for the flight control system computer"

---

## 8. Procedural Structure & Warnings

- Order steps chronologically.
- Start each procedural step with an imperative verb.
- **Warnings and Cautions**: Always place warnings (risk of injury) and cautions (risk of equipment/data damage) **before** the action step to which they apply.

**Correct STE Layout**:
> **CAUTION**: Data loss can occur. Back up your database before you run the migration script.
>
> 1. Stop the database service.
> 2. Run the migration script.

---

## 9. Punctuation, Hyphenation & Formatting

- Keep punctuation simple: periods, commas, colons, and hyphens.
- Avoid semicolons (`;`) and em-dashes (`—`). Use separate sentences instead.
- Standardize hyphens for compound Technical Names defined in the dictionary (e.g., `O-ring`, `single-sign-on`).
- Use vertical lists (bulleted or numbered) for items, conditions, or steps with 3 or more entries.
