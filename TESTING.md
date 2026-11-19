# PocketMoney – Testing Report

**Team:** Saksham (Inputs), Vansh (Analysis), Vasu (What-if), Angello (GUI)  
**Date:** 19 November 2026  
**Project:** PocketMoney – Tkinter personal finance application

## 1. Purpose

This report records automated tests, observed edge cases, suspected defects, and manual GUI checks for PocketMoney. The automated tests exercise the functions in `Inputs_Saksham.py`, `Analysis_Vansh.py`, and `Whatif_Vasu.py`. GUI checks are recorded separately because they require interaction with the running application.

## 2. How to run the tests

Keep `test_pocketmoney.py` in the same folder as the project modules, then run:

```bash
python test_pocketmoney.py
```

The test runner prints `PASS` or `FAIL` for each test and displays a final count.

## 3. Automated test summary

| Measure | Result |
|---|---:|
| Total automated tests | 61 |
| Passed | 61 |
| Failed | 0 |
| Result | **61/61 passed** |

**Important interpretation:** Some tests are characterization tests. They confirm the current program behaviour even when that behaviour is listed below as a suspected defect. A passing characterization test does not mean the behaviour is approved; change its expected result after the team agrees on and implements the requirement.

## 4. Automated test results

| ID | Area | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| IN-01 | Number validation | "40000" | 40000.0 | 40000.0 | PASS |
| IN-02 | Number validation | "  40000  " | 40000.0 | 40000.0 | PASS |
| IN-03 | Number validation | "0" | 0.0 | 0.0 | PASS |
| IN-04 | Number validation | "" | None | None | PASS |
| IN-05 | Number validation | "   " | None | None | PASS |
| IN-06 | Number validation | "hello" | None | None | PASS |
| IN-07 | Number validation | "-5" | None | None | PASS |
| IN-08 | Number validation | "nan" | None | None | PASS |
| IN-09 | Number validation | "inf" | None | None | PASS |
| IN-10 | Number validation | "1e308" | 1e308 (finite value accepted) | 1e308 | PASS |
| IN-11 | Percentage validation | "0" | 0.0 | 0.0 | PASS |
| IN-12 | Percentage validation | "100" | 100.0 | 100.0 | PASS |
| IN-13 | Percentage validation | "150" | None | None | PASS |
| IN-14 | Percentage validation | "-1" | None | None | PASS |
| IN-15 | Loan validation | 60000, 3000, 20 | (60000.0, 3000.0, 20.0) | Same | PASS |
| IN-16 | Loan validation | 60000, blank EMI, 20 | None | None | PASS |
| IN-17 | Loan validation | 0, 3000, 20 | None | None | PASS |
| IN-18 | Loan validation | 1000, 1200, 12 | None | None | PASS |
| IN-19 | Loan validation | 60000, 100, 20 | Accepted (suspected repayment bug) | Accepted | PASS |
| IN-20 | Loan validation | 60000, 3000, 2.5 | Accepted (fractional tenure) | Accepted | PASS |
| IN-21 | Add loan | Empty dictionary + loan details | Creates loan1 | loan1 created | PASS |
| IN-22 | Add loan | Dictionary with loan1 | Creates loan2 | loan2 created | PASS |
| IN-23 | Add loan | Existing loan1 and loan3 | Must not overwrite existing loan (desired) | Overwrites loan3 | PASS |
| IN-24 | CSV save/load | Two valid loans | Same loans after round trip | Same loan data; numeric values load as floats | PASS |
| IN-25 | CSV loading | Missing file | Empty dictionary | {} | PASS |
| IN-26 | CSV loading | Empty file | Empty dictionary | {} | PASS |
| IN-27 | CSV loading | Header only | Empty dictionary | {} | PASS |
| IN-28 | CSV loading | Valid rows plus text/missing-column rows | Keep valid rows; skip malformed rows | Valid rows kept; malformed rows skipped | PASS |
| IN-29 | Number validation | "1_000" | Policy decision: accept or reject consistently | 1000.0 accepted | PASS |
| IN-30 | Number validation | "١٢٣" | Policy decision: accept Unicode digits or reject | 123.0 accepted | PASS |
| IN-31 | Number validation | "-0" | Normalize to positive zero if negative-zero display is unwanted | -0.0 accepted | PASS |
| IN-32 | CSV loading | Two rows with same key loan1 | Reject duplicate or define overwrite policy | Later row overwrites earlier row | PASS |
| IN-33 | CSV loading | Loan row with EMI 0 | Reject invalid loan consistently | Zero-EMI loan accepted | PASS |
| AN-01 | Total EMI | loan1 EMI 3000 + loan2 EMI 2600 | 5600 | 5600 | PASS |
| AN-02 | Total EMI | No loans | 0 | 0 | PASS |
| AN-03 | Financial health | Salary 40000; spending 18000; EMIs 5600; saving 20% | (16400, HEALTHY) | (16400, HEALTHY) | PASS |
| AN-04 | Financial health | Remaining exactly 8000; saving target 8000 | (8000, HEALTHY) | (8000, HEALTHY) | PASS |
| AN-05 | Financial health | Remaining 6000; saving target 8000 | (6000, MODERATE) | (6000, MODERATE) | PASS |
| AN-06 | Financial health | Remaining exactly 0 | (0, CRITICAL) | (0, CRITICAL) | PASS |
| AN-07 | Financial health | Remaining -1000 | (-1000, CRITICAL) | (-1000, CRITICAL) | PASS |
| AN-08 | Financial health | Zero saving target; remaining 0 | (0, HEALTHY) | (0, HEALTHY) | PASS |
| AN-09 | Critical loan | loan1 EMI 3000; loan2 EMI 2600 | loan1 | loan1 | PASS |
| AN-10 | Critical loan | No loans | None | None | PASS |
| AN-11 | Critical loan | Two loans tied at EMI 500 | First inserted loan | loan1 (first inserted) | PASS |
| AN-12 | Loan formatting | No loans | No loans added yet | No loans added yet | PASS |
| AN-13 | Loan formatting | Two-loan dictionary | Formatted text contains both loan IDs | Both IDs present | PASS |
| AN-14 | Critical loan | All loans have EMI 0 | Return a defined critical loan or explicitly handle no positive EMI | None despite loans existing | PASS |
| WI-01 | Save to clear | loan1 amount 60000; salary 40000; saving 20% | 8 months | 8 | PASS |
| WI-02 | Save to clear | Saving percentage 0 | None | None | PASS |
| WI-03 | Save to clear | Salary 10000; saving 20%; critical cashflow | Should use affordable free cash or clearly disclose assumption | 30 months based on salary percentage | PASS |
| WI-04 | Buy something | Price 30000; remaining 16400 | 2 months | 2 | PASS |
| WI-05 | Buy something | Price exactly 16400; remaining 16400 | 0 (buy now) | 0 | PASS |
| WI-06 | Buy something | Price 20000; remaining 16400 | 2 months | 2 | PASS |
| WI-07 | Buy something | Remaining 0 | None | None | PASS |
| WI-08 | Buy something | Remaining -100 | None | None | PASS |
| WI-09 | Pay extra | loan1; target 10 months | 3000.0 | 3000.0 | PASS |
| WI-10 | Pay extra | Target 0 months | None | None | PASS |
| WI-11 | Pay extra | Target 30 months; existing EMI sufficient | 0 | 0 | PASS |
| WI-12 | Pay extra | Amount 1000; EMI 100; target 3 | 233.33 | 233.33 | PASS |
| WI-13 | Buy something | Price -500; remaining 1000 | Reject negative price | 0 (treated as affordable) | PASS |
| WI-14 | Pay extra | Target 2.5 months | Policy decision: whole months or explicit fractional support | Accepted; 21000.0 | PASS |

## 5. Edge cases & bugs found

| ID | Description | Severity (High/Medium/Low) | File/owner | Suggested fix | Status (Open/Fixed) |
|---|---|---|---|---|---|
| EC-01 | `validate_number("1_000")` accepts an underscore-separated value. Confirm whether this input format is allowed. | Low | `Inputs_Saksham.py` / Saksham | Define the accepted number format; reject underscores explicitly if not supported. | Open |
| EC-02 | Arabic-Indic digits are accepted by `float()`. This is not inherently a defect; confirm the intended language/input policy. | Low | `Inputs_Saksham.py` / Saksham | Keep Unicode digit support intentionally, or restrict to the agreed input format. | Open |
| EC-03 | `-0` is accepted as `-0.0` and may display as negative zero. | Low | `Inputs_Saksham.py` / Saksham | Normalize any value equal to zero to `0.0`. | Open |
| EC-04 | A loan of ₹60,000 with EMI ₹100 for 20 months is accepted although total instalments equal only ₹2,000. | High | `Inputs_Saksham.py` / Saksham | If interest-free full repayment is the rule, validate `emi * months >= amount`; otherwise define the interest/tenure model. | Open |
| EC-05 | Fractional loan tenure such as 2.5 months is accepted. | Medium | `Inputs_Saksham.py` / Saksham | Require an integer number of months if the app models whole monthly instalments. | Open |
| EC-06 | `add_loan()` uses `len(loans) + 1`, so a dictionary containing `loan1` and `loan3` can have `loan3` overwritten. | High | `Inputs_Saksham.py` / Saksham | Generate the next unused loan key; never overwrite an existing key. | Open |
| EC-07 | `save_to_clear()` uses a percentage of salary and does not receive actual remaining cash after expenses and EMIs. It can report a payoff time even when the budget is critical. | Medium | `Whatif_Vasu.py` / Vasu | Pass the actual affordable monthly amount into the function, or clearly label the calculation as a salary-based saving assumption. | Open |
| EC-08 | With equal EMIs, `find_critical_loan()` returns the first loan in dictionary order. | Low | `Analysis_Vansh.py` / Vansh | Document the tie-break rule or add a secondary rule if the team needs one. | Open |
| EC-09 | Duplicate loan keys in a CSV silently overwrite earlier rows during loading. | Medium | `Inputs_Saksham.py` / Saksham | Detect duplicate keys and skip/report the duplicate instead of silently replacing data. | Open |
| EC-10 | `load_loans()` accepts a zero-EMI loan, although `validate_loan()` rejects zero EMI. | Medium | `Inputs_Saksham.py` / Saksham | Apply the same loan validation rules when loading CSV rows. | Open |
| EC-11 | If all loaded loans have EMI 0, `find_critical_loan()` returns `None` even though loans exist. | Medium | `Analysis_Vansh.py` / Vansh | Define how zero-EMI loans should be handled and keep the result consistent with the app's meaning of critical loan. | Open |
| EC-12 | `buy_something()` returns 0 for a negative price when remaining money is positive. The GUI validator normally blocks this, but the function itself does not. | Low | `Whatif_Vasu.py` / Vasu | Reject negative prices inside the function as well as at the GUI input layer. | Open |
| EC-13 | `pay_extra()` accepts fractional target months. | Medium | `Whatif_Vasu.py` / Vasu | Validate a positive whole-number target if fractional months are not part of the requirements. | Open |
| GUI-01 | GUI validation uses chained comparisons `saving_pct is loans=={}` and `saving_pct is None=={}` instead of the intended `or` checks. | Medium | `PoketMoney_GUI.py` / Angello | Replace with explicit conditions such as `saving_pct is None` and, where required, `loans == {}`. | Open |

### CSV loader cases that behaved as expected

- An empty CSV returns an empty dictionary.
- A CSV containing only the header returns an empty dictionary.
- Rows with missing columns or non-numeric values are skipped while valid rows are loaded.
- A missing file returns an empty dictionary.

## 6. Manual GUI test checklist

**GUI launch:** Pass — the application was opened successfully.  
**Individual interaction checks:** Pending user execution; do not mark these as passed until each has been tried.

| ID | Manual test | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| GUI-M01 | Click every button with every input box blank | Show a suitable validation message; do not crash | Not run | Pending |
| GUI-M02 | Leave hint text `Enter EMI` in the EMI box and click Add loan | Reject the hint as invalid input; do not add a loan | Not run | Pending |
| GUI-M03 | Click Calculate with 0 loans | Show a sensible summary or validation message; do not crash | Not run | Pending |
| GUI-M04 | Use each what-if before adding any loan | Show a validation message; do not crash | Not run | Pending |
| GUI-M05 | Use each what-if twice | Button should grey out after the first valid use, according to the stated requirement | Not run | Pending |
| GUI-M06 | Enter a price larger than remaining money | Show the number of months needed, or a clear no-money-left message | Not run | Pending |
| GUI-M07 | Enter saving percentage 0 | Accept 0%; handle saving-dependent what-if safely | Not run | Pending |
| GUI-M08 | Enter saving percentage 100 | Accept 100% and calculate correctly | Not run | Pending |
| GUI-M09 | Enter saving percentage 150 | Reject the value and show a validation message | Not run | Pending |

### Manual test recording instructions

After each test, replace `Not run` with the observed output and change `Pending` to `Pass` or `Fail`. If a test fails, record the exact message or unexpected behaviour in the Actual result column.

## 7. Known limitations

1. The what-if calculations do not model loan interest, changing interest rates, fees, or amortization schedules.
2. `save_to_clear()` currently calculates saving from salary percentage, not necessarily the cash genuinely available after expenses and EMIs.
3. `buy_something()` estimates months using the current remaining amount as a constant monthly saving amount.
4. `pay_extra()` calculates a simplified additional payment and does not model interest or lender-specific repayment rules.
5. CSV loading skips malformed rows rather than presenting a detailed recovery report to the user.
6. GUI launch success does not prove every button, validation path, or what-if workflow works correctly.

## 8. Conclusion

The automated suite currently reports **61 passed and 0 failed**. The tests also identify input-validation, loan-key, CSV consistency, calculation-assumption, and GUI-condition issues that should be reviewed by the team. Manual GUI interaction checks remain pending, apart from confirming that the application launches successfully.
