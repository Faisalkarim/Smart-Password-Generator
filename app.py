import streamlit as st
import random
import string
import secrets

# --- Function to generate password ---
def generate_password(length, use_upper, use_lower, use_digits, use_special, avoid_ambiguous):
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
    ambiguous = "O0l1I"

    pool = ''
    if use_upper:
        pool += upper
    if use_lower:
        pool += lower
    if use_digits:
        pool += digits
    if use_special:
        pool += special

    # Remove ambiguous characters if requested
    if avoid_ambiguous:
        pool = ''.join(ch for ch in pool if ch not in ambiguous)

    if not pool:
        return ""

    # Ensure at least one of each selected type is included
    password = []
    if use_upper: password.append(secrets.choice(upper))
    if use_lower: password.append(secrets.choice(lower))
    if use_digits: password.append(secrets.choice(digits))
    if use_special: password.append(secrets.choice(special))

    while len(password) < length:
        password.append(secrets.choice(pool))

    random.shuffle(password)
    return ''.join(password[:length])

# --- Function to calculate strength ---
def password_strength(password):
    score = 0
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    types = [any(c.islower() for c in password),
             any(c.isupper() for c in password),
             any(c.isdigit() for c in password),
             any(c in string.punctuation for c in password)]
    
    score += sum(types)

    if score <= 2:
        return "Weak", "🔴"
    elif score == 3:
        return "Medium", "🟠"
    else:
        return "Strong", "🟢"

# --- Streamlit App UI ---
st.set_page_config(page_title="Smart Password Generator", layout="centered")
st.title("🔐 Smart Password Generator")

# User inputs
length = st.slider("Password Length", min_value=6, max_value=64, value=12)
use_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
use_lower = st.checkbox("Include Lowercase Letters (a-z)", value=True)
use_digits = st.checkbox("Include Numbers (0-9)", value=True)
use_special = st.checkbox("Include Special Characters (!@#$)", value=True)
avoid_ambiguous = st.checkbox("Avoid Ambiguous Characters (e.g., 0, O, l, 1)", value=False)

# Generate button
if st.button("🔁 Generate Password"):
    password = generate_password(length, use_upper, use_lower, use_digits, use_special, avoid_ambiguous)
    
    if not password:
        st.warning("Please select at least one character type.")
    else:
        strength, emoji = password_strength(password)

        # Display password
        st.code(password, language='')

        # Password strength
        st.markdown(f"**Password Strength:** {emoji} {strength}")

        # Copy to clipboard (via HTML + JS)
        st.markdown(f"""
        <input type="text" value="{password}" id="copyPass" style="width: 0; height: 0; border: none;">
        <button onclick="navigator.clipboard.writeText(document.getElementById('copyPass').value)">📋 Copy to Clipboard</button>
        """, unsafe_allow_html=True)

else:
    st.info("Click 'Generate Password' to create a secure password.")

