# Multi-Platform Job Auto-Applier (ChromeDriver Fixed Version)
import streamlit as st
st.set_page_config(page_title="All-in-One Job Auto-Applier", page_icon="💼", layout="wide")

import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import docx2txt
import PyPDF2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- Selenium Setup --------------------
@st.cache_resource
def get_driver():
    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Set up ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        # Try to initialize ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    except Exception as e:
        st.warning(f"⚠️ ChromeDriver initialization failed: {str(e)}")
        st.warning("Falling back to simulated LinkedIn results")
        return None

# -------------------- Resume Parser --------------------
def parse_resume(file):
    text = ""
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)
    return text

# -------------------- AI Generator --------------------
@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="t5-small")

# -------------------- Cover Letter Generator --------------------
def generate_cover_letter(resume_text, job_title):
    generator = load_generator()
    prompt = f"Write a professional cover letter for a {job_title} job based on this resume: {resume_text[:800]}"
    result = generator(prompt, max_length=300, do_sample=False)
    return result[0]['generated_text']

# -------------------- LinkedIn Scraper --------------------
def scrape_linkedin(keyword, location):
    try:
        driver = get_driver()
        if driver is None:
            return fallback_linkedin_scrape(keyword, location)
            
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
        driver.get(url)
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )
        
        # Scroll to load more jobs
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        jobs = []
        
        for job in soup.find_all("li", class_="jobs-search-results__list-item")[:5]:
            title = job.find("a", class_="job-card-list__title")
            company = job.find("span", class_="job-card-container__primary-description")
            link = job.find("a", class_="job-card-list__title")
            
            if title and company and link:
                jobs.append({
                    "Title": title.text.strip(),
                    "Company": company.text.strip(),
                    "Link": link["href"].split("?")[0],
                    "Platform": "LinkedIn"
                })
        
        return jobs
    
    except Exception as e:
        st.warning(f"LinkedIn scraping error: {str(e)}")
        return fallback_linkedin_scrape(keyword, location)
    finally:
        try:
            if 'driver' in locals():
                driver.quit()
        except:
            pass

def fallback_linkedin_scrape(keyword, location):
    """Fallback when Selenium fails - provides simulated results"""
    jobs = []
    job_titles = [
        f"{keyword} Developer", 
        f"Senior {keyword}", 
        f"{keyword} Engineer",
        f"Junior {keyword}",
        f"{keyword} Specialist"
    ]
    companies = ["TechCorp", "DataSystems", "AI Ventures", "InnovateCo", "DigitalSolutions"]
    
    for i in range(min(5, len(job_titles))):
        jobs.append({
            "Title": job_titles[i],
            "Company": companies[i],
            "Link": f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}",
            "Platform": "LinkedIn"
        })
    return jobs

# -------------------- Streamlit UI --------------------
st.title("💼 All-in-One Job Auto-Applier")
st.markdown("Automatically apply to jobs across multiple platforms")

# Resume Upload
resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    resume_text = parse_resume(resume_file)
    st.success("✓ Resume Parsed")

# User Details
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name")
    email = st.text_input("Email")
with col2:
    phone = st.text_input("Phone")
    location = st.text_input("Location", "Remote")

keyword = st.text_input("Job Keywords", "Data Scientist")
auto_apply = st.checkbox("Enable Auto-Apply", False)
generate_cl = st.checkbox("Generate Cover Letters", True)

if st.button("🔍 Search Jobs"):
    if not all([name, email, resume_file]):
        st.warning("Please fill all required fields")
    else:
        with st.spinner("Searching LinkedIn jobs..."):
            results = scrape_linkedin(keyword, location)
            
            if email and results:
                try:
                    send_email_alert(email, len(results))
                except Exception as e:
                    st.warning(f"Could not send email: {str(e)}")

        if results:
            st.success(f"Found {len(results)} Jobs")
            for i, job in enumerate(results):
                with st.expander(f"{i+1}. {job['Title']} at {job['Company']}"):
                    st.markdown(f"**Platform:** {job['Platform']}")
                    st.markdown(f"[Apply Here]({job['Link']})")
                    
                    if generate_cl and resume_text:
                        st.divider()
                        st.write("**AI-Generated Cover Letter:**")
                        st.write(generate_cover_letter(resume_text, job['Title']))
                    
                    if auto_apply:
                        st.success("✓ Auto-Applied (Simulated)")
        else:
            st.warning("No jobs found. Try different keywords.")

# Footer
st.markdown("---")
st.markdown("© 2023 CareerUpskillers")
