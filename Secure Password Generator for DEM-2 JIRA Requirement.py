# Secure Password Generator for DEM-2 JIRA Requirement
import argparse
import logging
import string
import secrets
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_password(length, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    """
    Generate a secure random password.

    Parameters:
    - length (int): Length of the password
    - use_upper (bool): Include uppercase letters
    - use_lower (bool): Include lowercase letters
    - use_digits (bool): Include digits
    - use_symbols (bool): Include special symbols

    Returns:
    - str: Generated password
    """

    char_sets = []
    if use_upper:
        char_sets.append(string.ascii_uppercase)
    if use_lower:
        char_sets.append(string.ascii_lowercase)
    if use_digits:
        char_sets.append(string.digits)
    if use_symbols:
        char_sets.append(string.punctuation)

    if not char_sets:
        raise ValueError("At least one character type must be included.")

    # Ensure password contains at least one character from each selected set
    password = [secrets.choice(char_set) for char_set in char_sets]

    # Fill the rest of the password length with random choices from all allowed chars
    all_chars = ''.join(char_sets)
    if length < len(password):
        raise ValueError(f"Password length must be at least {len(password)} (to include one of each type).")

    password += [secrets.choice(all_chars) for _ in range(length - len(password))]
    # Shuffle result so required characters aren't always at start
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Secure Password Generator - DEM-2"
    )
    parser.add_argument(
        "-l", "--length", type=int, default=12,
        help="Length of password (default: 12)"
    )
    parser.add_argument(
        "--no-upper", action="store_true",
        help="Exclude uppercase letters"
    )
    parser.add_argument(
        "--no-lower", action="store_true",
        help="Exclude lowercase letters"
    )
    parser.add_argument(
        "--no-digits", action="store_true",
        help="Exclude digits"
    )
    parser.add_argument(
        "--no-symbols", action="store_true",
        help="Exclude symbols"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        password = generate_password(
            length=args.length,
            use_upper=not args.no_upper,
            use_lower=not args.no_lower,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols
        )
        logging.info("Password generated successfully!")
        print(f"Generated Password: {password}")
    except Exception as e:
        logging.error(f"Error generating password: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()