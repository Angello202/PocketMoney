"""Automated tests for the PocketMoney team project.

Run from the folder containing this file and the three module files:
    python test_pocketmoney.py

Each test is isolated. A failure is reported and the remaining tests continue.
"""
import csv
import math
import os
import tempfile

from Inputs_Saksham import (
    validate_number, validate_percent, validate_loan,
    add_loan, save_loans, load_loans,
)
from Analysis_Vansh import (
    get_total_emi, financial_health, find_critical_loan, format_loans,
)
from Whatif_Vasu import save_to_clear, buy_something, pay_extra


TOTAL = 0
PASSED = 0
FAILED = 0


def run_test(label, test_function):
    """Run one test and print PASS or FAIL without stopping the suite."""
    global TOTAL, PASSED, FAILED
    TOTAL += 1
    try:
        test_function()
        PASSED += 1
        print(f"PASS: {label}")
    except Exception as error:
        FAILED += 1
        print(f"FAIL: {label} - {type(error).__name__}: {error}")


LOANS = {
    "loan1": [60000, 3000, 20],
    "loan2": [30000, 2600, 12],
}


# ---------- Inputs_Saksham.py ----------

def test_validate_number_normal():
    assert validate_number("40000") == 40000.0


def test_validate_number_whitespace():
    assert validate_number("  40000  ") == 40000.0


def test_validate_number_zero():
    assert validate_number("0") == 0.0


def test_validate_number_blank():
    assert validate_number("") is None


def test_validate_number_spaces():
    assert validate_number("   ") is None


def test_validate_number_letters():
    assert validate_number("hello") is None


def test_validate_number_negative():
    assert validate_number("-5") is None


def test_validate_number_nan():
    assert validate_number("nan") is None


def test_validate_number_infinity():
    assert validate_number("inf") is None


def test_validate_number_huge_finite():
    # 1e308 is huge but finite, so this implementation accepts it.
    assert validate_number("1e308") == 1e308


def test_validate_percent_zero():
    assert validate_percent("0") == 0.0


def test_validate_percent_100():
    assert validate_percent("100") == 100.0


def test_validate_percent_over_100():
    assert validate_percent("150") is None


def test_validate_percent_negative():
    assert validate_percent("-1") is None


def test_validate_loan_normal():
    assert validate_loan("60000", "3000", "20") == (60000.0, 3000.0, 20.0)


def test_validate_loan_blank_field():
    assert validate_loan("60000", "", "20") is None


def test_validate_loan_zero_amount():
    assert validate_loan("0", "3000", "20") is None


def test_validate_loan_emi_greater_than_amount():
    assert validate_loan("1000", "1200", "12") is None


def test_validate_loan_low_emi_is_currently_accepted():
    # Current code checks EMI <= amount, not whether EMI * months repays amount.
    assert validate_loan("60000", "100", "20") == (60000.0, 100.0, 20.0)


def test_validate_loan_fractional_months_currently_accepted():
    assert validate_loan("60000", "3000", "2.5") == (60000.0, 3000.0, 2.5)


def test_add_loan_first_key():
    data = {}
    assert add_loan(data, 60000, 3000, 20) == "loan1"
    assert data == {"loan1": [60000, 3000, 20]}


def test_add_loan_second_key():
    data = {"loan1": [60000, 3000, 20]}
    assert add_loan(data, 30000, 2600, 12) == "loan2"
    assert len(data) == 2


def test_add_loan_gap_key_current_bug():
    # Existing keys loan1 and loan3 cause len()+1 to overwrite loan3.
    data = {"loan1": [1000, 100, 10], "loan3": [3000, 300, 10]}
    add_loan(data, 5000, 500, 10)
    assert data["loan3"] == [5000, 500, 10]
    assert len(data) == 2


def test_save_and_load_loans_round_trip():
    data = {"loan1": [60000, 3000, 20], "loan2": [30000, 2600, 12]}
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "loans.csv")
        save_loans(data, path)
        assert load_loans(path) == {
            "loan1": [60000.0, 3000.0, 20.0],
            "loan2": [30000.0, 2600.0, 12.0],
        }


def test_load_missing_file():
    with tempfile.TemporaryDirectory() as folder:
        assert load_loans(os.path.join(folder, "missing.csv")) == {}


def test_load_empty_file():
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "empty.csv")
        open(path, "w", encoding="utf-8").close()
        assert load_loans(path) == {}


def test_load_header_only_file():
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "header.csv")
        with open(path, "w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(["key", "amount", "emi", "months"])
        assert load_loans(path) == {}


def test_load_malformed_rows_skips_bad_rows():
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "bad.csv")
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["key", "amount", "emi", "months"])
            writer.writerow(["loan1", "60000", "3000", "20"])
            writer.writerow(["loan2", "not-a-number", "200", "10"])
            writer.writerow(["loan3", "1000", "100"])  # missing column
            writer.writerow(["loan4", "2000", "200", "10"])
        assert load_loans(path) == {
            "loan1": [60000.0, 3000.0, 20.0],
            "loan4": [2000.0, 200.0, 10.0],
        }


# ---------- Analysis_Vansh.py ----------

def test_total_emi():
    assert get_total_emi(LOANS) == 5600


def test_total_emi_no_loans():
    assert get_total_emi({}) == 0


def test_financial_health_normal():
    assert financial_health(40000, 18000, LOANS, 20) == (16400, "HEALTHY")


def test_financial_health_exact_saving_target():
    # 40,000 * 20% = 8,000; remaining exactly 8,000 is HEALTHY.
    assert financial_health(40000, 32000, {}, 20) == (8000, "HEALTHY")


def test_financial_health_moderate():
    assert financial_health(40000, 34000, {}, 20) == (6000, "MODERATE")


def test_financial_health_critical_at_zero():
    assert financial_health(40000, 40000, {}, 20) == (0, "CRITICAL")


def test_financial_health_critical_negative():
    assert financial_health(40000, 41000, {}, 20) == (-1000, "CRITICAL")


def test_financial_health_zero_saving_target():
    assert financial_health(40000, 40000, {}, 0) == (0, "HEALTHY")


def test_critical_loan_highest_emi():
    assert find_critical_loan(LOANS) == "loan1"


def test_critical_loan_empty():
    assert find_critical_loan({}) is None


def test_critical_loan_tie_first_key_wins():
    data = {"loan1": [1000, 500, 2], "loan2": [2000, 500, 4]}
    assert find_critical_loan(data) == "loan1"


def test_format_loans_empty():
    assert format_loans({}) == "No loans added yet"


def test_format_loans_contains_both_loan_names():
    result = format_loans(LOANS)
    assert "loan1" in result and "loan2" in result


# ---------- Whatif_Vasu.py ----------

def test_save_to_clear_normal():
    assert save_to_clear(LOANS, "loan1", 40000, 20) == 8


def test_save_to_clear_zero_saving():
    assert save_to_clear(LOANS, "loan1", 40000, 0) is None


def test_save_to_clear_critical_budget_still_returns_months():
    # This function uses salary * saving_pct, not actual remaining cash.
    assert save_to_clear(LOANS, "loan1", 10000, 20) == 30


def test_buy_something_normal():
    assert buy_something(30000, 16400) == 2


def test_buy_something_price_equal_remaining():
    assert buy_something(16400, 16400) == 0


def test_buy_something_price_greater_remaining():
    assert buy_something(20000, 16400) == 2


def test_buy_something_no_money_left():
    assert buy_something(1000, 0) is None


def test_buy_something_negative_remaining():
    assert buy_something(1000, -100) is None


def test_pay_extra_normal():
    assert pay_extra(LOANS, "loan1", 10) == 3000.0


def test_pay_extra_target_zero():
    assert pay_extra(LOANS, "loan1", 0) is None


def test_pay_extra_already_meets_target():
    assert pay_extra(LOANS, "loan1", 30) == 0


def test_pay_extra_rounds_to_two_decimals():
    data = {"loan1": [1000, 100, 3]}
    assert pay_extra(data, "loan1", 3) == 233.33



# ---------- Additional edge-case tests ----------

def test_validate_number_underscore_currently_accepted():
    assert validate_number("1_000") == 1000.0


def test_validate_number_arabic_digits_currently_accepted():
    assert validate_number("١٢٣") == 123.0


def test_validate_number_negative_zero_currently_accepted():
    value = validate_number("-0")
    assert value == 0.0
    assert math.copysign(1, value) == -1.0


def test_load_duplicate_csv_key_later_row_overwrites():
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "duplicate.csv")
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["key", "amount", "emi", "months"])
            writer.writerow(["loan1", "60000", "3000", "20"])
            writer.writerow(["loan1", "90000", "4500", "20"])
        assert load_loans(path) == {"loan1": [90000.0, 4500.0, 20.0]}


def test_load_csv_zero_emi_currently_accepted():
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "zero_emi.csv")
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["key", "amount", "emi", "months"])
            writer.writerow(["loan1", "60000", "0", "20"])
        assert load_loans(path) == {"loan1": [60000.0, 0.0, 20.0]}


def test_critical_loan_all_zero_emi_returns_none():
    data = {"loan1": [60000, 0, 20], "loan2": [30000, 0, 12]}
    assert find_critical_loan(data) is None


def test_buy_something_negative_price_currently_affordable():
    # The GUI validator rejects negative prices, but the function itself does not.
    assert buy_something(-500, 1000) == 0


def test_pay_extra_fractional_target_currently_accepted():
    data = {"loan1": [60000, 3000, 20]}
    assert pay_extra(data, "loan1", 2.5) == 21000.0


if __name__ == "__main__":
    print("========== POCKETMONEY AUTOMATED TESTS ==========")
    # Input tests
    run_test("IN-01 validate_number normal", test_validate_number_normal)
    run_test("IN-02 validate_number trims whitespace", test_validate_number_whitespace)
    run_test("IN-03 validate_number accepts zero", test_validate_number_zero)
    run_test("IN-04 validate_number rejects blank", test_validate_number_blank)
    run_test("IN-05 validate_number rejects spaces", test_validate_number_spaces)
    run_test("IN-06 validate_number rejects letters", test_validate_number_letters)
    run_test("IN-07 validate_number rejects negative", test_validate_number_negative)
    run_test("IN-08 validate_number rejects NaN", test_validate_number_nan)
    run_test("IN-09 validate_number rejects infinity", test_validate_number_infinity)
    run_test("IN-10 validate_number accepts huge finite 1e308", test_validate_number_huge_finite)
    run_test("IN-11 validate_percent accepts 0", test_validate_percent_zero)
    run_test("IN-12 validate_percent accepts 100", test_validate_percent_100)
    run_test("IN-13 validate_percent rejects above 100", test_validate_percent_over_100)
    run_test("IN-14 validate_percent rejects negative", test_validate_percent_negative)
    run_test("IN-15 validate_loan normal", test_validate_loan_normal)
    run_test("IN-16 validate_loan rejects blank field", test_validate_loan_blank_field)
    run_test("IN-17 validate_loan rejects zero amount", test_validate_loan_zero_amount)
    run_test("IN-18 validate_loan rejects EMI above amount", test_validate_loan_emi_greater_than_amount)
    run_test("IN-19 validate_loan accepts low total repayment (suspected bug)", test_validate_loan_low_emi_is_currently_accepted)
    run_test("IN-20 validate_loan accepts fractional months (suspected bug)", test_validate_loan_fractional_months_currently_accepted)
    run_test("IN-21 add_loan creates loan1", test_add_loan_first_key)
    run_test("IN-22 add_loan creates loan2", test_add_loan_second_key)
    run_test("IN-23 add_loan overwrites key after a gap (suspected bug)", test_add_loan_gap_key_current_bug)
    run_test("IN-24 save_loans/load_loans round trip", test_save_and_load_loans_round_trip)
    run_test("IN-25 load_loans missing file", test_load_missing_file)
    run_test("IN-26 load_loans empty file", test_load_empty_file)
    run_test("IN-27 load_loans header only", test_load_header_only_file)
    run_test("IN-28 load_loans skips malformed rows", test_load_malformed_rows_skips_bad_rows)

    # Analysis tests
    run_test("AN-01 total EMI", test_total_emi)
    run_test("AN-02 total EMI with no loans", test_total_emi_no_loans)
    run_test("AN-03 financial health normal", test_financial_health_normal)
    run_test("AN-04 remaining equals saving target", test_financial_health_exact_saving_target)
    run_test("AN-05 financial health moderate", test_financial_health_moderate)
    run_test("AN-06 financial health zero is critical", test_financial_health_critical_at_zero)
    run_test("AN-07 financial health negative is critical", test_financial_health_critical_negative)
    run_test("AN-08 zero saving target", test_financial_health_zero_saving_target)
    run_test("AN-09 find highest EMI loan", test_critical_loan_highest_emi)
    run_test("AN-10 find critical loan with no loans", test_critical_loan_empty)
    run_test("AN-11 critical loan EMI tie", test_critical_loan_tie_first_key_wins)
    run_test("AN-12 format empty loans", test_format_loans_empty)
    run_test("AN-13 format loan list", test_format_loans_contains_both_loan_names)

    # What-if tests
    run_test("WI-01 save to clear normal", test_save_to_clear_normal)
    run_test("WI-02 save to clear with zero saving", test_save_to_clear_zero_saving)
    run_test("WI-03 save to clear when budget is critical", test_save_to_clear_critical_budget_still_returns_months)
    run_test("WI-04 buy something normal", test_buy_something_normal)
    run_test("WI-05 price equals remaining", test_buy_something_price_equal_remaining)
    run_test("WI-06 price greater than remaining", test_buy_something_price_greater_remaining)
    run_test("WI-07 buy with zero remaining", test_buy_something_no_money_left)
    run_test("WI-08 buy with negative remaining", test_buy_something_negative_remaining)
    run_test("WI-09 pay extra normal", test_pay_extra_normal)
    run_test("WI-10 pay extra target zero", test_pay_extra_target_zero)
    run_test("WI-11 pay extra when current EMI is enough", test_pay_extra_already_meets_target)
    run_test("WI-12 pay extra rounds result", test_pay_extra_rounds_to_two_decimals)

    # Additional edge-case tests
    run_test("IN-29 underscore in number accepted", test_validate_number_underscore_currently_accepted)
    run_test("IN-30 Arabic digits accepted", test_validate_number_arabic_digits_currently_accepted)
    run_test("IN-31 negative zero accepted", test_validate_number_negative_zero_currently_accepted)
    run_test("IN-32 duplicate CSV key overwrites earlier loan", test_load_duplicate_csv_key_later_row_overwrites)
    run_test("IN-33 CSV loader accepts zero EMI", test_load_csv_zero_emi_currently_accepted)
    run_test("AN-14 all zero-EMI loans produce no critical key", test_critical_loan_all_zero_emi_returns_none)
    run_test("WI-13 negative price is treated as affordable", test_buy_something_negative_price_currently_affordable)
    run_test("WI-14 fractional pay-extra target accepted", test_pay_extra_fractional_target_currently_accepted)

    print("\n========== TEST SUMMARY ==========")
    print(f"Total tests: {TOTAL}")
    print(f"Passed: {PASSED}")
    print(f"Failed: {FAILED}")
    print(f"{PASSED}/{TOTAL} passed")
