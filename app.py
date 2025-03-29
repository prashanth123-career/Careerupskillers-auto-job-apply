# Multi-Platform Job Auto-Applier (Now with Naukri Integration)

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline
import docx2txt
import PyPDF2
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

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

# -------------------- Naukri Scraper --------------------
def scrape_naukri(keyword, location):
    path_keyword = keyword.strip().replace(' ', '-')
    path_location = location.strip().replace(' ', '-')
    query_keyword = keyword.strip().replace(' ', '%20')
    query_location = location.strip().replace(' ', '%20')
    url = f"https://www.naukri.com/{path_keyword}-jobs-in-{path_location}?k={query_keyword}&l={query_location}"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    jobs = []
    results_div = soup.find('div', class_='list')
    if not results_div:
        return jobs
    job_cards = results_div.find_all('article', class_='jobTuple')
    for card in job_cards[:10]:
        title_tag = card.find('a', class_='title')
        company_tag = card.find('a', class_='subTitle')
        if title_tag and company_tag:
            jobs.append({
                "Title": title_tag.get_text(strip=True),
                "Company": company_tag.get_text(strip=True),
                "Link": title_tag['href'],
                "Platform": "Naukri"
            })
    return jobs

# -------------------- Streamlit App --------------------
st.set_page_config(page_title="All-in-One Job Auto-Applier", page_icon="💼")
st.title("💼 All-in-One Job Auto-Applier")
st.markdown("Apply smartly with AI-powered cover letters and resume autofill.")

st.subheader("📄 Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    resume_text = parse_resume(resume_file)
    st.success("Resume uploaded and parsed successfully!")

st.subheader("🌍 Select Platforms")
platforms = st.multiselect("Choose platforms to search:", ["Internshala", "Naukri"], default=["Internshala"])

st.subheader("🔍 Search Filters")
keyword = st.text_input("Job Title / Keywords", value="Data Science")
location = st.text_input("Location", value="Remote")
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
            log.append({"Title": job['Title'], "Company": job['Company'], "Platform": job['Platform'], "Link": job['Link'], "Time": datetime.now()})
        df = pd.DataFrame(log)
        df.to_csv("applied_jobs_log.csv", index=False)
        st.success("Log saved as applied_jobs_log.csv")
    else:
        st.warning("No jobs found. Try different filters.")
