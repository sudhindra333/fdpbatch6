import streamlit as st
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import io

# -------------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------------
st.set_page_config(page_title="AI Family Life Goals Planner", page_icon="💑", layout="centered")
st.title("💑 AI-Powered Life Goals & Family Planner")

st.header("Enter Family Details")

# -------------------------------------------------------
# Husband & Wife Details
# -------------------------------------------------------
husband_age = st.number_input("Husband Age", min_value=18, max_value=90, value=35)
husband_income = st.number_input("Husband Monthly Income (₹)", min_value=0)

wife_age = st.number_input("Wife Age", min_value=18, max_value=90, value=32)
wife_income = st.number_input("Wife Monthly Income (₹)", min_value=0)

# -------------------------------------------------------
# Children Details Input Section
# -------------------------------------------------------
num_children = st.number_input("Number of Children", min_value=0, max_value=10, value=1)
children_details = ""

if num_children > 0:
    for i in range(num_children):
        st.subheader(f"Child {i+1} Details")
        age = st.number_input(f"Age of Child {i+1}", min_value=0, max_value=30)
        health = st.text_input(f"Health Condition of Child {i+1} (None / Minor / Major)")
        children_details += f"Child {i+1}: Age {age}, Health: {health}\n"

health_condition = st.text_area("Describe any major/minor child health issues")

# -------------------------------------------------------
# Goals Input
# -------------------------------------------------------
st.header("Life Goals")

short_goals = st.text_area("Short-Term Goals (1–3 years)")
long_goals = st.text_area("Long-Term Goals (5–20 years)")

# -------------------------------------------------------
# Generate Button
# -------------------------------------------------------
generate = st.button("Generate Life Plan")

# -------------------------------------------------------
# Prompt Builder
# -------------------------------------------------------
def build_prompt():
    return f"""
You are a certified financial planner, family counselor, and life strategy expert.

Create a detailed life goals plan for the family using the data below:

HUSBAND:
- Age: {husband_age}
- Monthly Income: {husband_income}

WIFE:
- Age: {wife_age}
- Monthly Income: {wife_income}

FAMILY:
- Number of Children: {num_children}
- Children Details:
{children_details}
- Child Health Conditions: {health_condition}

GOALS:
- Short-term: {short_goals}
- Long-term: {long_goals}

TASKS:
1. Calculate combined income.
2. Plan recommended monthly budget split:
   - Household expenses
   - Emergency fund
   - Health insurance
   - Life insurance
   - Investments (safe categories only)
   - Child education fund
   - Child medical care fund (if needed)
3. Create tables for:
   - Income Summary
   - Recommended Expense Allocation
   - Goal Achievement Timeline (1yr, 5yrs, 10yrs, 20yrs)
   - Child Health Support Plan (if applicable)
   - Investment Priority Roadmap
4. Provide safe, educational recommendations — no financial advice.
5. Keep it professional, structured, and actionable.
"""


# -------------------------------------------------------
# helper function: Generate PDF file
# -------------------------------------------------------
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 7, line)

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output


# -------------------------------------------------------
# helper: Convert text report to CSV and Excel
# -------------------------------------------------------
def text_to_dataframe(text):
    """Simple conversion: Each line becomes a row."""
    lines = text.split("\n")
    df = pd.DataFrame(lines, columns=["Report"])
    return df


# -------------------------------------------------------
# Gemini API Execution
# -------------------------------------------------------
if generate:
    try:
        with st.spinner("Generating personalized family life plan..."):

            genai.configure(api_key="AIzaSyA_mrBIcoZ-6qBTbFVkxG5nOtCJjCe1lWI")
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(build_prompt())

            final_text = response.text

            st.success("Your life plan has been generated!")
            st.markdown("### 📘 Your AI-Generated Family Life Plan")
            st.markdown(final_text)

            # Convert text to DataFrame for CSV/XLSX
            df = text_to_dataframe(final_text)

            # PDF
            pdf_bytes = create_pdf(final_text)

            # CSV
            csv_bytes = df.to_csv(index=False).encode("utf-8")

            # Excel
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name="LifePlan")
            excel_bytes = excel_buffer.getvalue()

            # -------------------------------------------------------
            # DOWNLOAD BUTTONS
            # -------------------------------------------------------
            st.subheader("📥 Download Your Report")

            st.download_button(
                label="Download as PDF",
                data=pdf_bytes,
                file_name="family_life_plan.pdf",
                mime="application/pdf"
            )

            st.download_button(
                label="Download as CSV",
                data=csv_bytes,
                file_name="family_life_plan.csv",
                mime="text/csv"
            )

            st.download_button(
                label="Download as XLSX",
                data=excel_bytes,
                file_name="family_life_plan.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
