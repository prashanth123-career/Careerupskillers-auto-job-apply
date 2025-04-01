import streamlit as st
import openai
import re
import PyPDF2
import docx2txt
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="AI Job Finder", page_icon="💼")

# ---------- Setup OpenAI API ----------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------- Resume Reader ----------
def parse_resume(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    return ""

# ---------- OpenAI Cover Letter Generator ----------
def generate_cover_letter_openai(designation, experience, company, skills, job_title):
    prompt = f"""
Write a professional and concise cover letter for the position of {job_title}.
Candidate Details:
- Designation: {designation}
- Experience: {experience} years
- Previous Company: {company}
- Key Skills: {skills}
- The tone should be formal and achievement-driven.
"""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=300
    )
    return res.choices[0].message.content.strip()

# ---------- LinkedIn Smart URL Generator ----------
def get_linkedin_url(keyword, location, time_filter):
    base = "https://www.linkedin.com/jobs/search/"
    time_map = {
        "Past 24 hours": "r86400",
        "Past week": "r604800",
        "Past month": "r2592000",
        "Any time": ""
    }
    params = {
        "keywords": keyword,
        "location": location if location.lower() != "remote" else "",
        "f_TPR": time_map.get(time_filter, "")
    }
    return f"{base}?{urllib.parse.urlencode({k:v for k,v in params.items() if v})}"

# ---------- UI ----------
st.title("✨ AI Cover Letter & Job Finder")
st.markdown("🚀 Generate custom cover letters and find jobs on LinkedIn.")

with st.form("job_form"):
    designation = st.text_input("Your Designation", "AI Engineer")
    skills = st.text_input("Your Key Skills", "Python, NLP, LLMs")
    experience = st.number_input("Years of Experience", 0.0, 30.0, 2.5, step=0.1)
    company = st.text_input("Previous Company", "TechCorp")
    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

    st.divider()

    keyword = st.text_input("Job Title or Keyword", "Data Scientist")
    location = st.text_input("Preferred Location", "Remote")
    time_filter = st.selectbox("Time Filter", ["Past 24 hours", "Past week", "Past month", "Any time"])

    generate_cl = st.checkbox("Generate AI Cover Letter", value=True)
    submit = st.form_submit_button("🔍 Find Jobs")

if submit:
    if not resume_file or not designation or not skills or not company:
        st.warning("❌ Please fill all fields and upload your resume.")
    else:
        with st.spinner("📄 Parsing resume and preparing search..."):
            resume_text = parse_resume(resume_file)
            linkedin_url = get_linkedin_url(keyword, location, time_filter)

        st.success("✅ Ready! Here's your search link and optional cover letter:")
        st.markdown(f"🔗 [View LinkedIn Jobs for '{keyword}']({linkedin_url})")

        if generate_cl:
            with st.spinner("🧠 Generating AI Cover Letter..."):
                cover = generate_cover_letter_openai(designation, experience, company, skills, keyword)
                st.text_area("📩 AI-Generated Cover Letter", value=cover, height=300)
