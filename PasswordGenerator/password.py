import secrets
import string
import sys

MIN_LENGTH = 8
DEFAULT_LENGTH = 12
EXCLUDED_CHARS = "O0l1"

def generate_password(length: int, exclude_ambiguous: bool = False) -> str:
    if length < MIN_LENGTH:
        raise ValueError(f"🚫 Password length must be at least {MIN_LENGTH} characters for security.")

    charset = string.ascii_letters + string.digits + string.punctuation
    if exclude_ambiguous:
        charset = ''.join(c for c in charset if c not in EXCLUDED_CHARS)

    # Ensure password meets complexity rules
    while True:
        password = ''.join(secrets.choice(charset) for _ in range(length))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

def request_length(default: int = DEFAULT_LENGTH) -> int:
    print("🔐 Welcome to the Secure Password Generator!")
    print("You can customize your password length and character preferences.")
    print(f"Minimum recommended length: {MIN_LENGTH} characters\n")

    prompt = f"🔢 Enter desired password length (default={default}): "
    user_input = input(prompt).strip()

    if not user_input:
        print(f"ℹ️ No input provided. Using default length: {default}")
        return default

    try:
        length = int(user_input)
        if length < 1:
            raise ValueError
        return length
    except ValueError:
        print(f"⚠️ Invalid input. Falling back to default length: {default}", file=sys.stderr)
        return default

def ask_exclusion() -> bool:
    print("\n🚫 Ambiguous characters like 'O', '0', 'l', and '1' can be confusing.")
    choice = input("Would you like to exclude them from your password? (y/n): ").strip().lower()
    return choice == 'y'

def assess_strength(length: int) -> str:
    if length < 10:
        return "🟡 Weak — consider using at least 12 characters."
    elif length < 14:
        return "🟠 Moderate — good, but longer is stronger."
    else:
        return "🟢 Strong — great choice for security!"

def main() -> None:
    length = request_length()
    exclude = ask_exclusion()

    print("\n🔄 Generating your secure password...")
    try:
        password = generate_password(length, exclude)
    except Exception as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        sys.exit(1)

    strength = assess_strength(length)
    print("\n✅ Your password has been generated successfully!")
    print(f"🔑 Password: {password}")
    print(f"📊 Strength: {strength}")
    print("\n💡 Tip: Store your password securely. Consider using a password manager.")

if __name__ == "__main__":
    main()
