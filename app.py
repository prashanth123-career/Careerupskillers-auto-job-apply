# Multi-Platform Job Auto-Applier (Now with Naukri, Internshala, Indeed, TimesJobs, LinkedIn)

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

# -------------------- Internshala Scraper --------------------
def scrape_internshala(keyword):
    url = f"https://internshala.com/internships/keywords-{keyword.replace(' ', '%20')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = []
    for card in soup.find_all("div", class_="individual_internship")[:10]:
        title = card.find("a", class_="view_detail_button")
        link = "https://internshala.com" + title["href"] if title else ""
        role = card.find("div", class_="heading_4_5 profile")
        company = card.find("a", class_="link_display_like_text")
        jobs.append({
            "Title": role.text.strip() if role else "",
            "Company": company.text.strip() if company else "",
            "Link": link,
            "Platform": "Internshala"
        })
    return jobs

# -------------------- Naukri Scraper (Cloud-Safe Fallback) --------------------
def scrape_naukri(keyword, location):
    url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')})"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for card in soup.select(".jobTuple")[:10]:
            title = card.select_one("a.title")
            company = card.select_one("a.subTitle")
            if title and company:
                jobs.append({
                    "Title": title.text.strip(),
                    "Company": company.text.strip(),
                    "Link": title['href'],
                    "Platform": "Naukri (Cloud Safe)"
                })
        return jobs
    except Exception as e:
        st.warning("Naukri scraping failed on cloud. Try again or run locally for full features.")
        return []

# -------------------- Indeed Scraper (Basic Cloud-Safe) --------------------
def scrape_indeed(keyword, location):
    url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
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

# -------------------- TimesJobs Scraper (Basic Cloud-Safe) --------------------
def scrape_timesjobs(keyword):
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={keyword.replace(' ', '%20')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
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

# -------------------- LinkedIn Scraper (Manual Apply Only) --------------------
def scrape_linkedin(keyword, location):
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
    jobs = []
    for i in range(1, 11):
        jobs.append({
            "Title": f"LinkedIn Job {i} - {keyword}",
            "Company": "Confidential",
            "Link": url,
            "Platform": "LinkedIn (Manual)"
        })
    return jobs

# -------------------- Streamlit App --------------------
st.title("💼 All-in-One Job Auto-Applier")
st.markdown("Apply smartly with AI-powered cover letters and resume autofill.")

st.subheader("📄 Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    resume_text = parse_resume(resume_file)
    st.success("Resume uploaded and parsed successfully!")

st.subheader("🌍 Select Platforms")
platforms = st.multiselect("Choose platforms to search:", ["Internshala", "Naukri", "Indeed", "TimesJobs", "LinkedIn"], default=["Internshala"])

st.subheader("🔍 Search Filters")
keyword = st.text_input("Job Title / Keywords", value="Data Science")
location = st.text_input("Location", value="Remote")
experience = st.slider("Years of Experience (Optional)", 0, 20, 1)
salary = st.text_input("Minimum Salary (Optional)", value="")
use_gpt = st.checkbox("Generate AI-based Cover Letter", value=True)
mode = st.radio("Application Mode", ["Manual Click", "Auto Apply (coming soon)"])

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
            results += scrape_timesjobs(keyword)
        elif platform == "LinkedIn":
            results += scrape_linkedin(keyword, location)

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
                "Salary": salary,
                "Time": datetime.now()
            })
        df = pd.DataFrame(log)
        df.to_csv("applied_jobs_log.csv", index=False)
        st.success("Log saved as applied_jobs_log.csv")
    else:
        st.warning("No jobs found. Try different filters.")
