import streamlit as st
import openai
import os
from bs4 import BeautifulSoup
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --------------- CONFIG ------------------
st.set_page_config(page_title="AI Job Finder", page_icon="🤖", layout="wide")
st.title("✨ AI Cover Letter & Job Finder")

openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store your key in .streamlit/secrets.toml

# --------------- GPT Cover Letter Generator ------------------
def generate_cover_letter_openai(designation, experience, company, skills):
    prompt = f"""
Write a professional cover letter for a candidate applying for a {designation} role.
The candidate has {experience} years of experience at {company}, and has skills: {skills}.
Be concise, confident, and polite.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[
                {"role": "system", "content": "You are a career advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating cover letter: {e}"

# --------------- LinkedIn Scraper ------------------
@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_linkedin_url(keyword, location, time_filter):
    base_url = "https://www.linkedin.com/jobs/search/"
    time_map = {
        "Past 24 hours": "r86400",
        "Past week": "r604800",
        "Past month": "r2592000",
        "Any time": ""
    }
    params = {
        "keywords": keyword,
        "location": location,
        "f_TPR": time_map.get(time_filter, "")
    }
    return f"{base_url}?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

def scrape_linkedin(keyword, location, time_filter):
    driver = get_driver()
    try:
        url = get_linkedin_url(keyword, location, time_filter)
        driver.get(url)
        time.sleep(3)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        listings = soup.find_all("li", class_="jobs-search__results-list-item")[:8]
        jobs = []
        for job in listings:
            title = job.find("a", class_="job-card-list__title")
            company = job.find("h4", class_="job-card-container__company-name")
            time_posted = job.find("time", class_="job-search-card__listdate")
            if title:
                jobs.append({
                    "Job Title": title.text.strip(),
                    "Company": company.text.strip() if company else "N/A",
                    "Posted": time_posted.text.strip() if time_posted else time_filter,
                    "Apply Link": get_linkedin_url(keyword, location, time_filter)
                })
        return jobs
    except Exception as e:
        st.error(f"Scraping failed: {e}")
        return []
    finally:
        driver.quit()

# --------------- Competitor Suggestion ------------------
def suggest_competitors(company):
    competitors = {
        "TCS": ["Infosys", "Wipro", "Cognizant"],
        "Wipro": ["TCS", "HCL", "Capgemini"],
        "Google": ["Microsoft", "Amazon", "Meta"],
        "Amazon": ["Flipkart", "eBay", "Walmart"],
        "Accenture": ["IBM", "Capgemini", "Deloitte"]
    }
    return competitors.get(company.strip(), ["Infosys", "TCS", "HCL"])

# --------------- UI Form ------------------
with st.form("manual_input"):
    st.subheader("📌 Enter Your Details")
    col1, col2 = st.columns(2)
    with col1:
        designation = st.text_input("Designation", "Data Analyst")
        experience = st.number_input("Years of Experience", 1, 40, 2)
    with col2:
        company = st.text_input("Previous Company", "TCS")
        location = st.text_input("Job Location", "Remote")

    skills = st.text_area("Skills (comma-separated)", "Python, SQL, Excel")
    time_filter = st.selectbox("Jobs posted in:", ["Past 24 hours", "Past week", "Past month", "Any time"], index=1)
    submitted = st.form_submit_button("✨ Generate & Find Jobs")

if submitted:
    with st.spinner("Generating cover letter..."):
        letter = generate_cover_letter_openai(designation, experience, company, skills)
        st.success("Cover Letter Ready!")
        st.code(letter)

    with st.expander("🏢 Suggested Competitor Companies"):
        competitors = suggest_competitors(company)
        st.markdown(", ".join(competitors))

    with st.spinner("🔎 Searching LinkedIn..."):
        jobs = scrape_linkedin(designation, location, time_filter)

    if jobs:
        st.success(f"Found {len(jobs)} job listings")
        for i, job in enumerate(jobs):
            with st.expander(f"{i+1}. {job['Job Title']} at {job['Company']} ({job['Posted']})"):
                st.markdown(f"[🔗 Apply on LinkedIn]({job['Apply Link']})")
    else:
        st.warning("No jobs found.")

st.markdown("---")
st.caption("🚀 Built by CareerUpskillers • Powered by OpenAI")
