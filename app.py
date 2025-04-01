import streamlit as st
import urllib.parse
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="AI Job Finder", page_icon="💼", layout="centered")

# ---------------- LinkedIn Search Link ----------------
def linkedin_url(keyword, location, time_filter):
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
    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

# ---------------- Job Scrapers ----------------
def scrape_naukri(keyword, location):
    try:
        url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for card in soup.select(".jobTuple")[:10]:
            title = card.select_one("a.title")
            company = card.select_one("a.subTitle")
            if title and company:
                jobs.append({
                    "Title": title.get_text(strip=True),
                    "Company": company.text.strip(),
                    "Link": title['href'],
                    "Platform": "Naukri"
                })
        return jobs
    except:
        return []

def scrape_indeed(keyword, location):
    try:
        url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for div in soup.find_all("a", class_="tapItem")[:10]:
            title = div.find("h2")
            company = div.find("span", class_="companyName")
            link = "https://www.indeed.com" + div.get("href") if div.get("href") else ""
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

def scrape_timesjobs(keyword):
    try:
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&txtKeywords={keyword.replace(' ', '%20')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for job in soup.find_all("li", class_="clearfix job-bx wht-shd-bx")[:10]:
            title = job.find("h2")
            company = job.find("h3", class_="joblist-comp-name")
            link = title.find("a")["href"] if title and title.find("a") else ""
            if title and company:
                jobs.append({
                    "Title": title.text.strip(),
                    "Company": company.text.strip(),
                    "Link": link,
                    "Platform": "TimesJobs"
                })
        return jobs
    except:
        return []

def scrape_glassdoor(keyword, location):
    try:
        query = keyword.replace(" ", "-")
        loc = location.replace(" ", "-")
        url = f"https://www.glassdoor.com/Job/{loc}-{query}-jobs-SRCH_IL.0,6_IC{hash(loc)}_KO7,{7+len(query)}.htm"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for div in soup.select("li.react-job-listing")[:10]:
            title_tag = div.find("a", {"data-test": "job-link"})
            company_tag = div.find("div", class_="jobHeader")
            if title_tag and company_tag:
                title = title_tag.text.strip()
                company = company_tag.text.strip()
                link = "https://www.glassdoor.com" + title_tag["href"]
                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Link": link,
                    "Platform": "Glassdoor"
                })
        return jobs
    except:
        return []

# ---------------- Streamlit UI ----------------
st.title("💼 All-in-One Job Finder")

with st.form("job_search"):
    keyword = st.text_input("Job Title / Keyword", "Data Scientist")
    location = st.text_input("Preferred Location", "Remote")
    time_filter = st.selectbox("LinkedIn Posting Time", ["Past 24 hours", "Past week", "Past month", "Any time"])
    submitted = st.form_submit_button("🔍 Search Jobs")

if submitted:
    with st.spinner("Searching across platforms..."):
        # 1. LinkedIn
        linkedin_job_url = linkedin_url(keyword, location, time_filter)
        st.subheader("🔗 LinkedIn Search")
        st.markdown(f"[Click here to view LinkedIn Jobs]({linkedin_job_url})")

        # 2. Scrape all others
        raw_jobs = []
        raw_jobs += scrape_naukri(keyword, location)
        raw_jobs += scrape_indeed(keyword, location)
        raw_jobs += scrape_timesjobs(keyword)
        raw_jobs += scrape_glassdoor(keyword, location)

        # 3. Deduplicate
        seen = set()
        job_list = []
        for job in raw_jobs:
            key = (job["Title"].strip().lower(), job["Company"].strip().lower(), job["Link"].strip())
            if key not in seen:
                seen.add(key)
                job_list.append(job)

        # 4. Show fallback if nothing found
        if not job_list:
            job_list = [
                {"Title": "Data Analyst (Remote)", "Company": "DataCorp", "Link": "#", "Platform": "Simulated - Naukri"},
                {"Title": "ML Engineer", "Company": "SmartAI", "Link": "#", "Platform": "Simulated - Glassdoor"},
                {"Title": "Junior Data Scientist", "Company": "Insightful", "Link": "#", "Platform": "Simulated - TimesJobs"}
            ]
            st.info("⚠️ No live jobs found — showing fallback samples.")

    st.subheader("📋 Jobs from Naukri, Indeed, TimesJobs, Glassdoor")
    for i, job in enumerate(job_list):
        st.markdown(f"**{i+1}. {job['Title']}**  \n🧑‍💼 {job['Company']}  \n🌐 *{job['Platform']}*  \n🔗 [Apply Now]({job['Link']})")
        st.markdown("---")

    df = pd.DataFrame(job_list)
    st.download_button("📥 Download as CSV", df.to_csv(index=False), "job_list.csv", "text/csv")
