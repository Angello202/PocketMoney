import math


def save_to_clear(loans, critical_key, earning, saving_pct):
    """Return whole months needed to save enough to clear the critical loan."""
    monthly_saving = earning * saving_pct / 100

    if monthly_saving <= 0:
        return None

    amount = loans[critical_key][0]
    return math.ceil(amount / monthly_saving)


def buy_something(price, remaining):
    """Return 0 if affordable now, whole saving months, or None if saving is impossible."""
    if remaining <= 0:
        return None

    if price <= remaining:
        return 0

    return math.ceil(price / remaining)


def pay_extra(loans, critical_key, target_months):
    """Return the additional monthly payment needed to meet the target, or None."""
    if target_months <= 0:
        return None

    amount = loans[critical_key][0]
    emi = loans[critical_key][1]

    extra = amount / target_months - emi

    if extra < 0:
        return 0

    return round(extra, 2)
