# Smart Cover Letter + Job Search App (Manual Input + LinkedIn Integration)
import streamlit as st
import re
import time
import urllib.parse
from transformers import pipeline
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- Setup --------------------
st.set_page_config(page_title="Smart Job & Cover Letter App", page_icon="✉️", layout="wide")
st.title("✉️ AI Cover Letter & Job Finder")
st.markdown("Fill in your career details manually. Let AI generate a cover letter & find jobs for you!")

# -------------------- GPT Model --------------------
@st.cache_resource
def load_gpt():
    return pipeline("text2text-generation", model="google/flan-t5-base")

# -------------------- LinkedIn Job Scraper --------------------
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

# -------------------- Competitor Companies --------------------
def suggest_competitors(company):
    competitors = {
        "TCS": ["Infosys", "Wipro", "Cognizant"],
        "Wipro": ["TCS", "HCL", "Capgemini"],
        "Google": ["Microsoft", "Amazon", "Meta"],
        "Amazon": ["Flipkart", "eBay", "Walmart"],
        "Accenture": ["IBM", "Capgemini", "Deloitte"]
    }
    return competitors.get(company.strip(), ["Infosys", "TCS", "HCL"])

# -------------------- Streamlit Form --------------------
with st.form("manual_input"):
    st.subheader("📌 Enter Your Career Details")
    
    col1, col2 = st.columns(2)
    with col1:
        designation = st.text_input("Your Designation / Role", "Data Analyst")
        experience = st.number_input("Years of Experience", 0, 50, 2)
    with col2:
        company = st.text_input("Previous Company", "TCS")
        location = st.text_input("Preferred Job Location", "Remote")

    skills = st.text_area("Your Technical Skills (comma-separated)", "Python, SQL, Power BI, Excel")

    time_filter = st.selectbox("🕒 Show Jobs Posted In", ["Past 24 hours", "Past week", "Past month", "Any time"], index=1)

    submitted = st.form_submit_button("✨ Generate Cover Letter & Find Jobs")

# -------------------- Result --------------------
if submitted:
    if not designation or not skills:
        st.warning("Please fill in your designation and skills.")
    else:
        with st.spinner("Generating cover letter using AI..."):
            model = load_gpt()
            prompt = f"""Write a professional and concise cover letter for a {designation} role.
The candidate has {experience} years of experience at {company}, and has skills: {skills}.
"""
            try:
                output = model(prompt, max_length=400, do_sample=False)
                cover_letter = output[0]['generated_text']
            except:
                cover_letter = "Could not generate cover letter."

        st.success("✅ Cover Letter Generated")
        with st.expander("✉️ AI Cover Letter"):
            st.markdown(cover_letter)

        # Competitor companies
        competitors = suggest_competitors(company)
        with st.expander("🏢 Competitor Companies to Watch"):
            st.markdown(", ".join(competitors))

        with st.spinner("🔍 Searching LinkedIn for job listings..."):
            jobs = scrape_linkedin_jobs(designation, location, time_filter)

        if jobs:
            st.success(f"🔗 Found {len(jobs)} job listings on LinkedIn")
            for i, job in enumerate(jobs):
                with st.expander(f"{i+1}. {job['Job Title']} at {job['Company']} ({job['Posted']})"):
                    st.markdown(f"[Apply on LinkedIn]({job['Apply Link']})")
        else:
            st.warning("No jobs found. Try different designation or time filter.")

st.markdown("---")
st.caption("Built by CareerUpskillers • AI Tools for Job Seekers")
