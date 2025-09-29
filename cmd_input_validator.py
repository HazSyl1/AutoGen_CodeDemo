# cmd_input_validator.py
import re

def validate_name(value):
    if not value:
        return False, "Field is required"
    if not (2 <= len(value) <= 30):
        return False, "Must be 2-30 characters"
    return True, ""

def validate_email(value):
    if not value:
        return False, "Field is required"
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not re.match(email_regex, value):
        return False, "Enter valid email (user@domain.com)"
    return True, ""

def validate_phone(value):
    if not value:
        return False, "Field is required"
    if not value.isdigit():
        return False, "Phone must contain only digits (e.g. 1234567890)"
    if len(value) != 10:
        return False, "Phone must be 10 digits (e.g. 1234567890)"
    return True, ""

def validate_date_of_birth(value):
    if not value:
        # Optional field
        return True, ""
    date_regex = r"^\d{4}-\d{2}-\d{2}$"  # YYYY-MM-DD
    if not re.match(date_regex, value):
        return False, "Enter valid date (YYYY-MM-DD)"
    try:
        year, month, day = map(int, value.split('-'))
        if not (1 <= month <= 12 and 1 <= day <= 31):
            return False, "Month/day out of range (valid date: YYYY-MM-DD)"
    except Exception:
        return False, "Enter valid date (YYYY-MM-DD)"
    return True, ""

FIELD_DEFINITIONS = [
    {
        "name": "name",
        "label": "Full Name",
        "required": True,
        "validator": validate_name,
        "example": "John Doe",
    },
    {
        "name": "email",
        "label": "Email",
        "required": True,
        "validator": validate_email,
        "example": "user@domain.com",
    },
    {
        "name": "phone",
        "label": "Phone Number",
        "required": True,
        "validator": validate_phone,
        "example": "1234567890",
    },
    {
        "name": "date_of_birth",
        "label": "Date of Birth",
        "required": False,
        "validator": validate_date_of_birth,
        "example": "1990-01-28",
    }
]

def validate_all_fields(inputs):
    """
    Validate all inputs and collect errors and success states.
    Returns: dict of error messages, dict of valid fields
    """
    errors = {}
    valids = {}
    for field in FIELD_DEFINITIONS:
        value = inputs.get(field['name'], '')
        valid, error = field['validator'](value)
        if valid:
            valids[field['name']] = f"[OK] {field['label']} is valid"
        else:
            errors[field['name']] = f"{field['label']}: {error}"
    return errors, valids

def run_test_case(test_inputs, case_name=""):
    print(f"\n=== Test Case: {case_name} ===")
    errors, valids = validate_all_fields(test_inputs)
    # Show valid fields
    for check in valids.values():
        print(check)
    # Show errors
    if errors:
        print("Submission blocked! Please fix the following errors:\n")
        for i, (fname, errmsg) in enumerate(errors.items()):
            print(f"[ERROR] {errmsg}")
            if i == 0:
                print("--> Please focus on this field first.")
            print(f"(Screen Reader: {errmsg})")
        print("All errors are shown above. Please correct and re-submit.\n")
    else:
        print("All fields validated successfully. Form submitted!")
        print("User inputs:")
        for field in FIELD_DEFINITIONS:
            print(f"  {field['label']}: {test_inputs.get(field['name'], '')}")

def main():
    # Sample test cases
    test_cases = [
        {
            "case_name": "All Inputs Valid",
            "inputs": {
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "phone": "1234567890",
                "date_of_birth": "1995-12-30",
            }
        },
        {
            "case_name": "Missing Required Fields",
            "inputs": {
                "name": "",
                "email": "",
                "phone": "",
                "date_of_birth": "",
            }
        },
        {
            "case_name": "Invalid Formats & Lengths",
            "inputs": {
                "name": "A",
                "email": "no-at-symbol.com",
                "phone": "12AB56789!",
                "date_of_birth": "12-31-1990",
            }
        },
        {
            "case_name": "Multiple Errors, Valid Date",
            "inputs": {
                "name": "ThisNameIsWayWayTooLongForValidationCheck",
                "email": "foo@bar",
                "phone": "12345",
                "date_of_birth": "1990-05-31",
            }
        },
        {
            "case_name": "Empty Optional Field",
            "inputs": {
                "name": "Valid User",
                "email": "valid@domain.com",
                "phone": "9876543210",
                "date_of_birth": "",
            }
        },
    ]

    for tc in test_cases:
        run_test_case(tc["inputs"], tc["case_name"])

if __name__ == "__main__":
    main()