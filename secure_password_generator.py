# secure_password_generator.py
# Specific solution for DEM-3: Develop a secure password generator

import argparse
import secrets
import string
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    char_sets = []
    if use_upper:
        char_sets.append(string.ascii_uppercase)
    if use_lower:
        char_sets.append(string.ascii_lowercase)
    if use_digits:
        char_sets.append(string.digits)
    if use_symbols:
        char_sets.append(string.punctuation)

    logging.debug(f"Character sets enabled: {char_sets}")

    # Error if no character sets selected
    if not char_sets:
        raise ValueError("At least one character type must be included.")

    all_chars = ''.join(char_sets)
    if not all_chars:
        raise ValueError("No characters available to generate password.")

    # Ensure at least one of each selected type
    password = []
    for chars in char_sets:
        password.append(secrets.choice(chars))

    if length < len(password):
        raise ValueError(
            f"Password length must be at least the number of selected character types ({len(password)})."
        )

    # Fill the rest
    for _ in range(length - len(password)):
        password.append(secrets.choice(all_chars))

    # Shuffle to prevent predictable placement
    secrets.SystemRandom().shuffle(password)
    result = ''.join(password)
    logging.info(f"Generated password: {result}")
    return result

def parse_args():
    parser = argparse.ArgumentParser(
        description="Secure Password Generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--length", "-l", type=int, default=12, help="Length of the password"
    )
    parser.add_argument(
        "--no-upper", action="store_true", help="Exclude uppercase letters"
    )
    parser.add_argument(
        "--no-lower", action="store_true", help="Exclude lowercase letters"
    )
    parser.add_argument(
        "--no-digits", action="store_true", help="Exclude digits"
    )
    parser.add_argument(
        "--no-symbols", action="store_true", help="Exclude symbols"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    use_upper = not args.no_upper
    use_lower = not args.no_lower
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols

    try:
        password = generate_password(
            length=args.length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
            use_symbols=use_symbols
        )
        print(password)
    except Exception as e:
        logging.error(f"Password generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()