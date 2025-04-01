import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Global Job Finder", page_icon="🌎", layout="centered")

# ---------------- Global Job Portals ----------------
def generate_job_links(keyword, location, country):
    query = urllib.parse.quote_plus(keyword)
    loc = urllib.parse.quote_plus(location)
    
    portals = []

    # 🌎 USA
    if country == "USA":
        portals = [
            ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}"),
            ("Indeed", f"https://www.indeed.com/jobs?q={query}&l={loc}"),
            ("Glassdoor", f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locT=C&locId=1&locKeyword={loc}"),
            ("Monster", f"https://www.monster.com/jobs/search/?q={query}&where={loc}"),
            ("ZipRecruiter", f"https://www.ziprecruiter.com/jobs-search?search={query}&location={loc}"),
            ("CareerBuilder", f"https://www.careerbuilder.com/jobs?keywords={query}&location={loc}"),
            ("SimplyHired", f"https://www.simplyhired.com/search?q={query}&l={loc}"),
            ("Jobvite", f"https://jobs.jobvite.com/search?q={query}")
        ]

    # 🇬🇧 UK
    elif country == "UK":
        portals = [
            ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}"),
            ("Indeed UK", f"https://uk.indeed.com/jobs?q={query}&l={loc}"),
            ("Reed", f"https://www.reed.co.uk/jobs/{query}-jobs-in-{location.replace(' ', '-') }"),
            ("Monster UK", f"https://www.monster.co.uk/jobs/search/?q={query}&where={loc}"),
            ("TotalJobs", f"https://www.totaljobs.com/jobs/{query}/in-{location.replace(' ', '-')}"),
            ("CV-Library", f"https://www.cv-library.co.uk/search-jobs?kw={query}&loc={loc}"),
            ("Jobsite", f"https://www.jobsite.co.uk/jobs/{query}/in-{location.replace(' ', '-')}"),
            ("Adzuna", f"https://www.adzuna.co.uk/search?q={query}&location={loc}")
        ]

    # 🇮🇳 India
    elif country == "India":
        portals = [
            ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}"),
            ("Naukri", f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"),
            ("Indeed India", f"https://www.indeed.co.in/jobs?q={query}&l={loc}"),
            ("Monster India", f"https://www.monsterindia.com/srp/results?query={query}&locations={loc}"),
            ("TimesJobs", f"https://www.timesjobs.com/candidate/job-search.html?txtKeywords={query}&txtLocation={loc}"),
            ("Jobsearch", f"https://www.jobsearch.co.in/search-jobs?q={query}&l={loc}"),
            ("Shine", f"https://www.shine.com/job-search/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"),
            ("Freshersworld", f"https://www.freshersworld.com/jobs/jobsearch/{query}?location={loc}")
        ]

    # 🇦🇺 Australia
    elif country == "Australia":
        portals = [
            ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}"),
            ("Seek", f"https://www.seek.com.au/{keyword.replace(' ', '-')}-jobs/in-{location.replace(' ', '-')}"),
            ("Indeed AU", f"https://au.indeed.com/jobs?q={query}&l={loc}"),
            ("JobActive", f"https://www.workforceaustralia.gov.au/jobs?keyword={query}&location={loc}"),
            ("CareerOne", f"https://www.careerone.com.au/jobs?q={query}&where={loc}"),
            ("Adzuna AU", f"https://www.adzuna.com.au/search?q={query}&location={loc}"),
            ("Jora", f"https://au.jora.com/j?sp=homepage&q={query}&l={loc}"),
            ("SimplyHired", f"https://www.simplyhired.com.au/search?q={query}&l={loc}")
        ]

    # 🇨🇦 Canada
    elif country == "Canada":
        portals = [
            ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}"),
            ("Indeed CA", f"https://ca.indeed.com/jobs?q={query}&l={loc}"),
            ("Job Bank", f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={query}&locationstring={loc}"),
            ("Monster Canada", f"https://www.monster.ca/jobs/search/?q={query}&where={loc}"),
            ("Workopolis", f"https://www.workopolis.com/jobsearch/find-jobs?ak={query}&l={loc}"),
            ("SimplyHired", f"https://www.simplyhired.ca/search?q={query}&l={loc}"),
            ("Eluta", f"https://www.eluta.ca/search?q={query}&l={loc}"),
            ("Neuvoo", f"https://neuvoo.ca/jobs/?k={query}&l={loc}")
        ]

    # 🌍 Others fallback
    else:
        portals = [
            ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}"),
            ("Indeed", f"https://www.indeed.com/jobs?q={query}&l={loc}"),
            ("Google Jobs", f"https://www.google.com/search?q={query}+jobs+in+{loc}")
        ]
    
    return portals

# ---------------- UI ----------------
st.title("🌍 Global AI Job Finder")

with st.form("job_form"):
    keyword = st.text_input("Job Title / Keywords", "Data Scientist")
    location = st.text_input("Preferred Location", "Remote")
    country = st.selectbox("🌐 Select Country", ["USA", "UK", "India", "Australia", "Canada", "Others"])
    time_filter = st.selectbox("LinkedIn Job Time Filter", ["Past 24 hours", "Past week", "Past month", "Any time"])
    submit = st.form_submit_button("🔍 Find Jobs")

if submit:
    st.subheader(f"🔗 Smart Job Search Links ({country})")
    job_links = generate_job_links(keyword, location, country)
    for name, url in job_links:
        st.markdown(f"✅ [{name}]({url})")

    st.success("✅ All job portals loaded with your search filters!")
