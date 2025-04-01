import streamlit as st
import urllib.parse
from datetime import datetime
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

# -------------------- Setup --------------------
st.set_page_config(page_title="Job Auto-Applier", page_icon="💼", layout="wide")

# -------------------- Selenium Setup --------------------
@st.cache_resource
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

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

# -------------------- AI Cover Letter --------------------
@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="google/flan-t5-base")

generator = load_generator()

def generate_cover_letter(resume_text, job_title):
    prompt = f"Write a professional cover letter for a {job_title} position based on this resume: {resume_text[:800]}"
    result = generator(prompt, max_length=400, do_sample=False)
    return result[0]['generated_text']

# -------------------- LinkedIn Scraper --------------------
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
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return f"{base}?{query}"

def scrape_linkedin(keyword, location, time_filter, experience):
    driver = get_driver()
    url = get_linkedin_url(keyword, location, time_filter)
    driver.get(url)
    time.sleep(3)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
    )

    for _ in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    listings = soup.find_all("li", class_="jobs-search__results-list-item")[:10]
    jobs = []
    for job in listings:
        title_tag = job.find("a", class_="job-card-list__title")
        time_posted = job.find("time", class_="job-search-card__listdate")
        if title_tag:
            job_title = title_tag.text.strip()
            # Skip intern roles for experienced candidates
            if experience >= 2 and "intern" in job_title.lower():
                continue
            jobs.append({
                "Title": job_title,
                "Time Posted": time_posted.text.strip() if time_posted else time_filter,
                "Link": get_linkedin_url(keyword, location, time_filter),
                "Platform": "LinkedIn"
            })
    return jobs

# -------------------- Streamlit UI --------------------
st.title("💼 Smart Job Finder with Time Filters")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        designation = st.text_input("Your Designation", "AI Engineer")
        skills = st.text_input("Skills (comma-separated)", "Python, ML, NLP")
        experience = st.number_input("Years of Experience", 0.0, 30.0, 1.0, step=0.1)
    with col2:
        keyword = st.text_input("Job Title or Keyword", "Data Scientist")
        location = st.text_input("Preferred Location", "Remote")
        resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    
    time_filter = st.selectbox("Filter jobs by time posted", ["Past 24 hours", "Past week", "Past month", "Any time"])
    use_gpt = st.checkbox("Generate AI Cover Letter", value=True)

    submitted = st.form_submit_button("🔍 Search Jobs")

if submitted:
    if not designation or not resume_file or not keyword:
        st.warning("Please complete all required fields.")
    else:
        with st.spinner(f"Fetching LinkedIn jobs from {time_filter.lower()}..."):
            resume_text = parse_resume(resume_file)
            jobs = scrape_linkedin(keyword, location, time_filter, experience)

        if jobs:
            st.success(f"✅ Found {len(jobs)} relevant jobs")
            for i, job in enumerate(jobs):
                st.markdown(f"### {i+1}. {job['Title']} ({job['Platform']})")
                st.markdown(f"📅 Posted: {job['Time Posted']}")
                st.markdown(f"[🔗 View & Apply]({job['Link']})")
                if use_gpt:
                    with st.expander("📝 View AI-Generated Cover Letter"):
                        st.write(generate_cover_letter(resume_text, job['Title']))
        else:
            st.error("❌ No relevant jobs found. Try changing filters or keywords.")
