# secure_password_generator.py
"""
Develop a secure password generator (DEM-3)

Features:
- Generate passwords of configurable length
- Include uppercase, lowercase, numbers, and symbols
- Guarantee at least one character from each selected type (unless only one type selected)
- Allow exclusion of certain character types
- Command-line interface for user configuration

Usage:
    python secure_password_generator.py --length 16 --no-uppercase --no-symbols

Author: Senior_Developer (via GPT-4)
Date: 2024-06
"""

import argparse
import logging
import sys
import secrets
import string
import random

def setup_logging():
    """Initialize logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    )

def build_charsets(include_uppercase, include_lowercase, include_digits, include_symbols):
    """
    Construct individual charsets based on included types.

    Returns:
        char_dict: dict with keys for types and respective charset strings.
    """
    char_dict = {}
    if include_uppercase:
        char_dict['uppercase'] = string.ascii_uppercase
    if include_lowercase:
        char_dict['lowercase'] = string.ascii_lowercase
    if include_digits:
        char_dict['digits'] = string.digits
    if include_symbols:
        char_dict['symbols'] = string.punctuation
    return char_dict

def generate_password(length, charsets):
    """
    Generate a password with guaranteed coverage of each selected charset.

    Args:
        length: int, desired password length
        charsets: dict, charsets for each type

    Returns:
        str: generated password

    Raises:
        ValueError: if character sets are invalid or too many sets for desired length
    """
    types = list(charsets.keys())
    if not types:
        raise ValueError("Character set is empty. Cannot generate password.")
    if length < len(types):
        raise ValueError(
            f"Password length ({length}) is less than number "
            f"of selected character types ({len(types)})."
        )

    # Pick at least one from each enabled type
    password_chars = [
        secrets.choice(charsets[type_name]) for type_name in types
    ]
    all_chars = ''.join(charsets.values())

    # Fill the rest with random choices
    for _ in range(length - len(types)):
        password_chars.append(secrets.choice(all_chars))

    # Shuffle to avoid predictable ordering
    random.shuffle(password_chars)

    return ''.join(password_chars)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Secure Random Password Generator'
    )
    parser.add_argument('--length', type=int, default=12,
                        help='Length of the password to generate (default: 12)')
    parser.add_argument('--no-uppercase', action='store_true',
                        help='Exclude uppercase letters')
    parser.add_argument('--no-lowercase', action='store_true',
                        help='Exclude lowercase letters')
    parser.add_argument('--no-digits', action='store_true',
                        help='Exclude numbers')
    parser.add_argument('--no-symbols', action='store_true',
                        help='Exclude symbols')
    return parser.parse_args()

def main():
    """
    Main program logic for secure password generator.
    Handles argument parsing, charset selection, error handling, and output.
    """
    setup_logging()
    args = parse_args()
    logging.info(f"Password length requested: {args.length}")

    if args.length < 4:
        logging.error("Password length must be at least 4 for reasonable security.")
        print("ERROR: Minimum password length is 4.")
        sys.exit(1)

    include_uppercase = not args.no_uppercase
    include_lowercase = not args.no_lowercase
    include_digits = not args.no_digits
    include_symbols = not args.no_symbols

    charsets = build_charsets(
        include_uppercase,
        include_lowercase,
        include_digits,
        include_symbols
    )

    if not charsets:
        logging.error("No character types selected; cannot generate password.")
        print("ERROR: You must select at least one character type.")
        sys.exit(1)

    try:
        password = generate_password(args.length, charsets)
        logging.info("Password generated successfully.")
        print(f"Generated password: {password}")
    except Exception as e:
        logging.exception("Failed to generate password.")
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()