# email_generator_app.py

import streamlit as st
from google.generativeai import GenerativeModel, configure
from fpdf import FPDF
import os
from dotenv import load_dotenv

# Load Gemini API Key
load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model
model = GenerativeModel('gemini-pro')

# App title
st.title("📧 AI Email Generator")

# User Instructions
st.markdown("Enter your message or idea. Select the desired tone and format, then click **Generate Email**.")

# Input fields
user_input = st.text_area("Enter your content", height=150)

tone = st.selectbox("Choose tone", ["Formal", "Informal", "Professional", "Friendly"])
format_type = st.selectbox("Choose format", ["Apology", "Follow-up", "Request", "Invitation", "Thank you"])

# Session state to hold latest email
if "latest_email" not in st.session_state:
    st.session_state.latest_email = ""

# Generate Email
if st.button("Generate Email"):
    if not user_input.strip():
        st.warning("Please enter some input text.")
    else:
        prompt = f"""Write an email in a {tone} tone using the format of a {format_type} email.
        Content to include: {user_input}"""
        
        try:
            response = model.generate_content(prompt)
            st.session_state.latest_email = response.text
            st.success("✅ Email generated!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Show the generated email
if st.session_state.latest_email:
    st.subheader("Generated Email:")
    st.text_area("Email Output", st.session_state.latest_email, height=300)

    # Regenerate with different tone/format
    if st.button("🔁 Regenerate with new Tone/Format"):
        if not user_input.strip():
            st.warning("Please enter some input text.")
        else:
            prompt = f"""Rewrite the same content but in a {tone} tone and {format_type} format."""
            try:
                response = model.generate_content(prompt)
                st.session_state.latest_email = response.text
                st.success("✅ Email regenerated!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Download PDF
    def save_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf_path = "/tmp/generated_email.pdf"
        pdf.output(pdf_path)
        return pdf_path

    pdf_file = save_pdf(st.session_state.latest_email)
    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download as PDF", f, file_name="email_output.pdf", mime="application/pdf")
