# ALDEBERAN ASCII Art
ascii_art = """
  _____   _____   __    __   ______   ______   ______   ______   _____   _   _
 /     \\ /     \\ /  \\  /  \\ /      \\ /      \\ /      \\ /      \\ /     \\ / \\ / \\
/  /\\  \\ /  /\\  \\ /  \\/  \\ /  /\\  \\ /  /\\  \\ /  /\\  \\ /  /\\  \\ /  \\/  \\
/  /  \\  \\ /  /  \\  \\ /  \\/\\  \\ /  /  \\  \\ /  /  \\  \\ /  /  \\  \\ /  \\/\\  \\
/  /    \\  \\ /  /    \\  \\ /  /    \\  \\ /  /    \\  \\ /  /    \\  \\ /  /    \\  \\
\\  \\     /  / \\  \\     /  / \\  \\     /  / \\  \\     /  / \\  \\     /  / \\  \\     / 
 \\  \\   /  /   \\  \\   /  /   \\  \\   /  /   \\  \\   /  /   \\  \\   /  /   \\  \\   / 
  \\  \\ /  /     \\  \\ /  /     \\  \\ /  /     \\  \\ /  /     \\  \\ /  /     \\  \\ / 
   \\  \\/  /       \\  \\/  /       \\  \\/  /       \\  \\/  /       \\  \\/  /       \\  \\
    \\  /  /         \\  /  /         \\  /  /         \\  /  /         \\  /  /         \\  /  /    
     \\/   /           \\/   /           \\/   /           \\/   /           \\/   /           \\/   
"""
print(ascii_art)

# Legal Export Calculator for Arms - AldebaranTools
# Educational simulation only. Not legal advice.

import sys

SANCTIONED_COUNTRIES = {
    'high_risk': ['Russia', 'Iran', 'North Korea', 'Syria', 'Venezuela', 'Cuba'],
    'medium_risk': ['China', 'Pakistan', 'Sudan', 'Myanmar', 'Belarus'],
    'low_risk': ['Saudi Arabia', 'India', 'Turkey']
}

CONTROLLED_ITEMS = {
    'firearms': 'High risk: Requires ITAR license, strict controls.',
    'ammunition': 'High risk: EAR/ITAR, end-use certificates needed.',
    'missiles': 'Extreme risk: WMD controls, full embargo to sanctioned.',
    'electronics': 'Medium risk: Dual-use, ECCN checks.',
    'chemicals': 'Medium risk: CWC controls for precursors.',
    'other': 'Low risk: Case-by-case.'
}

RISK_WEIGHTS = {
    'country_risk': 0.4,
    'item_risk': 0.3,
    'end_use_risk': 0.2,
    'license_status': 0.1
}

def safe_input(prompt: str) -> str:
    """Safe wrapper around input() to avoid OSError in restricted I/O environments."""
    try:
        return input(prompt)
    except (OSError, EOFError):
        print("\nInput unavailable in this environment. Exiting safely.")
        sys.exit(0)


def get_country_risk(country):
    country = country.capitalize()
    if country in SANCTIONED_COUNTRIES['high_risk']:
        return 90, "High risk: Full embargo likely."
    elif country in SANCTIONED_COUNTRIES['medium_risk']:
        return 60, "Medium risk: Partial restrictions, licenses needed."
    elif country in SANCTIONED_COUNTRIES['low_risk']:
        return 30, "Low risk: Controlled but feasible."
    else:
        return 10, "Low risk: No major sanctions."


def get_item_risk(item_type):
    item_type = item_type.lower()
    if item_type in CONTROLLED_ITEMS:
        desc = CONTROLLED_ITEMS[item_type]
        if 'Extreme risk' in desc:
            return 90
        elif 'High risk' in desc:
            return 70
        elif 'Medium risk' in desc:
            return 50
        else:
            return 30
    return 20


def get_end_use_risk(end_use):
    end_use = end_use.lower()
    if 'military' in end_use or 'defense' in end_use:
        return 80, "High risk: End-use certificate required."
    elif 'civilian' in end_use or 'dual-use' in end_use:
        return 50, "Medium risk: Potential dual-use scrutiny."
    else:
        return 20, "Low risk: Non-military use."


def get_license_status_risk(status):
    status = status.lower()
    if status == 'yes':
        return 10, "Low risk: Licensed."
    elif status == 'pending':
        return 50, "Medium risk: Pending approval."
    else:
        return 90, "High risk: No license."


def calculate_risk_score(country_risk, item_risk, end_use_risk, license_risk):
    score = (
        country_risk * RISK_WEIGHTS['country_risk'] +
        item_risk * RISK_WEIGHTS['item_risk'] +
        end_use_risk * RISK_WEIGHTS['end_use_risk'] +
        license_risk * RISK_WEIGHTS['license_status']
    )
    if country_risk > 70 and item_risk > 70:
        score += 20
    if end_use_risk > 50 and license_risk > 50:
        score += 15
    return min(score, 100)


def interpret_risk(score):
    if score < 30:
        return "Low Risk: Export likely compliant."
    elif score < 60:
        return "Medium Risk: Proceed with caution, obtain licenses."
    else:
        return "High Risk: Export not recommended without full compliance review."


def main_menu():
    print("\n--- Export Risk Calculator ---")
    print("1. Input Export Details")
    print("2. View Sanctioned Countries List")
    print("3. View Controlled Items Categories")
    print("4. Exit")
    return safe_input("Enter choice (1-4): ")


def run():
    # Detect non-interactive environments early
    if not sys.stdin.isatty():
        print("Non-interactive environment detected. Exiting safely.")
        return

    while True:
        choice = main_menu()

        if choice == '1':
            country = safe_input("Enter destination country: ")
            item_type = safe_input("Enter item type: ")
            end_use = safe_input("Enter end use: ")
            license_status = safe_input("Have license? (yes/no/pending): ")

            cr, cd = get_country_risk(country)
            ir = get_item_risk(item_type)
            er, ed = get_end_use_risk(end_use)
            lr, ld = get_license_status_risk(license_status)

            score = calculate_risk_score(cr, ir, er, lr)
            print("\n--- Risk Assessment ---")
            print(f"Country Risk: {cr} ({cd})")
            print(f"Item Risk: {ir}")
            print(f"End Use Risk: {er} ({ed})")
            print(f"License Risk: {lr} ({ld})")
            print(f"Overall Risk Score: {score:.2f}/100")
            print(interpret_risk(score))

        elif choice == '2':
            for lvl, c in SANCTIONED_COUNTRIES.items():
                print(f"{lvl}: {', '.join(c)}")

        elif choice == '3':
            for i, d in CONTROLLED_ITEMS.items():
                print(f"{i}: {d}")

        elif choice == '4':
            print("Exiting. Nameless star fades.")
            sys.exit(0)

        else:
            print("Invalid choice.")


if __name__ == '__main__':
    run()
