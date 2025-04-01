# Job Auto-Applier (No Email Alerts Version)
import streamlit as st
st.set_page_config(page_title="Job Auto-Applier", page_icon="💼", layout="wide")

from bs4 import BeautifulSoup
from transformers import pipeline
import docx2txt
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- Selenium Setup --------------------
@st.cache_resource
def get_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        st.warning("⚠️ ChromeDriver failed - using simulated results")
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

def generate_cover_letter(resume_text, job_title):
    generator = load_generator()
    prompt = f"Write a cover letter for {job_title} based on: {resume_text[:800]}"
    result = generator(prompt, max_length=300, do_sample=False)
    return result[0]['generated_text']

# -------------------- LinkedIn Scraper --------------------
def scrape_linkedin(keyword, location):
    try:
        driver = get_driver()
        if not driver:
            return get_simulated_results(keyword, location)
            
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return parse_job_listings(soup)
        
    except Exception as e:
        st.warning(f"Scraping failed: {str(e)}")
        return get_simulated_results(keyword, location)
    finally:
        if 'driver' in locals():
            driver.quit()

def parse_job_listings(soup):
    jobs = []
    listings = soup.find_all("li", class_="jobs-search-results__list-item")[:5]
    for job in listings:
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

def get_simulated_results(keyword, location):
    """Fallback with realistic-looking simulated data"""
    jobs = []
    templates = [
        ("Senior {keyword} Engineer", "TechCorp"),
        ("{keyword} Developer", "DataSystems"),
        ("Junior {keyword}", "StartUp Inc"),
        ("{keyword} Specialist", "DigitalSolutions"),
        ("Remote {keyword}", "GlobalTech")
    ]
    
    for title, company in templates:
        jobs.append({
            "Title": title.format(keyword=keyword),
            "Company": company,
            "Link": f"https://www.linkedin.com/jobs/search/?keywords={keyword}",
            "Platform": "LinkedIn"
        })
    return jobs

# -------------------- Streamlit UI --------------------
st.title("💼 Job Auto-Applier")
st.markdown("Find and apply to jobs automatically")

# User Input
resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
resume_text = parse_resume(resume_file) if resume_file else ""

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name")
with col2:
    location = st.text_input("Location", "Remote")

keyword = st.text_input("Job Title/Keywords", "Data Analyst")
generate_cl = st.checkbox("Generate Cover Letters", True)

if st.button("🔍 Find Jobs"):
    if not name or not resume_file:
        st.warning("Please enter your name and upload a resume")
    else:
        with st.spinner("Searching jobs..."):
            jobs = scrape_linkedin(keyword, location)
            
            if jobs:
                st.success(f"Found {len(jobs)} jobs")
                for i, job in enumerate(jobs):
                    with st.expander(f"{i+1}. {job['Title']} at {job['Company']}"):
                        st.markdown(f"[Apply on {job['Platform']}]({job['Link']})")
                        
                        if generate_cl and resume_text:
                            st.divider()
                            st.write("**Suggested Cover Letter:**")
                            st.write(generate_cover_letter(resume_text, job['Title']))
            else:
                st.warning("No jobs found. Try different keywords.")

st.markdown("---")
st.caption("© 2023 JobFinder Tool")
