import streamlit as st
import urllib.parse

st.set_page_config(page_title="AI Job Finder", page_icon="💼", layout="centered")

# ---------------- Job URLs ----------------
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

def naukri_url(keyword, location):
    return f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"

def indeed_url(keyword, location):
    return f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}"

def timesjobs_url(keyword, location):
    return f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&txtKeywords={keyword.replace(' ', '%20')}&txtLocation={location.replace(' ', '%20')}"

def glassdoor_url(keyword, location):
    return f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote_plus(keyword)}&locT=C&locId=1&locKeyword={urllib.parse.quote_plus(location)}"

# ---------------- UI ----------------
st.title("💼 AI Job Finder")

with st.form("job_form"):
    keyword = st.text_input("Job Title / Keywords", "Data Scientist")
    location = st.text_input("Preferred Location", "Remote")
    time_filter = st.selectbox("LinkedIn Posting Time", ["Past 24 hours", "Past week", "Past month", "Any time"])
    submitted = st.form_submit_button("🔍 Search Jobs")

if submitted:
    st.subheader("🔗 Job Search Links")
    st.markdown(f"✅ [View on LinkedIn]({linkedin_url(keyword, location, time_filter)})")
    st.markdown(f"✅ [View on Naukri]({naukri_url(keyword, location)})")
    st.markdown(f"✅ [View on Indeed]({indeed_url(keyword, location)})")
    st.markdown(f"✅ [View on TimesJobs]({timesjobs_url(keyword, location)})")
    st.markdown(f"✅ [View on Glassdoor]({glassdoor_url(keyword, location)})")

    st.success("Search links generated successfully ✅")
