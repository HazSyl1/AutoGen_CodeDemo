# Secure Password Generator for JIRA DEM-2
import argparse
import sys
import secrets
import string
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """
    Generates a secure random password.
    :param length: Length of password
    :param use_upper: Include uppercase letters
    :param use_lower: Include lowercase letters
    :param use_digits: Include digits
    :param use_symbols: Include symbols
    :return: Password string
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
        logging.error("At least one character type must be included (upper, lower, digits, symbols).")
        raise ValueError("No character types selected.")

    all_chars = "".join(char_sets)

    # Ensure at least one character from each selected set is present
    password = [secrets.choice(char_set) for char_set in char_sets]

    if length < len(password):
        logging.error(f"Password length ({length}) is less than number of selected character types ({len(password)}).")
        raise ValueError("Password length is too short for the given options.")

    # Fill the rest of the password length
    password += [secrets.choice(all_chars) for _ in range(length - len(password))]

    # Shuffle the resulting password for better randomness
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def main():
    parser = argparse.ArgumentParser(
        description="Secure Password Generator"
    )
    parser.add_argument('-l', '--length', type=int, default=16,
                        help='Password length (default: 16)')
    parser.add_argument('--no-upper', action='store_true',
                        help='Exclude uppercase letters')
    parser.add_argument('--no-lower', action='store_true',
                        help='Exclude lowercase letters')
    parser.add_argument('--no-digits', action='store_true',
                        help='Exclude digits')
    parser.add_argument('--no-symbols', action='store_true',
                        help='Exclude symbols')

    args = parser.parse_args()

    length = args.length
    use_upper = not args.no_upper
    use_lower = not args.no_lower
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols

    try:
        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        logging.info(f"Generated password: {password}")
        print(password)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()