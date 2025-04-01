# LinkedIn Job Scraper with Time Filter
import streamlit as st
import urllib.parse
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --------------- Streamlit Setup ----------------
st.set_page_config(page_title="LinkedIn Job Scraper", page_icon="💼", layout="wide")
st.title("💼 LinkedIn Job Scraper with Time Filters")
st.markdown("Search and apply to latest jobs from LinkedIn based on your preferences.")

# --------------- Get Chrome Driver ---------------
@st.cache_resource
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# --------------- LinkedIn URL Builder ---------------
def get_linkedin_search_url(keyword, location, time_filter):
    base_url = "https://www.linkedin.com/jobs/search/"
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
    query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return f"{base_url}?{query_string}"

# --------------- Job Scraper ----------------------
def scrape_linkedin_jobs(keyword, location, time_filter):
    driver = get_driver()
    try:
        url = get_linkedin_search_url(keyword, location, time_filter)
        driver.get(url)
        time.sleep(3)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )

        # Scroll to load more jobs
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        return parse_listings(soup, keyword, time_filter, location)
    except Exception as e:
        st.warning(f"Scraping failed: {e}")
        return []
    finally:
        try:
            driver.quit()
        except:
            pass

def parse_listings(soup, keyword, time_filter, location):
    jobs = []
    listings = soup.find_all("li", class_="jobs-search__results-list-item")[:10]
    for job in listings:
        title = job.find("a", class_="job-card-list__title")
        company = job.find("h4", class_="job-card-container__company-name")
        time_posted = job.find("time", class_="job-search-card__listdate")

        if title:
            job_title = title.text.strip()
            company_name = company.text.strip() if company else "N/A"
            jobs.append({
                "Job Title": job_title,
                "Company": company_name,
                "Time Posted": time_posted.text.strip() if time_posted else time_filter,
                "Apply Link": get_linkedin_search_url(keyword, location, time_filter)
            })
    return jobs

# --------------- Streamlit UI ----------------------
with st.form("job_search_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("🔍 Job Keyword", "Data Analyst")
    with col2:
        location = st.text_input("📍 Location", "Remote")

    time_filter = st.selectbox(
        "🕒 Filter by Time Posted",
        ["Past 24 hours", "Past week", "Past month", "Any time"]
    )

    submitted = st.form_submit_button("🔎 Search Jobs")

# --------------- Display Results ----------------------
if submitted:
    with st.spinner("Fetching jobs from LinkedIn..."):
        jobs = scrape_linkedin_jobs(keyword, location, time_filter)

        if jobs:
            st.success(f"✅ Found {len(jobs)} job listings")
            for i, job in enumerate(jobs):
                with st.expander(f"{i+1}. {job['Job Title']} at {job['Company']}"):
                    st.markdown(f"**Posted:** {job['Time Posted']}")
                    st.markdown(f"[🔗 View Job on LinkedIn]({job['Apply Link']})")
        else:
            st.warning("❌ No jobs found. Try changing your filters.")

# --------------- Footer ----------------------
st.markdown("---")
st.caption("Made with 💻 by CareerUpskillers – Automate your job hunt easily.")
