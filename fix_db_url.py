import urllib.parse

print("\n--- DATABASE URL FIXER ---\n")
print("This script URL-encodes your password so it works with Render/Supabase.")

# Ask for components
print("1. Enter your database password (with the special characters):")
password = input("> ").strip()

print("\n2. Enter the rest of your connection string (WITHOUT the password).")
print("   It should look like: postgresql://postgres.xxxx:PASSWORD@aws-0-region.pooler.supabase.com:6543/postgres")
print("   Enter the part BEFORE the password (e.g., postgresql://postgres.xxxx):")
prefix = input("> ").strip()
if prefix.endswith(":"):
    prefix = prefix[:-1]

print("\n3. Enter the part AFTER the password (e.g., @aws-0-region.pooler.supabase.com:6543/postgres):")
suffix = input("> ").strip()
if not suffix.startswith("@"):
    suffix = "@" + suffix

# Encode
encoded_password = urllib.parse.quote_plus(password)
final_url = f"{prefix}:{encoded_password}{suffix}"

print("\n" + "="*60)
print("SUCCESS! INVALID CHARACTERS ENCODED.")
print("COPY THE LINE BELOW EXACTLY INTO RENDER 'DATABASE_URL':")
print("="*60 + "\n")
print(final_url)
print("\n" + "="*60)
