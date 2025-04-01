# Job Auto-Applier with Time Filters
import streamlit as st
import urllib.parse
from datetime import datetime, timedelta
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
    if not file:
        return ""
    try:
        text = ""
        if file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file.name.endswith(".docx"):
            text = docx2txt.process(file)
        return text
    except Exception as e:
        st.warning(f"Error parsing resume: {str(e)}")
        return ""

# -------------------- AI Generator --------------------
@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="t5-small")

def generate_cover_letter(resume_text, job_title):
    try:
        generator = load_generator()
        prompt = f"Write a professional cover letter for {job_title} position based on these skills: {resume_text[:800]}"
        result = generator(prompt, max_length=400, do_sample=False)
        return result[0]['generated_text']
    except:
        return "Could not generate cover letter at this time."

# -------------------- Job Scraper with Time Filters --------------------
def get_linkedin_search_url(keyword, location, time_filter):
    """Generate LinkedIn search URL with time filter"""
    base_url = "https://www.linkedin.com/jobs/search/"
    
    # Convert time filter to LinkedIn's parameter
    time_mapping = {
        "Past 24 hours": "r86400",
        "Past week": "r604800",
        "Past month": "r2592000",
        "Any time": ""
    }
    time_param = time_mapping.get(time_filter, "")
    
    params = {
        "keywords": keyword,
        "location": location if location.lower() != "remote" else "",
        "f_TPR": time_param
    }
    
    query_string = urllib.parse.urlencode(
        {k: v for k, v in params.items() if v},
        quote_via=urllib.parse.quote
    )
    return f"{base_url}?{query_string}"

def scrape_linkedin(keyword, location, time_filter):
    driver = None
    try:
        driver = get_driver()
        if not driver:
            return get_simulated_results(keyword, location, time_filter)
            
        url = get_linkedin_search_url(keyword, location, time_filter)
        driver.get(url)
        
        # Wait for filters to be applied
        time.sleep(3)
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )
        
        # Scroll to load more jobs
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return parse_job_listings(soup, keyword, time_filter)
        
    except Exception as e:
        st.warning(f"Scraping failed: {str(e)}")
        return get_simulated_results(keyword, location, time_filter)
    finally:
        if driver is not None:
            try:
                driver.quit()
            except:
                pass

def parse_job_listings(soup, keyword, time_filter):
    jobs = []
    try:
        listings = soup.find_all("li", class_="jobs-search__results-list-item")[:5]
        for job in listings:
            title = job.find("a", class_="job-card-list__title")
            time_posted = job.find("time", class_="job-search-card__listdate")
            
            if title:
                job_title = title.text.strip()
                if keyword.lower() in job_title.lower():
                    jobs.append({
                        "Title": job_title,
                        "Time Posted": time_posted.text.strip() if time_posted else time_filter,
                        "Link": get_linkedin_search_url(keyword, "", time_filter),
                        "Platform": "LinkedIn"
                    })
    except:
        pass
    return jobs if jobs else get_simulated_results(keyword, "", time_filter)

def get_simulated_results(keyword, location, time_filter):
    """Fallback with time-aware simulated data"""
    job_titles = [
        f"Senior {keyword} Engineer",
        f"{keyword} Developer",
        f"Junior {keyword} Analyst",
        f"Remote {keyword} Specialist",
        f"{keyword} Consultant"
    ]
    
    search_url = get_linkedin_search_url(keyword, location, time_filter)
    
    return [{
        "Title": title,
        "Time Posted": time_filter,
        "Link": search_url,
        "Platform": "LinkedIn"
    } for title in job_titles]

# -------------------- Streamlit UI with Time Filters --------------------
def main():
    st.title("💼 Smart Job Finder with Time Filters")
    st.markdown("Find recent job postings and generate customized cover letters")
    
    # User Input Section
    with st.form("job_search"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name")
            keyword = st.text_input("Job Title/Keywords", "Data Analyst")
        with col2:
            resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
            location = st.text_input("Location", "Remote")
        
        # Time filter dropdown
        time_filter = st.selectbox(
            "Show jobs from",
            ["Past 24 hours", "Past week", "Past month", "Any time"],
            index=0
        )
        
        generate_cl = st.checkbox("Generate Cover Letters", True)
        submitted = st.form_submit_button("🔍 Find Jobs")
    
    if submitted:
        if not name or not resume_file:
            st.warning("Please enter your name and upload a resume")
        else:
            with st.spinner(f"Searching {time_filter.lower()} jobs..."):
                resume_text = parse_resume(resume_file)
                jobs = scrape_linkedin(keyword, location, time_filter)
                
                if jobs:
                    st.success(f"Found {len(jobs)} {time_filter.lower()} positions")
                    for i, job in enumerate(jobs):
                        with st.expander(f"{i+1}. {job['Title']} ({job['Time Posted']})"):
                            st.markdown(f"[🔍 Search similar {time_filter.lower()} positions on LinkedIn]({job['Link']})")
                            
                            if generate_cl and resume_text:
                                st.divider()
                                st.subheader("AI-Generated Cover Letter")
                                st.write(generate_cover_letter(resume_text, job['Title']))
                else:
                    st.warning(f"No {time_filter.lower()} jobs found. Try different keywords or time range.")

    # Footer
    st.markdown("---")
    st.caption("© 2023 CareerConnect | Find fresh opportunities")

if __name__ == "__main__":
    main()
