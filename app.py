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

def scrape_internshala(keyword):
    try:
        url = f"https://internshala.com/internships/keywords-{keyword.replace(' ', '%20')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for card in soup.find_all("div", class_="individual_internship")[:10]:
            title = card.find("div", class_="heading_4_5 profile")
            company = card.find("a", class_="link_display_like_text")
            link_tag = card.find("a", class_="view_detail_button")
            link = "https://internshala.com" + link_tag['href'] if link_tag else ""
            if title and company:
                jobs.append({
                    "Title": title.get_text(strip=True),
                    "Company": company.get_text(strip=True),
                    "Link": link,
                    "Platform": "Internshala"
                })
        return jobs
    except:
        return []

def scrape_naukri(keyword, location):
    try:
        url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for card in soup.select(".jobTuple")[:10]:
            title = card.select_one("a.title")
            company = card.select_one("a.subTitle")
            if title and company:
                jobs.append({
                    "Title": title.get_text(strip=True),
                    "Company": company.get_text(strip=True),
                    "Link": title['href'],
                    "Platform": "Naukri"
                })
        return jobs
    except:
        return []

def scrape_indeed(keyword, location):
    try:
        url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for div in soup.find_all("a", class_="tapItem")[:10]:
            title = div.find("h2")
            company = div.find("span", class_="companyName")
            link = "https://www.indeed.com" + div.get("href") if div.get("href") else ""
            if title and company:
                jobs.append({
                    "Title": title.text.strip(),
                    "Company": company.text.strip(),
                    "Link": link,
                    "Platform": "Indeed"
                })
        return jobs
    except:
        return []

def scrape_timesjobs(keyword):
    try:
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={keyword.replace(' ', '%20')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        listings = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
        for job in listings[:10]:
            title = job.find("h2")
            company = job.find("h3", class_="joblist-comp-name")
            link = title.find("a")["href"] if title and title.find("a") else ""
            if title and company:
                jobs.append({
                    "Title": title.text.strip(),
                    "Company": company.text.strip(),
                    "Link": link,
                    "Platform": "TimesJobs"
                })
        return jobs
    except:
        return []

def scrape_linkedin(keyword, location):
    try:
        # Placeholder for future dynamic scraping logic
        jobs = []
        job_titles = [
            "Marketing Specialist (Junior / Mid-Level)",
            "Lead Generation Specialist (Remote)",
            "AI Business Development & Marketing Specialist",
            "Lead Generation Specialist",
            "Market Research Executive",
            "Telecaller (IT Sales & Marketing)"
        ]
        companies = [
            "InfobelPRO", "Job Helping Hand", "Synaptyx AI",
            "Supy", "Soul AI", "HashRoot"
        ]
        for i in range(len(job_titles)):
            jobs.append({
                "Title": job_titles[i],
                "Company": companies[i],
                "Link": f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote_plus(keyword)}&location={urllib.parse.quote_plus(location)}",
                "Platform": "LinkedIn (Manual)"
            })
        return jobs
    except:
        return []
    except:
        return []

# -------------------- Streamlit App --------------------
st.markdown("""
<style>
    .branding {
        background: linear-gradient(90deg, #2AB7CA 0%, #1A3550 100%);
        color: white;
        padding: 15px;
        border-radius: 0 0 12px 12px;
        text-align: center;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .branding a {
        color: white;
        text-decoration: none;
        margin: 0 8px;
    }
</style>
<div class="branding">
    © 2025 CareerUpskillers | 
    <a href="https://www.careerupskillers.com/about-1">Privacy</a> | 
    <a href="https://wa.me/917892116728">WhatsApp</a> | 
    <a href="https://www.youtube.com/@Careerupskillers">YouTube</a> | 
    <a href="https://www.facebook.com/share/18gUeR73H6/">Facebook</a> | 
    <a href="https://www.linkedin.com/company/careerupskillers/">LinkedIn</a> | 
    <a href="https://www.instagram.com/careerupskillers?igsh=YWNmOGMwejBrb24z">Instagram</a>
</div>
""", unsafe_allow_html=True)

st.title("💼 All-in-One Job Auto-Applier")
st.markdown("Apply smartly with AI-powered cover letters and resume autofill.")

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
        import json
        import urllib.parse
        google_sheets_url = st.secrets.get("GOOGLE_SHEETS_URL")
        try:
            if google_sheets_url:
                requests.post(google_sheets_url, json=lead_info)
            else:
                st.warning("Google Sheets URL not found in secrets. Data saved locally.")
                lead_df.to_csv("lead_data.csv", mode='a', header=not os.path.exists("lead_data.csv"), index=False)
        except Exception as e:
            st.warning(f"Google Sheets push failed. Saving locally. Error: {e}")
            lead_df.to_csv("lead_data.csv", mode='a', header=not os.path.exists("lead_data.csv"), index=False)
        st.success("✅ Employee details saved!")

        st.info("🔍 Searching jobs on all platforms...")
        platforms = ["LinkedIn", "TimesJobs", "Internshala", "Naukri", "Indeed"]
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
