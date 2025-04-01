import streamlit as st
st.set_page_config(page_title="All-in-One Job Auto-Applier", page_icon="💼")

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline
import docx2txt
import PyPDF2
import re

# -------------------- Resume Parser --------------------
def parse_resume(file):
    text = ""
    ext = file.name.split(".")[-1].lower()
    if ext == "pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
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
def scrape_monster(keyword, location):
    try:
        url = f"https://www.monsterindia.com/srp/results?query={keyword.replace(' ', '%20')}&locations={location.replace(' ', '%20')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for div in soup.find_all("div", class_="card-apply-content")[:10]:
            title = div.find("h3")
            company = div.find("span", class_="company-name")
            link = title.find("a")['href'] if title and title.find("a") else ""
            if title and company:
                jobs.append({"Title": title.text.strip(), "Company": company.text.strip(), "Link": link, "Platform": "Monster"})
        return jobs
    except:
        return []

def scrape_angellist(keyword, location):
    try:
        jobs = []
        titles = ["Startup Data Analyst", "AI Research Intern", "Remote ML Developer"]
        companies = ["AngelTech", "GrowStart", "InnovateAI"]
        import urllib.parse
        for i in range(min(len(titles), len(companies))):
            jobs.append({
                "Title": titles[i],
                "Company": companies[i],
                "Link": f"https://angel.co/jobs?query={urllib.parse.quote_plus(keyword)}",
                "Platform": "AngelList (Manual)"
            })
        return jobs
    except:
        return []

def scrape_internshala(keyword):
    try:
        url = f"https://internshala.com/internships/keywords-{keyword.replace(' ', '%20')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for card in soup.find_all("div", class_="individual_internship")[:10]:
            title = card.find("div", class_="heading_4_5 profile")
            company = card.find("a", class_="link_display_like_text")
            link_tag = card.find("a", class_="view_detail_button")
            link = "https://internshala.com" + link_tag['href'] if link_tag else ""
            if title and company:
                jobs.append({"Title": title.get_text(strip=True), "Company": company.text.strip(), "Link": link, "Platform": "Internshala"})
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
                jobs.append({"Title": title.get_text(strip=True), "Company": company.text.strip(), "Link": title['href'], "Platform": "Naukri"})
        return jobs
    except:
        return []

def scrape_indeed(keyword, location):
    try:
        url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for div in soup.find_all("a", class_="tapItem")[:10]:
            title = div.find("h2")
            company = div.find("span", class_="companyName")
            link = "https://www.indeed.com" + div.get("href") if div.get("href") else ""
            if title and company:
                jobs.append({"Title": title.text.strip(), "Company": company.text.strip(), "Link": link, "Platform": "Indeed"})
        return jobs
    except:
        return []

def scrape_timesjobs(keyword):
    try:
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={keyword.replace(' ', '%20')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for job in soup.find_all("li", class_="clearfix job-bx wht-shd-bx")[:10]:
            title = job.find("h2")
            company = job.find("h3", class_="joblist-comp-name")
            link = title.find("a")["href"] if title and title.find("a") else ""
            if title and company:
                jobs.append({"Title": title.text.strip(), "Company": company.text.strip(), "Link": link, "Platform": "TimesJobs"})
        return jobs
    except:
        return []

def scrape_linkedin(keyword, location):
    try:
        jobs = []
        job_titles = ["Marketing Specialist", "Lead Generation Specialist", "AI Business Development"]
        companies = ["InfobelPRO", "Job Helping Hand", "Synaptyx AI"]
        import urllib.parse
        for i in range(min(len(job_titles), len(companies))):
            jobs.append({
                "Title": job_titles[i],
                "Company": companies[i],
                "Link": f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote_plus(keyword)}&location={urllib.parse.quote_plus(location)}",
                "Platform": "LinkedIn (Manual)"
            })
        return jobs
    except:
        return []

# -------------------- Streamlit App --------------------
st.markdown("""
<style>
    .branding {background: linear-gradient(90deg, #2AB7CA 0%, #1A3550 100%); color: white; padding: 15px; border-radius: 0 0 12px 12px; text-align: center; font-size: 14px; margin-bottom: 10px;}
    .branding a {color: white; text-decoration: none; margin: 0 8px;}
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

st.subheader("👤 Candidate Details")
designation = st.text_input("Your Designation (e.g., Data Analyst)")
target_role = st.text_input("Target Role (e.g., ML Engineer)")
skills = st.text_input("Your Skills (comma-separated)")
experience = st.number_input("Years of Experience", min_value=0.0, max_value=30.0, step=0.1, format="%.1f")

st.subheader("🌍 Job Location Preferences")
current_location = st.text_input("Current Location (City, Country)")
interested_location = st.text_input("Preferred Location for Jobs")
current_salary = st.text_input("Current Salary (Optional)")
expected_salary = st.text_input("Expected Salary")

st.subheader("🔍 Job Search Filters")
keyword = st.text_input("Job Title / Keywords", value="Data Science")
location = st.text_input("Search Location", value="Remote")
use_gpt = st.checkbox("Generate AI-based Cover Letter", value=True)
mode = st.radio("Application Mode", ["Manual Click", "Auto Apply (coming soon)"])

if st.button("Search Jobs"):
    if not designation or not target_role or not skills or not current_location or not interested_location or not expected_salary or not resume_file:
        st.error("❌ Please fill in all required fields.")
    else:
        with st.spinner("Searching for jobs..."):
            results = []
            results.extend(scrape_monster(keyword, location))
            results.extend(scrape_angellist(keyword, location))
            results.extend(scrape_internshala(keyword))
            results.extend(scrape_naukri(keyword, location))
            results.extend(scrape_indeed(keyword, location))
            results.extend(scrape_timesjobs(keyword))
            results.extend(scrape_linkedin(keyword, location))

        if results:
            st.subheader("📋 Job Results")
            log = []
            for i, job in enumerate(results):
                st.write(f"**{i+1}. {job['Title']}** at {job['Company']} ({job['Platform']})")
                if use_gpt:
                    cover_letter = generate_cover_letter(resume_text, job['Title'])
                    with st.expander("View AI-Generated Cover Letter"):
                        st.text(cover_letter)
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
