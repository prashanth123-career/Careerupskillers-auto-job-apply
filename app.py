import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder", page_icon="🌐", layout="centered")

# --- Portal database with LinkedIn filter support ---
PORTALS_BY_COUNTRY = {
    "USA": [
        ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("USAJobs (Govt)", lambda k, l, e, d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Indeed", lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Glassdoor", lambda k, l, e, d: f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(k)}&locT=C&locName={urllib.parse.quote(l)}"),
        ("Monster", lambda k, l, e, d: f"https://www.monster.com/jobs/search?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("CareerBuilder", lambda k, l, e, d: f"https://www.careerbuilder.com/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "UK": [
        ("LinkedIn UK", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Guardian Jobs (Govt)", lambda k, l, e, d: f"https://jobs.theguardian.com/jobs/{urllib.parse.quote(k)}/in-{urllib.parse.quote(l)}"),
        ("Indeed UK", lambda k, l, e, d: f"https://uk.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Reed", lambda k, l, e, d: f"https://www.reed.co.uk/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Totaljobs", lambda k, l, e, d: f"https://www.totaljobs.com/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
        ("CV-Library", lambda k, l, e, d: f"https://www.cv-library.co.uk/search-jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "India": [
        ("LinkedIn India", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Government Jobs (India)", lambda k, l, e, d: f"https://www.indgovtjobs.in/search/label/{urllib.parse.quote(k)}"),
        ("Indeed India", lambda k, l, e, d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Naukri", lambda k, l, e, d: f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-') if l != 'Remote' else 'india'}"),
        ("Shine", lambda k, l, e, d: f"https://www.shine.com/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("TimesJobs", lambda k, l, e, d: f"https://www.timesjobs.com/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("Freshersworld", lambda k, l, e, d: f"https://www.freshersworld.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Canada": [
        ("LinkedIn Canada", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Job Bank (Govt)", lambda k, l, e, d: f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={urllib.parse.quote(k)}&locationstring={urllib.parse.quote(l)}"),
        ("Indeed CA", lambda k, l, e, d: f"https://ca.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Workopolis", lambda k, l, e, d: f"https://www.workopolis.com/jobsearch/find-jobs?ak={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Monster CA", lambda k, l, e, d: f"https://www.monster.ca/jobs/search?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("Eluta", lambda k, l, e, d: f"https://www.eluta.ca/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Australia": [
        ("LinkedIn Australia", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("APS Jobs (Govt)", lambda k, l, e, d: f"https://www.apsjobs.gov.au/s/search?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed AU", lambda k, l, e, d: f"https://au.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Seek", lambda k, l, e, d: f"https://www.seek.com.au/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
        ("CareerOne", lambda k, l, e, d: f"https://www.careerone.com.au/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Jora", lambda k, l, e, d: f"https://au.jora.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "UAE": [
        ("LinkedIn UAE", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Dubai Careers (Govt)", lambda k, l, e, d: f"https://dubaicareers.ae/en/Pages/Search.aspx?k={urllib.parse.quote(k)}"),
        ("Bayt", lambda k, l, e, d: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ', '-')}-jobs/"),
        ("GulfTalent", lambda k, l, e, d: f"https://www.gulftalent.com/uae/jobs?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Naukrigulf", lambda k, l, e, d: f"https://www.naukrigulf.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("JobsAbuDhabi", lambda k, l, e, d: f"https://jobsabudhabi.ae/en/search-jobs/?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Germany": [
        ("LinkedIn Germany", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("StepStone", lambda k, l, e, d: f"https://www.stepstone.de/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
        ("Xing", lambda k, l, e, d: f"https://www.xing.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Jobware", lambda k, l, e, d: f"https://www.jobware.de/jobs/{k.lower().replace(' ', '-')}/{l.lower().replace(' ', '-')}"),
        ("Meinestadt", lambda k, l, e, d: f"https://jobs.meinestadt.de/deutschland?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Bundesagentur für Arbeit (Govt)", lambda k, l, e, d: f"https://jobboerse.arbeitsagentur.de/stellenangebote/suche?was={urllib.parse.quote(k)}&wo={urllib.parse.quote(l)}")
    ]
}

# --- UI ---
st.title("🌍 Mega Job Finder")
st.markdown("🔍 Access **50+ job portals** worldwide with smart filters")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Data Scientist")
        location = st.text_input("Preferred Location", "Remote")
        country = st.selectbox("Country", list(PORTALS_BY_COUNTRY.keys()))
    with col2:
        experience = st.selectbox("Experience Level", ["Any", "Entry", "Mid", "Senior", "Executive"])
        date_posted = st.selectbox("Date Posted", ["Any time", "Past month", "Past week", "Past 24 hours"])

    submitted = st.form_submit_button("🔍 Find Jobs")

if submitted:
    st.subheader(f"🌐 Job Portals in {country}")

    # Filters mapping
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

    # Display portals as buttons using HTML for redirection
    for name, url_func in PORTALS_BY_COUNTRY[country]:
        if "LinkedIn" in name:
            url = url_func(keyword, location, e_filter, d_filter)
        else:
            url = url_func(keyword, location, "", "")  # Non-LinkedIn portals don’t use exp/date filters here
        
        # Create a button with HTML that opens in a new tab
        button_html = f"""
        <a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 5px 0;">
            🔍 Search on {name}
        </a>
        <p style="font-size: 12px; color: #666;">If you are logged into {name}, this will take you directly to the relevant job listings.</p>
        """
        st.markdown(button_html, unsafe_allow_html=True)

    st.success(f"✅ Generated {len(PORTALS_BY_COUNTRY[country])} job search links.")

    # Google fallback
    google_jobs = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs"
    st.markdown(f"""
    <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
        <h3 style='color:#1e3a8a;'>Need more options?</h3>
        <p>Try these global aggregators:</p>
        <a href='{google_jobs}' 
           target='_blank' 
           style='background-color:#1e3a8a; color:white; padding:10px 15px; text-decoration:none; border-radius:5px; display:inline-block; margin-top:10px;'>
            🔍 Search Google Jobs
        </a>
    </div>
    """, unsafe_allow_html=True)
