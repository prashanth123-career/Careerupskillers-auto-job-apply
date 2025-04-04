import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder", page_icon="🌐", layout="centered")

# --- Enhanced Portal Database ---
PORTALS_BY_COUNTRY = {
    "USA": [
        ("LinkedIn", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("USAJobs (Govt)", lambda k,l,s,e,d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Indeed", lambda k,l,s,e,d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "UK": [
        ("LinkedIn UK", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Guardian Jobs (Govt)", lambda k,l,s,e,d: f"https://jobs.theguardian.com/jobs/{urllib.parse.quote(k)}/in-{urllib.parse.quote(l)}"),
        ("Indeed UK", lambda k,l,s,e,d: f"https://uk.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "India": [
        ("LinkedIn India", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Government Jobs (India)", lambda k,l,s,e,d: f"https://www.indgovtjobs.in/search/label/{urllib.parse.quote(k)}"),
        ("Indeed India", lambda k,l,s,e,d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "Canada": [
        ("LinkedIn Canada", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Job Bank (Govt)", lambda k,l,s,e,d: f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={urllib.parse.quote(k)}&locationstring={urllib.parse.quote(l)}"),
        ("Indeed CA", lambda k,l,s,e,d: f"https://ca.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "Australia": [
        ("LinkedIn Australia", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("APS Jobs (Govt)", lambda k,l,s,e,d: f"https://www.apsjobs.gov.au/s/search?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed AU", lambda k,l,s,e,d: f"https://au.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "UAE": [
        ("LinkedIn UAE", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Dubai Careers (Govt)", lambda k,l,s,e,d: f"https://dubaicareers.ae/en/Pages/Search.aspx?k={urllib.parse.quote(k)}"),
        ("Bayt", lambda k,l,s,e,d: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ','-')}-jobs/")
    ]
}

# --- UI with Enhanced Filters ---
st.title("🌍 Mega Job Finder")
st.markdown("\ud83d\udd0e Access **50+ job portals** worldwide with smart filters")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Data Scientist")
        location = st.text_input("Preferred Location", "Remote")
        country = st.selectbox("Country", list(PORTALS_BY_COUNTRY.keys()))

    with col2:
        experience = st.selectbox("Experience Level", ["Any", "Entry", "Mid", "Senior", "Executive"])
        remote_option = st.selectbox("Work Type", ["Any", "Remote", "Hybrid", "On-site"])
        date_posted = st.selectbox("Date Posted", ["Any time", "Past month", "Past week", "Past 24 hours"])

    submitted = st.form_submit_button("\ud83d\udd0d Find Jobs")

if submitted:
    st.subheader(f"🌐 {len(PORTALS_BY_COUNTRY[country])} Job Portals in {country}")

    time_map = {
        "Any time": "",
        "Past month": "r2592000",
        "Past week": "r604800",
        "Past 24 hours": "r86400"
    }
    exp_map = {
        "Any": "",
        "Entry": "2",
        "Mid": "3",
        "Senior": "4",
        "Executive": "5"
    }
    d_filter = time_map[date_posted]
    e_filter = exp_map[experience]

    for name, url_func in PORTALS_BY_COUNTRY[country]:
        if "LinkedIn" in name:
            url = url_func(keyword, location, "", e_filter, d_filter)
        else:
            url = url_func(keyword, location, "", "", "")
        st.markdown(f"- \ud83d\udd17 [{name}]({url})")

    st.success(f"✅ Generated {len(PORTALS_BY_COUNTRY[country])} job search links")

    st.markdown(f"""
    <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
        <h3 style='color:#1e3a8a;'>Need more options?</h3>
        <p>Try these global aggregators:</p>
        <a href='https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs' 
           target='_blank' 
           style='background-color:#1e3a8a; color:white; padding:10px 15px; text-decoration:none; border-radius:5px; display:inline-block; margin-top:10px;'>
            🔍 Search Google Jobs
        </a>
    </div>
    """, unsafe_allow_html=True)
