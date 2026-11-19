
def get_total_emi(loans):
    total = 0

    for key in loans:
        total += loans[key][1]

    return total


def financial_health(earning, expenses, loans, saving_pct):
    total_emi = get_total_emi(loans)

    remaining = earning - expenses - total_emi
    target = earning * saving_pct / 100

    if remaining >= target:
        status = "HEALTHY"
    elif remaining > 0:
        status = "MODERATE"
    else:
        status = "CRITICAL"

    return remaining, status


def find_critical_loan(loans):
    if not loans:
        return None

    best_key = None
    best_emi = 0

    for key in loans:
        if loans[key][1] > best_emi:
            best_emi = loans[key][1]
            best_key = key

    return best_key


def format_loans(loans):
    if not loans:
        return "No loans added yet"

    lines = []

    for key in loans:
        amount = loans[key][0]
        emi = loans[key][1]
        months = loans[key][2]

        lines.append(
            f"{key}: ₹{amount:,.0f} | EMI ₹{emi:,.0f} | {months:.0f} months"
        )

    return "\n".join(lines)
