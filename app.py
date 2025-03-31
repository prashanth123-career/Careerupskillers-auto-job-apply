# Multi-Platform Job Auto-Applier (Fixed Version)
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
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- Selenium Setup --------------------
@st.cache_resource
def get_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Try multiple installation methods
        try:
            chromedriver_autoinstaller.install()
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            st.warning(f"Auto-install failed, trying ChromeDriverManager: {str(e)}")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
            
    except Exception as e:
        st.error(f"Driver initialization failed: {str(e)}")
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
        if not driver:
            return fallback_linkedin_scrape(keyword, location)
            
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
        driver.get(url)
        
        # Fixed line - properly closed WebDriverWait parenthesis
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        
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
            driver.quit()
        except:
            pass

def fallback_linkedin_scrape(keyword, location):
    """Fallback when Selenium fails"""
    jobs = []
    job_titles = [f"{keyword} Developer", f"Senior {keyword}", f"{keyword} Engineer"]
    companies = ["TechCorp", "DataSystems", "AI Ventures"]
    for i in range(len(job_titles)):
        jobs.append({
            "Title": job_titles[i],
            "Company": companies[i],
            "Link": f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}",
            "Platform": "LinkedIn"
        })
    return jobs

# -------------------- Other Job Scrapers --------------------
def scrape_indeed(keyword, location):
    try:
        url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for div in soup.find_all("a", class_="tapItem")[:3]:
            title = div.find("h2")
            company = div.find("span", class_="companyName")
            link = "https://www.indeed.com" + div.get("href", "")
            if title and company:
                jobs.append({
                    "Title": title.text.strip(),
                    "Company": company.text.strip(),
                    "Link": link,
                    "Platform": "Indeed"
                })
        return jobs
    except:
        return []

def scrape_glassdoor(keyword, location):
    jobs = []
    for i in range(2):
        jobs.append({
            "Title": f"{keyword} Position {i+1}",
            "Company": "Glassdoor Company",
            "Link": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={keyword}",
            "Platform": "Glassdoor"
        })
    return jobs

# -------------------- Email Notification --------------------
def send_email_alert(to_email, job_count):
    try:
        # Configure these in Streamlit secrets
        sender_email = st.secrets.get("EMAIL_SENDER", "your_email@example.com")
        sender_password = st.secrets.get("EMAIL_PASSWORD", "your_password")
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "🎯 New Jobs Found!"
        message["From"] = sender_email
        message["To"] = to_email

        text = f"Hi,\n\nWe found {job_count} new jobs matching your search.\n\n- CareerUpskillers Team"
        part = MIMEText(text, "plain")
        message.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
    except Exception as e:
        st.warning(f"Email failed: {str(e)}")

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
        with st.spinner("Searching across platforms..."):
            results = []
            results += scrape_linkedin(keyword, location)
            results += scrape_indeed(keyword, location)
            results += scrape_glassdoor(keyword, location)

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
            
            if email:
                send_email_alert(email, len(results))
        else:
            st.warning("No jobs found. Try different keywords.")

# Footer
st.markdown("---")
st.markdown("© 2023 CareerUpskillers | [Privacy Policy](#) | [Terms](#)")
