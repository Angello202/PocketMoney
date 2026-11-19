
import csv
import math


# STEP 1: Validate a number
def validate_number(text):
    text = text.strip()

    if text == "":
        return None

    try:
        number = float(text)
    except ValueError:
        return None

    if not math.isfinite(number):
        return None

    if number < 0:
        return None

    return number


# STEP 2: Validate a percentage
def validate_percent(text):
    number = validate_number(text)

    if number is None:
        return None

    if number > 100:
        return None

    return number


# STEP 3: Validate all loan details
def validate_loan(amount_text, emi_text, months_text):
    amount = validate_number(amount_text)
    emi = validate_number(emi_text)
    months = validate_number(months_text)

    if amount is None or emi is None or months is None:
        return None

    if amount == 0 or emi == 0 or months == 0:
        return None

    if emi > amount:
        return None

    return (amount, emi, months)


# STEP 4: Add a loan
def add_loan(loans, amount, emi, months):
    key = "loan" + str(len(loans) + 1)

    loans[key] = [amount, emi, months]

    return key


# STEP 5: Save loans to CSV
def save_loans(loans, filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["key", "amount", "emi", "months"])

        for key in loans:
            writer.writerow([key] + loans[key])


# STEP 6: Load loans from CSV
def load_loans(filename):
    loans = {}

    try:
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)

            next(reader, None)

            for row in reader:
                try:
                    key = row[0]
                    amount = float(row[1])
                    emi = float(row[2])
                    months = float(row[3])

                    if not key:
                        continue

                    if not all(math.isfinite(value) for value in (amount, emi, months)):
                        continue

                    if amount < 0 or emi < 0 or months < 0:
                        continue

                    loans[key] = [amount, emi, months]

                except (ValueError, IndexError):
                    continue

    except FileNotFoundError:
        return {}

    return loans

