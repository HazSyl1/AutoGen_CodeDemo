# Secure Password Generator for DEM-3 JIRA Ticket

import argparse
import logging
import secrets
import string
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols):
    """
    Generate a secure random password based on user preferences.

    Args:
        length (int): Desired password length.
        use_uppercase (bool): Use uppercase letters.
        use_lowercase (bool): Use lowercase letters.
        use_digits (bool): Use digits.
        use_symbols (bool): Use symbols.

    Returns:
        str: The generated password.

    Raises:
        ValueError: If no character sets are selected or input is invalid.
    """
    logging.debug("Generating password with length=%d, uppercase=%s, lowercase=%s, digits=%s, symbols=%s",
                  length, use_uppercase, use_lowercase, use_digits, use_symbols)

    charset = ''
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_lowercase:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation

    if not charset:
        raise ValueError("At least one character type must be included.")

    if length <= 0:
        raise ValueError("Password length must be a positive integer.")

    # To ensure at least one character from each selected set, gather individual pools
    pools = []
    if use_uppercase:
        pools.append(string.ascii_uppercase)
    if use_lowercase:
        pools.append(string.ascii_lowercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)

    password_chars = [
        secrets.choice(pool) for pool in pools
    ]

    remaining_length = length - len(password_chars)
    
    if remaining_length < 0:
        raise ValueError(f"Password length must be at least the number of selected character types ({len(pools)}).")

    password_chars += [secrets.choice(charset) for _ in range(remaining_length)]
    # Shuffle the result
    secrets.SystemRandom().shuffle(password_chars)
    password = ''.join(password_chars)
    logging.info("Password generated successfully.")
    return password

def main():
    parser = argparse.ArgumentParser(
        description="Secure Password Generator (DEM-3)\nGenerates a secure password with configurable settings."
    )
    parser.add_argument(
        "-l", "--length", type=int, default=16,
        help="Length of the password (default: 16)"
    )
    parser.add_argument(
        "--no-uppercase", action="store_true",
        help="Exclude uppercase letters from the password"
    )
    parser.add_argument(
        "--no-lowercase", action="store_true",
        help="Exclude lowercase letters from the password"
    )
    parser.add_argument(
        "--no-digits", action="store_true",
        help="Exclude digits from the password"
    )
    parser.add_argument(
        "--no-symbols", action="store_true",
        help="Exclude symbols from the password"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        password = generate_password(
            length=args.length,
            use_uppercase=not args.no_uppercase,
            use_lowercase=not args.no_lowercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols
        )
        print(f"Generated password: {password}")
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()