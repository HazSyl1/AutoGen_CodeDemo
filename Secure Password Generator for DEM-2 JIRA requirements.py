# Secure Password Generator for DEM-2 JIRA requirements
import argparse
import secrets
import string
import logging
import sys

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Generate a secure random password based on the given parameters."""
    if not any([use_upper, use_lower, use_digits, use_symbols]):
        raise ValueError("At least one character type must be enabled.")

    # Build character pool
    pool = ''
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    if not pool:
        raise ValueError("Character pool is empty after exclusions.")

    # Guarantee each chosen character type appears at least once (optional, but common best practice)
    chars = []
    type_pools = []
    if use_upper:
        chars.append(secrets.choice(string.ascii_uppercase))
        type_pools.append(string.ascii_uppercase)
    if use_lower:
        chars.append(secrets.choice(string.ascii_lowercase))
        type_pools.append(string.ascii_lowercase)
    if use_digits:
        chars.append(secrets.choice(string.digits))
        type_pools.append(string.digits)
    if use_symbols:
        chars.append(secrets.choice(string.punctuation))
        type_pools.append(string.punctuation)

    # Fill in the rest of the password
    while len(chars) < length:
        chars.append(secrets.choice(pool))

    # Shuffle to avoid predictable sequence
    secrets.SystemRandom().shuffle(chars)
    return ''.join(chars[:length])

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # CLI arguments
    parser = argparse.ArgumentParser(
        description='Secure Password Generator (DEM-2): Generates secure random passwords with configurable options.'
    )
    parser.add_argument('-l', '--length', type=int, default=16, help='Password length (default: 16)')
    parser.add_argument('--no-upper', action='store_true', help='Exclude uppercase letters')
    parser.add_argument('--no-lower', action='store_true', help='Exclude lowercase letters')
    parser.add_argument('--no-digits', action='store_true', help='Exclude digits')
    parser.add_argument('--no-symbols', action='store_true', help='Exclude symbols')
    args = parser.parse_args()

    try:
        if args.length < 4:
            logging.warning("Short passwords are insecure. Recommend at least 8 characters.")
        password = generate_password(
            length=args.length,
            use_upper=not args.no_upper,
            use_lower=not args.no_lower,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols
        )
        logging.info("Password generated successfully:")
        print(password)
    except Exception as e:
        logging.error(f"Error during password generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()