import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Global AI Job Finder", page_icon="🌎", layout="centered")

# ---------------- LinkedIn Smart Filtered Link ----------------
def linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply):
    time_map = {
        "Past 24 hours": "r86400",
        "Past week": "r604800",
        "Past month": "r2592000",
        "Any time": ""
    }
    exp_map = {
        "Any": "",
        "Internship": "1",
        "Entry level": "2",
        "Associate": "3",
        "Mid-Senior level": "4",
        "Director": "5"
    }
    remote_map = {
        "Any": "",
        "Remote": "2",
        "On-site": "1",
        "Hybrid": "3"
    }

    params = {
        "keywords": keyword,
        "location": location,
        "f_TPR": time_map.get(time_filter, ""),
        "f_E": exp_map.get(experience, ""),
        "f_WT": remote_map.get(remote_option, ""),
        "f_AL": "true" if easy_apply else ""
    }

    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

# ---------------- Global Portals Generator ----------------
def generate_job_links(keyword, location, country):
    query = urllib.parse.quote_plus(keyword)
    loc = urllib.parse.quote_plus(location)

    portals = []

    if country == "USA":
        portals = [
            ("Indeed", f"https://www.indeed.com/jobs?q={query}&l={loc}"),
            ("Glassdoor", f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locKeyword={loc}"),
            ("Monster", f"https://www.monster.com/jobs/search/?q={query}&where={loc}"),
            ("ZipRecruiter", f"https://www.ziprecruiter.com/jobs-search?search={query}&location={loc}"),
            ("CareerBuilder", f"https://www.careerbuilder.com/jobs?keywords={query}&location={loc}"),
            ("SimplyHired", f"https://www.simplyhired.com/search?q={query}&l={loc}"),
            ("Jobvite", f"https://jobs.jobvite.com/search?q={query}")
        ]

    elif country == "UK":
        portals = [
            ("Indeed UK", f"https://uk.indeed.com/jobs?q={query}&l={loc}"),
            ("Reed", f"https://www.reed.co.uk/jobs/{query}-jobs-in-{location.replace(' ', '-') }"),
            ("Monster UK", f"https://www.monster.co.uk/jobs/search/?q={query}&where={loc}"),
            ("TotalJobs", f"https://www.totaljobs.com/jobs/{query}/in-{location.replace(' ', '-')}"),
            ("CV-Library", f"https://www.cv-library.co.uk/search-jobs?kw={query}&loc={loc}"),
            ("Jobsite", f"https://www.jobsite.co.uk/jobs/{query}/in-{location.replace(' ', '-')}"),
            ("Adzuna", f"https://www.adzuna.co.uk/search?q={query}&location={loc}")
        ]

    elif country == "India":
        portals = [
            ("Naukri", f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"),
            ("Indeed India", f"https://www.indeed.co.in/jobs?q={query}&l={loc}"),
            ("Monster India", f"https://www.monsterindia.com/srp/results?query={query}&locations={loc}"),
            ("TimesJobs", f"https://www.timesjobs.com/candidate/job-search.html?txtKeywords={query}&txtLocation={loc}"),
            ("Shine", f"https://www.shine.com/job-search/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"),
            ("Freshersworld", f"https://www.freshersworld.com/jobs/jobsearch/{query}?location={loc}")
        ]

    elif country == "Australia":
        portals = [
            ("Seek", f"https://www.seek.com.au/{keyword.replace(' ', '-')}-jobs/in-{location.replace(' ', '-')}"),
            ("Indeed AU", f"https://au.indeed.com/jobs?q={query}&l={loc}"),
            ("JobActive", f"https://www.workforceaustralia.gov.au/jobs?keyword={query}&location={loc}"),
            ("CareerOne", f"https://www.careerone.com.au/jobs?q={query}&where={loc}"),
            ("Adzuna AU", f"https://www.adzuna.com.au/search?q={query}&location={loc}"),
            ("Jora", f"https://au.jora.com/j?sp=homepage&q={query}&l={loc}")
        ]

    elif country == "Canada":
        portals = [
            ("Indeed CA", f"https://ca.indeed.com/jobs?q={query}&l={loc}"),
            ("Job Bank", f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={query}&locationstring={loc}"),
            ("Monster Canada", f"https://www.monster.ca/jobs/search/?q={query}&where={loc}"),
            ("Workopolis", f"https://www.workopolis.com/jobsearch/find-jobs?ak={query}&l={loc}"),
            ("SimplyHired", f"https://www.simplyhired.ca/search?q={query}&l={loc}"),
            ("Eluta", f"https://www.eluta.ca/search?q={query}&l={loc}"),
            ("Neuvoo", f"https://neuvoo.ca/jobs/?k={query}&l={loc}")
        ]

    else:  # Others
        portals = [
            ("Indeed", f"https://www.indeed.com/jobs?q={query}&l={loc}"),
            ("Google Jobs", f"https://www.google.com/search?q={query}+jobs+in+{loc}")
        ]

    return portals

# ---------------- UI ----------------
st.title("🌍 Global AI Job Finder")
st.markdown("🔎 Get LinkedIn + top job portals for any country with smart filters!")

with st.form("job_form"):
    keyword = st.text_input("Job Title / Keywords", "Data Scientist")
    location = st.text_input("Preferred Location", "Remote")
    country = st.selectbox("🌐 Country", ["USA", "UK", "India", "Australia", "Canada", "Others"])
    time_filter = st.selectbox("📅 LinkedIn Date Posted", ["Past 24 hours", "Past week", "Past month", "Any time"])
    experience = st.selectbox("📈 Experience Level", ["Any", "Internship", "Entry level", "Associate", "Mid-Senior level", "Director"])
    remote_option = st.selectbox("🏢 Work Type", ["Any", "Remote", "On-site", "Hybrid"])
    easy_apply = st.checkbox("⚡ Easy Apply only", value=False)
    submitted = st.form_submit_button("🔍 Find Jobs")

if submitted:
    st.subheader("🔗 LinkedIn Smart Search")
    linkedin_link = linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply)
    st.markdown(f"✅ [Open LinkedIn Search]({linkedin_link})")

    st.subheader(f"🌐 Job Portals in {country}")
    for name, url in generate_job_links(keyword, location, country):
        st.markdown(f"- 🔗 [{name}]({url})")

    st.success("🎯 All job search links generated successfully!")
