# Smart Resume-Based Job Finder
import streamlit as st
import re
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
import time
import urllib.parse

# -------------------- Setup --------------------
st.set_page_config(page_title="Resume Job Matcher", page_icon="🔍", layout="wide")

# -------------------- Resume Analyzer --------------------
def extract_skills(resume_text):
    """Extract skills from resume text"""
    skills = []
    # Common tech skills pattern
    tech_skills = re.findall(r'\b(?:Python|Java|SQL|JavaScript|React|AWS|Machine Learning|Data Analysis)\b', resume_text, re.IGNORECASE)
    # Extract job titles mentioned
    titles = re.findall(r'\b(?:Engineer|Developer|Analyst|Specialist|Manager|Designer)\b', resume_text, re.IGNORECASE)
    return list(set(tech_skills + titles))

def suggest_job_titles(skills):
    """Generate relevant job titles based on skills"""
    mapping = {
        'Python': ['Python Developer', 'Data Engineer'],
        'Java': ['Java Developer', 'Backend Engineer'],
        'SQL': ['Data Analyst', 'Database Administrator'],
        'JavaScript': ['Frontend Developer', 'Full Stack Engineer'],
        'React': ['React Developer', 'UI Engineer'],
        'AWS': ['Cloud Engineer', 'DevOps Specialist'],
        'Machine Learning': ['ML Engineer', 'Data Scientist'],
        'Data Analysis': ['Business Analyst', 'Data Analyst']
    }
    titles = []
    for skill in skills:
        titles.extend(mapping.get(skill, []))
    return list(set(titles))[:5]  # Return top 5 unique titles

# -------------------- Selenium Setup --------------------
@st.cache_resource
def get_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    except:
        return None

# -------------------- Job Scraper --------------------
def get_search_url(job_title, location):
    """Generate LinkedIn search URL"""
    params = {
        "keywords": job_title,
        "location": location if location.lower() != "remote" else ""
    }
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return f"https://www.linkedin.com/jobs/search/?{query}"

def scrape_jobs(job_title, location):
    driver = get_driver()
    if not driver:
        return []  # Return empty if no driver
    
    try:
        url = get_search_url(job_title, location)
        driver.get(url)
        time.sleep(3)  # Let page load
        
        # Extract job count
        try:
            count_element = driver.find_element(By.CLASS_NAME, "results-context-header__job-count")
            job_count = count_element.text
        except:
            job_count = "multiple"
        
        return {
            "title": job_title,
            "count": job_count,
            "url": url
        }
    finally:
        if driver:
            driver.quit()

# -------------------- Streamlit UI --------------------
def main():
    st.title("🔍 Smart Resume Job Matcher")
    st.markdown("Upload your resume to find matching job opportunities")
    
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    location = st.text_input("Preferred Location", "Remote")
    
    if st.button("Find Matching Jobs") and resume_file:
        with st.spinner("Analyzing your resume..."):
            # Parse resume
            text = ""
            if resume_file.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(resume_file)
                text = " ".join([page.extract_text() or "" for page in reader.pages])
            else:
                text = docx2txt.process(resume_file)
            
            # Extract skills and suggest jobs
            skills = extract_skills(text)
            suggested_jobs = suggest_job_titles(skills)
            
            if not suggested_jobs:
                st.warning("Couldn't identify relevant skills in your resume")
                return
            
            st.success(f"Based on your resume, we recommend searching for these positions:")
            
            # Display job matches
            for job in suggested_jobs:
                with st.expander(f"🧑‍💻 {job}"):
                    result = scrape_jobs(job, location)
                    if result:
                        st.markdown(f"**{result['count']} jobs found**")
                        st.markdown(f"[🔍 Search {job} positions on LinkedIn]({result['url']})")
                    else:
                        st.markdown(f"[🔍 Search {job} positions on LinkedIn]({get_search_url(job, location)})")
            
            # Show extracted skills
            st.divider()
            st.subheader("Skills Identified in Your Resume")
            cols = st.columns(4)
            for i, skill in enumerate(skills):
                cols[i%4].success(f"• {skill}")

if __name__ == "__main__":
    main()
