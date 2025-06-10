# email_generator_app.py

import streamlit as st
from google.generativeai import GenerativeModel, configure
from fpdf import FPDF

# --- SET YOUR API KEY HERE ---
GEMINI_API_KEY = "AIzaSyCqzY2VImY7KaTWSLqfQth86DacZFkDSMI"  # Replace this with your key

# --- Configure Gemini ---
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-2.0-flash')

# --- App Title & Instructions ---
st.set_page_config(page_title="AI Email Generator", layout="centered")
st.title("📨 AI-Powered Email Generator using Gemini API")
st.markdown("Follow the steps below to generate and download a customized email.\n\n")

# --- User Input Section ---
st.subheader("Step 1: Enter Your Message Idea")
user_input = st.text_area("✏️ What should the email be about?", height=150, placeholder="e.g. Requesting a meeting with a client...")

st.subheader("Step 2: Select Tone and Format")
tone = st.selectbox("🎭 Choose Tone", ["Formal", "Informal", "Professional", "Friendly"])
format_type = st.selectbox("📄 Choose Format", ["Request", "Apology", "Invitation", "Follow-up", "Thank You"])

# --- Generate & Regenerate ---
st.subheader("Step 3: Generate or Regenerate Email")

# Memory storage
if "email_output" not in st.session_state:
    st.session_state.email_output = ""

# Function to generate email
def generate_email(input_text, tone, format_type):
    prompt = f"""
    Compose an email in a {tone} tone using the {format_type} format.
    The content should be based on the following input:\n\n"{input_text}"
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Generate Email Button
if st.button("🛠️ Generate Email"):
    if not user_input.strip():
        st.warning("Please provide the email content idea first.")
    else:
        email_text = generate_email(user_input, tone, format_type)
        st.session_state.email_output = email_text
        st.success("✅ Email generated successfully!")

# Regenerate Email Button
if st.button("🔁 Regenerate with New Format or Tone"):
    if not user_input.strip():
        st.warning("Please enter the main idea for the email first.")
    else:
        email_text = generate_email(user_input, tone, format_type)
        st.session_state.email_output = email_text
        st.success("✅ Email regenerated with new settings!")

# --- Display Output Email ---
if st.session_state.email_output:
    st.subheader("📬 Your Generated Email")
    st.text_area("Generated Email", value=st.session_state.email_output, height=300)

    # --- PDF Download ---
    def convert_to_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.multi_cell(0, 10, line)
        output_path = "C:/Users/THOMASSOFY/Desktop/email_output.pdf"
        pdf.output(output_path)
        return output_path

    pdf_path = convert_to_pdf(st.session_state.email_output)
    with open(pdf_path, "rb") as file:
        st.download_button("📥 Download as PDF", file, file_name="generated_email.pdf", mime="application/pdf")

