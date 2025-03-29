# Multi-Platform Job Auto-Applier (Modular Base Code)
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 🟢 Set page config — must be FIRST Streamlit command
st.set_page_config(page_title="All-in-One Job Auto-Applier", page_icon="💼")

# --- Safe Imports ---
try:
    from utils.scrapers import scrape_internshala, scrape_indeed, scrape_naukri, scrape_timesjobs
except ImportError:
    st.error("⚠️ Scraper module missing or incorrectly named. Please check `utils/scrapers.py`.")

try:
    from utils.cover_letter import generate_cover_letter
except ImportError:
    st.error("⚠️ Cover letter generator module missing or has import errors.")

try:
    from utils.resume_parser import parse_resume
except ImportError:
    st.error("⚠️ Resume parser module missing or has import errors.")

# -------------------- UI SETUP --------------------
st.title("💼 All-in-One Job Auto-Applier")
st.markdown("Apply smartly with AI-powered cover letters and resume autofill.")

# -------------------- Upload Resume --------------------
st.subheader("📄 Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    resume_text = parse_resume(resume_file)
    st.success("Resume uploaded and parsed successfully!")

# -------------------- Select Platforms --------------------
st.subheader("🌍 Select Platforms")
platforms = st.multiselect("Choose platforms to search:", ["Internshala", "Naukri", "Indeed", "TimesJobs", "LinkedIn"], default=["Internshala"])

# -------------------- Job Search Filters --------------------
st.subheader("🔍 Search Filters")
keyword = st.text_input("Job Title / Keywords", value="Data Science")
location = st.text_input("Location", value="Remote")
use_gpt = st.checkbox("Generate AI-based Cover Letter", value=True)
mode = st.radio("Application Mode", ["Manual Click", "Auto Apply (where possible)"])

if st.button("Search Jobs") and keyword and platforms:
    st.info("Searching jobs on selected platforms...")
    results = []
    for platform in platforms:
        if platform == "Internshala":
            results += scrape_internshala(keyword)
        elif platform == "Naukri":
            results += scrape_naukri(keyword, location)
        elif platform == "Indeed":
            results += scrape_indeed(keyword, location)
        elif platform == "TimesJobs":
            results += scrape_timesjobs(keyword, location)
        elif platform == "LinkedIn":
            st.warning("LinkedIn supports only manual click mode. Showing jobs only.")

    if results:
        st.success(f"Found {len(results)} jobs across platforms.")
        log = []
        for job in results:
            st.markdown("---")
            st.markdown(f"### 🏢 {job['Title']} at {job['Company']}")
            st.markdown(f"🌐 Platform: {job['Platform']}")
            st.markdown(f"🔗 [View Job]({job['Link']})")
            if use_gpt and resume_text:
                with st.expander("🧠 View AI-Generated Cover Letter"):
                    try:
                        st.write(generate_cover_letter(resume_text, job['Title']))
                    except:
                        st.error("⚠️ Failed to generate cover letter. Model may not have loaded.")
            if mode == "Auto Apply (where possible)":
                st.button(f"🚀 Auto Apply (Coming Soon)", key=job['Link'])
            else:
                st.markdown(f"[🖱️ Click to Apply]({job['Link']})")
            log.append({"Title": job['Title'], "Company": job['Company'], "Platform": job['Platform'], "Link": job['Link'], "Time": datetime.now()})
        df = pd.DataFrame(log)
        df.to_csv("applied_jobs_log.csv", index=False)
        st.success("Log saved as applied_jobs_log.csv")
    else:
        st.warning("No jobs found. Try different filters.")
