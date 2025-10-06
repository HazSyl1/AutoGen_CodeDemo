# Secure Password Generator for JIRA DEM-3
import argparse
import logging
import secrets
import string
import sys

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def generate_password(length: int,
                      use_upper: bool,
                      use_lower: bool,
                      use_digits: bool,
                      use_symbols: bool) -> str:
    """Generate a secure random password.

    Args:
        length (int): Desired password length.
        use_upper (bool): Include uppercase letters.
        use_lower (bool): Include lowercase letters.
        use_digits (bool): Include digits.
        use_symbols (bool): Include symbols.

    Returns:
        str: The generated password.

    Raises:
        ValueError: If no character sets are selected.
    """
    char_pools = []
    if use_upper:
        char_pools.append(string.ascii_uppercase)
    if use_lower:
        char_pools.append(string.ascii_lowercase)
    if use_digits:
        char_pools.append(string.digits)
    if use_symbols:
        char_pools.append(string.punctuation)

    if not char_pools:
        raise ValueError("At least one character type must be included.")

    # Ensure at least one character from each selected set
    mandatory_chars = [secrets.choice(pool) for pool in char_pools]

    all_chars = ''.join(char_pools)

    if length < len(mandatory_chars):
        raise ValueError(
            f"Password length must be at least {len(mandatory_chars)} "
            f"to include all selected character sets.")

    password_chars = mandatory_chars + \
        [secrets.choice(all_chars) for _ in range(length - len(mandatory_chars))]
    # Shuffle password to avoid predictable order
    secrets.SystemRandom().shuffle(password_chars)
    password = ''.join(password_chars)
    return password

def parse_args():
    """CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Generate strong, secure random passwords."
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=16,
        help="Password length (default: 16)"
    )
    parser.add_argument(
        "--no-upper",
        action='store_true',
        help="Exclude uppercase letters"
    )
    parser.add_argument(
        "--no-lower",
        action='store_true',
        help="Exclude lowercase letters"
    )
    parser.add_argument(
        "--no-digits",
        action='store_true',
        help="Exclude numbers"
    )
    parser.add_argument(
        "--no-symbols",
        action='store_true',
        help="Exclude symbols"
    )
    return parser.parse_args()

def main():
    """Main driver function."""
    setup_logging()
    args = parse_args()
    logging.info("Generating password with options: length=%d, use_upper=%s, use_lower=%s, use_digits=%s, use_symbols=%s",
                 args.length,
                 not args.no_upper,
                 not args.no_lower,
                 not args.no_digits,
                 not args.no_symbols)

    try:
        password = generate_password(
            length=args.length,
            use_upper=not args.no_upper,
            use_lower=not args.no_lower,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols
        )
        print(password)
    except Exception as e:
        logging.error("Failed to generate password: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()