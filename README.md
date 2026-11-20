# PocketMoney 💰

**Earnings, Expenses, Loans & "What if" Planner**

A Python desktop app that shows students and young earners how their EMIs affect their monthly money: what is left after all loan payments, how healthy their finances are, and how to deal with their most critical loan.

> Python Collaborative Project · Computational Thinking and Programming (2026CSAE100) · Bennett University · Batch 62

![PocketMoney screenshot](screenshots/app.png)

---

## Features

- **Loan tracking:** add any number of loans (amount, EMI, months), stored in a dictionary
- **Financial summary:** money left after spending and all EMIs
- **Health rating:** HEALTHY, MODERATE or CRITICAL based on your saving target
- **Critical-loan detection:** finds the loan with the highest EMI automatically
- **3 "What if" scenarios** for the critical loan:
  - **Save to clear:** how many months of saving it takes to pay it off
  - **Buy something:** whether you can afford an item now, or in how many months
  - **Pay extra:** how much extra per month clears the loan by your target date
- **Input validation:** blanks, letters, negatives, `nan`, `inf` and an EMI bigger than the loan are all rejected with an error message, never a crash
- **CSV storage:** loans can be saved to and loaded from `loans.csv`

---

## How to run

**Requirements:** Python 3.10 or newer and VS Code with the Python extension (by Microsoft). Tkinter is included with Python, so there is nothing else to install.

1. Download this repo (**Code → Download ZIP**) and unzip it.
2. In VS Code, go to **File → Open Folder** and open the whole `PocketMoney` folder. Don't open just one file: the GUI imports the other `.py` files, so they must be open together.
3. Open `PoketMoney_GUI.py` and click the **▷ Run** button in the top right.

---

## Example

| Input | Value |
|---|---|
| Salary | 40000 |
| Spending | 18000 |
| Saving % | 20 |
| Loan 1 | 60000, EMI 3000, 20 months |
| Loan 2 | 30000, EMI 2600, 12 months |

**Result:** Remaining after EMI **₹16,400**, status **HEALTHY**, critical loan **loan1**

- Save to clear: **8 months**
- Buy something (₹30,000): **about 2 months**
- Pay extra (clear in 10 months): **₹3,000 extra per month**

---

## Project structure

```
PocketMoney/
├── PoketMoney_GUI.py      # Tkinter window + glue functions (main file)
├── Inputs_Saksham.py      # Input validation, add_loan, CSV save/load
├── Analysis_Vansh.py      # Total EMI, financial health, critical loan, loan list
├── Whatif_Vasu.py         # The three what-if scenarios
├── test_pocketmoney.py    # Automated tests
├── TESTING.md             # Test results and edge cases found
└── README.md
```

The modules only take values and return results (no `input()`, `print()` or Tkinter inside them). The GUI reads the boxes, calls a module function, and shows the result.

---

## How it works

```
remaining = salary − spending − total EMI
target    = salary × saving % ÷ 100

HEALTHY   if remaining ≥ target
MODERATE  if remaining > 0
CRITICAL  otherwise
```

| What-if | Formula |
|---|---|
| Save to clear | `months = ceil(loan amount ÷ monthly saving)` |
| Buy something | `0 if price ≤ remaining, else ceil(price ÷ remaining)` |
| Pay extra | `extra = loan amount ÷ target months − EMI` |

---

## Python concepts used

Functions and modules · dictionary with list values · tuples · `for` loops · `if / elif / else` · `try / except` · CSV file handling · `math.ceil`, `math.isfinite` · f-string formatting · Tkinter (`ttk`, `StringVar`, `Style`)

---

## Testing

Run the automated tests with:

```bash
python test_pocketmoney.py
```

See [TESTING.md](TESTING.md) for the full results, the manual GUI checklist and the edge cases we found.

---

## Team

| Member | Enrolment no. | Contribution |
|---|---|---|
| Angello Iwin | S26CSEU2185 | GUI (Tkinter) and integration of all modules |
| Saksham Sangwan | S26CSEU2200 | Input validation and CSV storage (`Inputs_Saksham.py`) |
| Vansh Chauhan | S26CSEU2202 | Analysis and health rating (`Analysis_Vansh.py`) |
| Khushi Kasaudhan | S26CSEU2228 | Testing and test report (`test_pocketmoney.py`, `TESTING.md`) |
| Vasu Tripathi | S26CSEU2197 | What-if scenarios (`Whatif_Vasu.py`) |

---

## Future scope

- Interest-rate input that calculates the EMI automatically
- Login system with passwords stored as a salted hash
- Move from CSV to SQLite, then a web version
- An AI "Personal CA" for India (tax guidance, UPI categorisation, Indian languages)
