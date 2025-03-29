# Multi-Platform Job Auto-Applier with Lead Capture (Improved Validation)

import streamlit as st
st.set_page_config(page_title="All-in-One Job Auto-Applier", page_icon="💼")

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline
import docx2txt
import PyPDF2
import os
import re

# -------------------- Resume Parser --------------------
def parse_resume(file):
    text = ""
    ext = file.name.split(".")[-1]
    if ext == "pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif ext == "docx":
        text = docx2txt.process(file)
    return text

# -------------------- Cover Letter Generator --------------------
@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="google/flan-t5-base")

generator = load_generator()

def generate_cover_letter(resume_text, job_title):
    prompt = f"Write a short and professional cover letter for a {job_title} job based on this resume: {resume_text[:800]}"
    result = generator(prompt, max_length=200, do_sample=False)
    return result[0]['generated_text']

# -------------------- Job Platform Scrapers --------------------
# (Internshala, Naukri, Indeed, TimesJobs, LinkedIn same as before...)

# -------------------- Streamlit App --------------------
st.title("💼 All-in-One Job Auto-Applier + Lead Scraper")
st.markdown("Apply smartly with AI-powered cover letters and collect employee details for job opportunities.")

st.subheader("📄 Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    resume_text = parse_resume(resume_file)
    st.success("Resume uploaded and parsed successfully!")

st.subheader("👤 Employee Details")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
current_location = st.text_input("Current Location (City, Country)")
interested_location = st.text_input("Preferred Location for Jobs")
experience = st.slider("Years of Experience", 0, 30, 1)
current_salary = st.text_input("Current Salary (Optional)")
expected_salary = st.text_input("Expected Salary")

st.subheader("🔍 Job Search Filters")
keyword = st.text_input("Job Title / Keywords", value="Data Science")
location = st.text_input("Search Location", value="Remote")
use_gpt = st.checkbox("Generate AI-based Cover Letter", value=True)
mode = st.radio("Application Mode", ["Manual Click", "Auto Apply (coming soon)"])

email_valid = re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
phone_valid = re.match(r"^\+?[0-9\-\s]{8,15}$", phone)

if st.button("Search Jobs"):
    if not name.strip():
        st.error("❌ Please enter your full name.")
    elif not email_valid:
        st.error("❌ Please enter a valid email address.")
    elif not phone_valid:
        st.error("❌ Please enter a valid phone number (8–15 digits, can include country code).")
    elif not current_location.strip():
        st.error("❌ Please enter your current location.")
    elif not interested_location.strip():
        st.error("❌ Please enter your preferred job location.")
    elif not expected_salary.strip():
        st.error("❌ Please enter your expected salary.")
    elif not resume_file:
        st.error("❌ Please upload your resume.")
    else:
        lead_info = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Current Location": current_location,
            "Interested Location": interested_location,
            "Experience": experience,
            "Current Salary": current_salary,
            "Expected Salary": expected_salary,
            "Resume Uploaded": bool(resume_file),
            "Time": datetime.now()
        }
        lead_df = pd.DataFrame([lead_info])
        lead_df.to_csv("lead_data.csv", mode='a', header=not os.path.exists("lead_data.csv"), index=False)
        st.success("✅ Employee details saved!")

        st.info("🔍 Searching jobs on all platforms...")
        platforms = ["Internshala", "Naukri", "Indeed", "TimesJobs", "LinkedIn"]
        results = []
        for platform in platforms:
            st.write(f"Searching {platform}...")
            if platform == "Internshala":
                jobs = scrape_internshala(keyword)
            elif platform == "Naukri":
                jobs = scrape_naukri(keyword, location)
            elif platform == "Indeed":
                jobs = scrape_indeed(keyword, location)
            elif platform == "TimesJobs":
                jobs = scrape_timesjobs(keyword)
            elif platform == "LinkedIn":
                jobs = scrape_linkedin(keyword, location)
            else:
                jobs = []
            if jobs:
                results.extend(jobs)
            else:
                st.warning(f"⚠️ No jobs found on {platform}.")

        if results:
            st.success(f"✅ Found {len(results)} jobs across all platforms.")
            log = []
            for job in results:
                st.markdown("---")
                st.markdown(f"### 🏢 {job['Title']} at {job['Company']}")
                st.markdown(f"🌐 Platform: {job['Platform']}")
                st.markdown(f"🔗 [View Job]({job['Link']})")
                if use_gpt and resume_text:
                    with st.expander("🧠 View AI-Generated Cover Letter"):
                        st.write(generate_cover_letter(resume_text, job['Title']))
                if mode == "Auto Apply (coming soon)":
                    st.button(f"🚀 Auto Apply (Disabled)", key=job['Link'])
                else:
                    st.markdown(f"[🖱️ Click to Apply]({job['Link']})")
                log.append({
                    "Title": job['Title'],
                    "Company": job['Company'],
                    "Platform": job['Platform'],
                    "Link": job['Link'],
                    "Experience": experience,
                    "Expected Salary": expected_salary,
                    "Time": datetime.now()
                })
            df = pd.DataFrame(log)
            df.to_csv("applied_jobs_log.csv", index=False)
            st.success("📁 Log saved as applied_jobs_log.csv")
        else:
            st.error("❌ No jobs found on any platform. Try different filters.")
