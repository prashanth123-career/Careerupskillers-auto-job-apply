# Smart LinkedIn Job Finder with Resume & GPT
import streamlit as st
import re
import time
import urllib.parse
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
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- Page Setup --------------------
st.set_page_config(page_title="Smart Job Finder", page_icon="💼", layout="wide")
st.title("💼 Smart Job Finder Based on Your Resume")
st.markdown("Upload your resume and let AI match you with relevant LinkedIn jobs.")

# -------------------- Load Free GPT Model --------------------
@st.cache_resource
def load_gpt():
    return pipeline("text2text-generation", model="google/flan-t5-base")

# -------------------- Resume Reader --------------------
def parse_resume(file):
    try:
        if file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            return " ".join([page.extract_text() or "" for page in reader.pages])
        elif file.name.endswith(".docx"):
            return docx2txt.process(file)
    except:
        return ""
    return ""

# -------------------- Extract Details from Resume --------------------
def extract_resume_details(text, model):
    prompt = f"""From the resume below, extract:
1. Job Title or Designation
2. Key Skills
3. Short Job Description (max 30 words)

Resume:
{text[:1500]}
"""
    try:
        output = model(prompt, max_length=200, do_sample=False)
        return output[0]['generated_text']
    except:
        return "Could not extract details from resume."

# -------------------- LinkedIn Scraping --------------------
@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_linkedin_search_url(keyword, location, time_filter):
    base_url = "https://www.linkedin.com/jobs/search/"
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
    return f"{base_url}?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

def scrape_linkedin_jobs(keyword, location, time_filter):
    driver = get_driver()
    try:
        url = get_linkedin_search_url(keyword, location, time_filter)
        driver.get(url)
        time.sleep(3)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )

        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        return parse_job_listings(soup, keyword, time_filter, location)
    except Exception as e:
        st.warning(f"Error scraping jobs: {e}")
        return []
    finally:
        driver.quit()

def parse_job_listings(soup, keyword, time_filter, location):
    jobs = []
    listings = soup.find_all("li", class_="jobs-search__results-list-item")[:8]
    for job in listings:
        title = job.find("a", class_="job-card-list__title")
        company = job.find("h4", class_="job-card-container__company-name")
        time_posted = job.find("time", class_="job-search-card__listdate")

        if title:
            jobs.append({
                "Job Title": title.text.strip(),
                "Company": company.text.strip() if company else "N/A",
                "Posted": time_posted.text.strip() if time_posted else time_filter,
                "Apply Link": get_linkedin_search_url(keyword, location, time_filter)
            })
    return jobs

# -------------------- Streamlit UI --------------------
with st.form("job_form"):
    st.subheader("📄 Upload Your Resume")
    resume_file = st.file_uploader("Choose your resume file", type=["pdf", "docx"])

    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("🌍 Preferred Job Location", "Remote")
    with col2:
        time_filter = st.selectbox("🕒 Show Jobs Posted In", ["Past 24 hours", "Past week", "Past month", "Any time"], index=1)

    submitted = st.form_submit_button("🔍 Find Jobs")

# -------------------- After Submission --------------------
if submitted:
    if not resume_file:
        st.warning("Please upload a resume file.")
    else:
        with st.spinner("Reading your resume and preparing search..."):
            model = load_gpt()
            resume_text = parse_resume(resume_file)
            extracted = extract_resume_details(resume_text, model)

            st.success("📌 Resume Analyzed")
            st.markdown("#### 📊 Extracted Details from Resume")
            st.code(extracted)

            # Extract keywords from resume details
            keyword_match = re.findall(r'(?:Designation|Job Title):?\s*(.*)', extracted)
            search_keyword = keyword_match[0] if keyword_match else "Data Analyst"

            st.info(f"🔄 Fetching jobs based on: **{search_keyword.strip()}**")

        with st.spinner("Searching LinkedIn jobs..."):
            jobs = scrape_linkedin_jobs(search_keyword.strip(), location, time_filter)

        if jobs:
            st.success(f"✅ Found {len(jobs)} job listings")
            for i, job in enumerate(jobs):
                with st.expander(f"{i+1}. {job['Job Title']} at {job['Company']} ({job['Posted']})"):
                    st.markdown(f"[🔗 View & Apply on LinkedIn]({job['Apply Link']})")
        else:
            st.warning("No relevant jobs found. Try a different keyword or time filter.")

st.markdown("---")
st.caption("Powered by CareerUpskillers • AI Resume + LinkedIn Scraper")
