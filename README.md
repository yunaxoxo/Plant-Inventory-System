# Plant & Fertilizer Management CLI

## Description

This is a Command-Line Interface (CLI) program for managing plants, fertilizers, and logbook entries. Users can **add, view, edit, and delete plants**, **track fertilizers and nourishment**, and **log plant activities**. The system ensures that all actions are validated and provides feedback for invalid inputs.

---

## Features

- Add, view, edit, and delete plants (Indoor/Outdoor)
- Track fertilizers and suppliers
- Apply fertilizers or nutrients to plants
- Maintain a logbook for plant activities
- Input validation for menu options, yes/no prompts, and plant names

---

## Menu Options

1. **Exit** – Quit the program
2. **Previous** – Return to the previous menu
3. **Add Plant** – Add a new plant with name and storage type
4. **Delete Plant** – Remove a plant from the system
5. **View Plant** – View plant details by entering its name
6. **Edit Plant** – Modify existing plant information
7. **Update Nourishment** – Add or update fertilizers and nutrients
8. **Nourish Plant** – Apply fertilizers or nutrients to a plant
9. **Logbook** – Add or view log entries for plant activities

---

## Input Guidelines

### Plant Names

- Input is **case-insensitive**. `"Tomato"` and `"tomato"` are treated the same.
- Must match an existing plant for view, edit, delete, or nourish actions.

### Yes/No Prompts

- Acceptable inputs: `y`, `n`, `yes`, `no` (case-insensitive)
- Invalid entries will prompt again until correct input is given.

### Menu Options

- Use the **numeric index** of the option (e.g., `2` for Add Plant)
- Non-numeric or out-of-range entries will display an error message.

---

## Sample Usage

```
What would you like to see? (Plant/Fertilizer/Logbook/All/Exit)
You can choose one or more options separated by comma (,): 2
Enter Plant Name: Tomato
Enter Storage Type (Indoor/Outdoor): Outdoor
Plant added with ID: P1
Would you like to continue? (y/n): y
```

```
Which one would you like to proceed with? 4
Enter Plant Name: Tomato
Plant ID: P1
Storage: Outdoor
Logs: None
```

---

## Setup & Run

1. Clone the repository:

```bash
git clone <repo-url>
cd <project-folder>
```

2. Run the program:

```bash
python main.py
```

> Make sure you have Python 3 installed.

---

## Notes

- Always enter the **exact plant name** when performing actions on existing plants, but capitalization does not matter.
- Numeric menu selection is required; typing plant names in place of numbers will cause errors.
- Logbook entries should use the `day/month/year` forma
